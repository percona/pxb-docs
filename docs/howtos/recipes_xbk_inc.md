# Make an Incremental Backup

Backup all InnoDB data and log files - located in `/var/lib/mysql/` -
**once**, then make two daily incremental backups in `/data/backups/mysql/`
(destination). Finally, prepare the backup files to be ready to restore or
use.

## Create one full backup

Making an incremental backup requires a full backup as a base:

```shell
$ xtrabackup --backup --target-dir=/data/backups/mysql/
```

It is important that you **do not run** the `--prepare` command yet.

## Create two incremental backups

Suppose the full backup is on Monday, and you will create an incremental
one on Tuesday:

```shell
$ xtrabackup --backup --target-dir=/data/backups/inc/tue/ \
      --incremental-basedir=/data/backups/mysql/
```

and the same policy is applied on Wednesday:

```shell
$ xtrabackup --backup --target-dir=/data/backups/inc/wed/ \
       --incremental-basedir=/data/backups/inc/tue/
```

## Prepare the base backup

Prepare the base backup (Monday’s backup):

```shell
$ xtrabackup --prepare --apply-log-only --target-dir=/data/backups/mysql/
```

## Roll forward the base data to the first increment

Roll Monday’s data forward to the state on Tuesday:

```shell
$ xtrabackup --prepare --apply-log-only --target-dir=/data/backups/mysql/ \
   --incremental-dir=/data/backups/inc/tue/
```

## Roll forward again to the second increment

Roll forward again to the state on Wednesday (without --apply-log-only):

```shell
xtrabackup --prepare --target-dir=/data/backups/mysql/ \
   --incremental-dir=/data/backups/inc/wed/
```

!!! note

    Starting with [Percona Server for MySQL 8.0.30-22](../release-notes/8.0/8.0.30-23.0.md), preparing a backup in two steps, --prepare --apply-log-only and then a second --prepare is not supported. The second --prepare skips the dynamic metadata and causes corruption.

## Notes

* You might want to set the `--use-memory` to speed up the process if you are on a dedicated server that has enough free memory. See [xtrabackup Option Reference](https://docs.percona.com/percona-xtrabackup/latest/xtrabackup_bin/xbk_option_reference.html)

* See [Incremental Backups](https://docs.percona.com/percona-xtrabackup/latest/xtrabackup_bin/incremental_backups.html)
