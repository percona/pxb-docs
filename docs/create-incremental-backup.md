# Create an incremental backup

*xtrabackup* supports incremental backups, which means that they can copy only all the data that has changed since the last backup.

!!! note
   
    Incremental backups on the MyRocks storage engine do not determine if an earlier full backup or incremental backup contains the same files. **Percona XtraBackup** copies all the MyRocks files each time it takes a backup.

You can perform many incremental backups between each full backup, so you can set up a backup process such as a full backup once a week and an incremental backup every day, or full backups every day and incremental backups every hour.

Incremental backups work because each *InnoDB* page contains a log sequence
number, or LSN. The LSN is the system version number for the
entire database. Each page’s LSN shows how recently it was changed.

An incremental backup copies each page which LSN is newer than the
previous incremental or full backup’s LSN. An algorithm finds the pages that match the criteria. The algorithm reads the data pages and checks the page LSN.

### Use the changed page tracking algorithm 

*Percona XtraBackup* 8.0.30 removes the algorithm that used the [changed page tracking](https://docs.percona.com/percona-server/8.0/management/changed_page_tracking.html) feature in *Percona Server for MySQL*. *Percona Server for MySQL* 8.0.27 deprecated the changed page tracking feature.

With PXB 8.0.27 or earlier, another algorithm enabled the *Percona Server for MySQL* changed page tracking feature. The algorithm generates a bitmap file. The *xtrabackup* binary uses that bitmap file to read only those pages needed for the incremental backup. This method potentially saves resources. The backup enables the algorithm by default if the *xtrabackup* binary discovers the bitmap file. You can override the algorithm with `--incremental-force-scan` which forces a read of all pages even if the bitmap file is available.

## Create an incremental backup 

To make an incremental backup, begin with a full backup as usual. The
*xtrabackup* binary writes a file called `xtrabackup_checkpoints` into
the backup’s target directory. This file contains a line showing the
`to_lsn`, which is the database’s LSN at the end of the backup.
Create the full backup with a following command:

```{.bash data-prompt="$"}
$ xtrabackup --backup --target-dir=/data/backups/base
```

If you look at the `xtrabackup_checkpoints` file, you should see similar
content depending on your LSN nuber:

??? example "Expected output"

    ```{.text .no-copy}
    backup_type = full-backuped
    from_lsn = 0
    to_lsn = 1626007
    last_lsn = 1626007
    compact = 0
    recover_binlog_info = 1
    ```

Now that you have a full backup, you can make an incremental backup based on it. Use the following command:

```{.bash data-prompt="$"}
$ xtrabackup --backup --target-dir=/data/backups/inc1 \
--incremental-basedir=/data/backups/base
```

The `/data/backups/inc1/` directory should now contain delta files, such
as `ibdata1.delta` and `test/table1.ibd.delta`. These represent the
changes since the `LSN 1626007`. If you examine the
`xtrabackup_checkpoints` file in this directory, you should see similar
content to the following:

??? example "Expected output"

    ```{.text .no-copy}
    backup_type = incremental
    from_lsn = 1626007
    to_lsn = 4124244
    last_lsn = 4124244
    compact = 0
    recover_binlog_info = 1
    ```

`from_lsn` is the starting LSN of the backup and for incremental it has to be the same as `to_lsn` (if it is the last checkpoint) of the previous/base backup.

It’s now possible to use this directory as the base for yet another incremental backup:

```{.bash data-prompt="$"}
$ xtrabackup --backup --target-dir=/data/backups/inc2 \
--incremental-basedir=/data/backups/inc1
```

This folder also contains the `xtrabackup_checkpoints`:

??? example "Expected output"

    ```{.text .no-copy}
    backup_type = incremental
    from_lsn = 4124244
    to_lsn = 6938371
    last_lsn = 7110572
    compact = 0
    recover_binlog_info = 1
    ```

!!! note
   
    In this case you can see that there is a difference between the `to_lsn` (last checkpoint LSN) and `last_lsn` (last copied LSN), this means that there was some traffic on the server during the backup process.

The next step is to [prepare](prepare-incremental-backup.md) the backup in order to restore it. 

