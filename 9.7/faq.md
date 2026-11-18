> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-xtrabackup/9.7/llms.txt).

# Frequently asked questions

## Does Percona XtraBackup 9.7 support making backups of databases in versions prior to 9.7?

Percona XtraBackup 9.7 does not support making backups of databases created in versions prior to 9.7 of MySQL, Percona Server for MySQL or Percona XtraDB Cluster.

## Are you aware of any web-based backup management tools (commercial or not) built around Percona XtraBackup?

[Percona Monitoring and Management (PMM)](https://docs.percona.com/percona-monitoring-and-management/3/backup/index.html) includes backup management for MySQL. PMM uses Percona XtraBackup to create on-demand and scheduled physical backups and to restore them from the PMM web interface.

For the required XtraBackup version and setup, see [MySQL backup prerequisites](https://docs.percona.com/percona-monitoring-and-management/3/backup/mysql-backup/mysql_prerequisites.html) .

## xtrabackup binary fails with a floating point exception

In most of the cases this is due to not having installed the required libraries (and version) by xtrabackup. Installing the GCC suite with the supporting libraries and recompiling xtrabackup solves the issue. See [Compiling and Installing from Source Code](https://docs.percona.com/percona-xtrabackup/9.7/compile-xtrabackup.html) for instructions on the procedure.

## How xtrabackup handles the ibdata/ib_log files on restore if they aren’t in mysql datadir?

In case the `ibdata` and `ib_log` files are located in different directories outside the datadir, you will have to put them in their proper place after the logs have been applied.

## Backup fails with Error 24: ‘Too many open files’

This usually happens when database being backed up contains large amount of files and Percona XtraBackup can’t open all of them to create a successful backup. In order to avoid this error the operating system should be configured appropriately so that Percona XtraBackup can open all its files. On Linux, this can be done with the `ulimit` command for specific backup session or by editing the `/etc/security/limits.conf` to change it globally (NOTE: the maximum possible value that can be set up is `1048576` which is a hard-coded constant in the Linux kernel).

## How to deal with skipping of redo logs for DDL operations?

To prevent creating corrupted backups when running DDL operations, Percona XtraBackup aborts if it detects that redo logging is disabled. In this case, the following error is printed:

```
[FATAL] InnoDB: An optimized (without redo logging) DDL operation has been performed. All modified pages may not have been flushed to the disk yet.
Percona XtraBackup will not be able to take a consistent backup. Retry the backup operation.
```

Note

- Redo logging is disabled during a [sorted index build](https://dev.mysql.com/doc/refman/9.7/en/sorted-index-builds.html) . To avoid this error, Percona XtraBackup can use metadata locks on tables while they are copied:
- To block all DDL operations, use the `--lock-ddl` option that issues `LOCK TABLES FOR BACKUP`.
