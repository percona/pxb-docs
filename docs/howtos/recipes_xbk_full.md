# Make a full backup

Backup the InnoDB data and log files - located in `/var/lib/mysql/` - to
`/data/backups/mysql/` (destination). Then, prepare the backup files to be
ready to restore or use (make the data files consistent).

## Make a backup:

```shell
$ xtrabackup --backup --target-dir=/data/backups/mysql/
```

## Prepare the backup:

```shell
$ xtrabackup --prepare --target-dir=/data/backups/mysql/
```

## Success criteria

* The exit status of xtrabackup is 0.

## Notes

* You might want to set the `xtrabackup --use-memory` option to
something similar to the size of your buffer pool, if you are on a dedicated
server that has enough free memory. More details [here](../xtrabackup_bin/xbk_option_reference.md).

* For a more detailed explanation, see [Creating a backup](../backup_scenarios/full_backup.md#creating-a-backup)
