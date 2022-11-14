# Make a Full Backup

Backup the InnoDB data and log files located in `/var/lib/mysql/` to
`/data/backups/mysql/` (destination). Then, prepare the backup files to be
ready to restore or use (make the data files consistent).

### Make a backup

```shell
$ xtrabackup --backup --target-dir=/data/backup/mysql/
```

### Prepare the backup

```shell
$ xtrabackup --prepare --target-dir=/data/backup/mysql/
```

!!! note
    
    Starting with [Percona Server for MySQL 8.0.30-22](release-notes/8.0/8.0.30-22.0.md) only run prepare once.

### Success Criteria

* The exit status of xtrabackup is 0.

!!! note
   
    You might want to set the `--use-memory` option to a value close to the size of your buffer pool, if you are on a dedicated server that has enough free memory. The [xtrabackup Option reference](https://docs.percona.com/percona-xtrabackup/latest/xtrabackup_bin/xbk_option_reference.html#xbk-option-reference) contains more details. 
    
    Review [Full Backups](https://docs.percona.com/percona-xtrabackup/latest/backup_scenarios/full_backup.html#creating-a-backup) for a more detailed explanation.


