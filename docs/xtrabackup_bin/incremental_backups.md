# Incremental Backups

*xtrabackup* supports incremental backups. It copies only the data that has
changed since the last full backup. You can perform multiple incremental backups
between each full backup. You can set up a backup process with a full
backup once a week and an incremental backup every day, or full backups every
day and incremental backups every hour.

!!! note

    Incremental backups on the MyRocks storage engine do not determine if an earlier full backup or incremental backup contains the same files. **Percona XtraBackup** copies all of the MyRocks files each time it takes a backup.

The write-ahead log (WAL) is immutable and append-only. All writes to the WAL are sequential. Every record has a unique, uniformly increasing log sequence number (LSN) which is assigned to page changes. Each page contains a Page LSN that shows the most recent update to that page. An incremental backup copies each page whose
LSN is newer than the previous incremental or the full backup’s
LSN. An incremental backup copies each page whose LSN is newer than the
previous incremental or full backup’s LSN. An algorithm finds the pages that match the criteria. The algorithm reads the data pages and checks the page LSN.

Incremental backups do not actually compare the data files to the previous
backup’s data files. In fact, you can use `--incremental-lsn` to perform
an incremental backup without even having the previous backup, if you know its
LSN. Incremental backups simply read the pages and compare their
LSN to the last backup’s LSN. You still need a full backup to
recover the incremental changes, however; without a full backup to act as a
base, the incremental backups are useless.

### Using the changed page tracking algorithm 

*Percona XtraBackup* 8.0.30 removes the algorithm that used the [changed page tracking](https://docs.percona.com/percona-server/8.0/management/changed_page_tracking.html) feature in *Percona Server for MySQL*. *Percona Server for MySQL* 8.0.27 deprecated the changed page tracking feature.

With PXB 8.0.27 or earlier, another algorithm enabled the *Percona Server for MySQL* changed page tracking feature. The algorithm generates a bitmap file. The *xtrabackup* binary uses that bitmap file to read only those pages needed for the incremental backup. This method potentially saves resources. The backup enables the algorithm by default if the *xtrabackup* binary discovers the bitmap file. You can override the algorithm with `--incremental-force-scan` which forces a read of all pages even if the bitmap file is available.

## Creating an Incremental Backup

To make an incremental backup, begin with a full backup as usual. The
*xtrabackup* binary writes a file called `xtrabackup_checkpoints` into the
backup’s target directory. This file contains a line showing the `to_lsn`,
which is the database’s LSN at the end of the backup. Create the
full backup with a command such as the following:

```
$ xtrabackup --backup --target-dir=/data/backups/base --datadir=/var/lib/mysql/
```

If you look at the `xtrabackup_checkpoints` file, you should see contents
similar to the following:

```
backup_type = full-backuped
from_lsn = 0
to_lsn = 1291135
```

Now that you have a full backup, you can make an incremental backup based on
it. Use a command such as the following:

```
$ xtrabackup --backup --target-dir=/data/backups/inc1 \
--incremental-basedir=/data/backups/base --datadir=/var/lib/mysql/
```

The `/data/backups/inc1/` directory should now contain delta files, such
as `ibdata1.delta` and `test/table1.ibd.delta`. These represent the
changes since the `LSN 1291135`. If you examine the
`xtrabackup_checkpoints` file in this directory, you should see something
similar to the following:

```
backup_type = incremental
from_lsn = 1291135
to_lsn = 1291340
```

The meaning should be self-evident. It’s now possible to use this directory as
the base for yet another incremental backup:

```
$ xtrabackup --backup --target-dir=/data/backups/inc2 \
--incremental-basedir=/data/backups/inc1 --datadir=/var/lib/mysql/
```

## Preparing the Incremental Backups

The `--prepare` step for incremental backups is not the same as for
normal backups. In normal backups, two types of operations are performed to make
the database consistent: committed transactions are replayed from the log file
against the data files, and uncommitted transactions are rolled back. You must
skip the rollback of uncommitted transactions when preparing a backup, because
transactions that were uncommitted at the time of your backup may be in
progress, and it is likely that they will be committed in the next incremental
backup. You should use the `--apply-log-only` option to prevent the
rollback phase.

!!! note
   
    If you do not use the `--apply-log-only` option to prevent the
    rollback phase, then your incremental backups will be useless. After
    transactions have been rolled back, further incremental backups cannot be
    applied.
 
Beginning with the full backup you created, you can prepare it, and then apply
the incremental differences to it. Recall that you have the following backups:

```
/data/backups/base
/data/backups/inc1
/data/backups/inc2
```

To prepare the base backup, you need to run `--prepare` as usual, but
prevent the rollback phase:

```
xtrabackup --prepare --apply-log-only --target-dir=/data/backups/base
```

The output should end with some text such as the following:

```
101107 20:49:43  InnoDB: Shutdown completed; log sequence number 1291135
```

The log sequence number should match the `to_lsn` of the base backup, which
you saw previously.

This backup is actually safe to restore as-is now,
even though the rollback phase has been skipped. If you restore it and start
*MySQL*, *InnoDB* will detect that the rollback phase was not performed, and it
will do that in the background, as it usually does for a crash recovery upon
start. It will notify you that the database was not shut down normally.

To apply the first incremental backup to the full backup, you should use the
following command:

```
xtrabackup --prepare --apply-log-only --target-dir=/data/backups/base \
--incremental-dir=/data/backups/inc1
```

This applies the delta files to the files in `/data/backups/base`, which
rolls them forward in time to the time of the incremental backup. It then
applies the redo log as usual to the result. The final data is in
`/data/backups/base`, not in the incremental directory. You should see
some output such as the following:

```
incremental backup from 1291135 is enabled.
xtrabackup: cd to /data/backups/base/
xtrabackup: This target seems to be already prepared.
xtrabackup: xtrabackup_logfile detected: size=2097152, start_lsn=(1291340)
Applying /data/backups/inc1/ibdata1.delta ...
Applying /data/backups/inc1/test/table1.ibd.delta ...
.... snip
101107 20:56:30  InnoDB: Shutdown completed; log sequence number 1291340
```

Again, the LSN should match what you saw from your earlier inspection of the
first incremental backup. If you restore the files from
`/data/backups/base`, you should see the state of the database as of the
first incremental backup.

Preparing the second incremental backup is a similar process: apply the deltas
to the (modified) base backup, and you will roll its data forward in time to the
point of the second incremental backup:

```
xtrabackup --prepare --target-dir=/data/backups/base \
--incremental-dir=/data/backups/inc2
```

!!! note
   
    `--apply-log-only` should be used when merging all incrementals
    except the last one. That’s why the previous line doesn’t contain the
    `--apply-log-only` option. Even if the `--apply-log-only` was
    used on the last step, backup would still be consistent but in that case
    server would perform the rollback phase.

If you wish to avoid the notice that *InnoDB* was not shut down normally, when
you applied the desired deltas to the base backup, you can run
`--prepare` again without disabling the rollback phase.

## Restoring Incremental Backups

After preparing the incremental backups, the base directory contains the same
data as the full backup. To restoring this backup, you can use this command:
`xtrabackup --copy-back --target-dir=BASE-DIR`

You may have to change the ownership as detailed on
Restoring a Backup.

## Incremental Streaming Backups Using xbstream

Incremental streaming backups can be performed with the *xbstream* streaming
option. Currently backups are packed in custom **xbstream** format. With this
feature, you need to take a BASE backup as well.

### Making a base backup

```
$ xtrabackup --backup --target-dir=/data/backups
```

### Taking a local backup

```
$ xtrabackup --backup --incremental-lsn=LSN-number --stream=xbstream --target-dir=./ > incremental.xbstream
```

### Unpacking the backup

```
$ xbstream -x < incremental.xbstream
```

### Taking a local backup and streaming it to the remote server and unpacking it

```
$ xtrabackup --backup --incremental-lsn=LSN-number --stream=xbstream --target-dir=./
$ ssh user@hostname " cat - | xbstream -x -C > /backup-dir/"
```
