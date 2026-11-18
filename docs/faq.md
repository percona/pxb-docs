# Frequently asked questions

## Does Percona XtraBackup {{vers}} support making backups of databases in versions prior to {{vers}}?

Percona XtraBackup {{vers}} does not support making backups of databases
created in versions prior to {{vers}} of MySQL, Percona Server for MySQL or
Percona XtraDB Cluster. 


## Are you aware of any web-based backup management tools (commercial or not) built around Percona XtraBackup?

[Percona Monitoring and Management (PMM) :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/3/backup/index.html) includes backup management for MySQL. PMM uses Percona XtraBackup to create on-demand and scheduled physical backups and to restore them from the PMM web interface.

For the required XtraBackup version and setup, see [MySQL backup prerequisites :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/3/backup/mysql-backup/mysql_prerequisites.html).

## xtrabackup binary fails with a floating point exception

In most of the cases this is due to not having installed the required
libraries (and version) by xtrabackup. Installing the GCC suite with the
supporting libraries and recompiling xtrabackup solves the issue. See
[Compiling and Installing from Source Code](compile-xtrabackup.md) for instructions on the
procedure.

## How xtrabackup handles the ibdata/ib_log files on restore if they aren’t in mysql datadir?

In case the `ibdata` and `ib_log` files are located in different
directories outside the datadir, you will have to put them in their
proper
place after the logs have been applied.

## Backup fails with Error 24: ‘Too many open files’

This usually happens when database being backed up contains large amount of
files and Percona XtraBackup can’t open all of them to create a
successful
backup. In order to avoid this error the operating system should be
configured
appropriately so that Percona XtraBackup can open all its files. On
Linux,
this can be done with the `ulimit` command for specific backup session or
by
editing the `/etc/security/limits.conf` to change it globally (NOTE:
the maximum possible value that can be set up is `1048576` which is a
hard-coded constant in the Linux kernel).

## How to deal with skipping of redo logs for DDL operations?

To prevent creating corrupted backups when running DDL operations,
Percona XtraBackup aborts if it detects that redo logging is disabled.
In this case, the following error is printed:

```{.text .no-copy}
[FATAL] InnoDB: An optimized (without redo logging) DDL operation has been performed. All modified pages may not have been flushed to the disk yet.
Percona XtraBackup will not be able to take a consistent backup. Retry the backup operation.
```

!!! note
   
    * Redo logging is disabled during a [sorted index build :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/sorted-index-builds.html). To avoid this error, Percona XtraBackup can use metadata locks on tables while they are copied:

    * To block all DDL operations, use the `--lock-ddl` option that issues `LOCK TABLES FOR BACKUP`.

## Backup fails on a Percona Server for MySQL 9.7.4-4 database that uses Vector Search

Percona XtraBackup versions earlier than 9.7.2-3 cannot create a backup of Vector Search data. If Percona XtraBackup reads the Vector Search record type in the redo log, the backup fails with exit code `2`. In this case, Percona XtraBackup prints the following error message:

```{.text .no-copy}
[ERROR] [MY-012519] [InnoDB] ############### CORRUPT LOG RECORD FOUND ###############
[Note] [MY-012520] [InnoDB] Log record type 62, page 4294967295:4294967295. Log parsing proceeded successfully up to 19604413.
[ERROR] [MY-014008] [InnoDB] [FATAL] Index log version 251 did not match. Max index version is 1. Recovery can't continue.
```

To fix the error, upgrade Percona XtraBackup to 9.7.2-3 or higher and take the backup again. For details, see [Minimum Percona XtraBackup version for server features](server-backup-version-comparison.md#minimum-percona-xtrabackup-version-for-server-features).

## Prepare fails on a Percona Server for MySQL 9.7.4-4 database that uses Vector Search

Percona XtraBackup versions earlier than 9.7.2-3 can create a backup of a table with a vector index. The `--prepare` step can then fail with exit code `2` in two cases:

* A transaction that changed the table was still open when the backup ended.

* You run `--prepare --export`.

In this case, Percona XtraBackup prints the following output:

```{.text .no-copy}
[Note] [MY-011825] [Xtrabackup] Time taken to build dictionary: ...
mysqld got signal 11 ;
 #1 ... dict_table_read_dynamic_metadata(...)
 #2 ... dict_table_load_dynamic_metadata(dict_table_t*)
```

To fix the error, upgrade Percona XtraBackup to 9.7.2-3 or higher and take the backup again. For details, see [Minimum Percona XtraBackup version for server features](server-backup-version-comparison.md#minimum-percona-xtrabackup-version-for-server-features).

## Import of an exported tablespace fails with a schema mismatch

Percona XtraBackup versions earlier than 9.7.2-3 write a wrong column type to the `.cfg` file for a `VECTOR` column. The `ALTER TABLE ... IMPORT TABLESPACE` statement then prints the following error:

```{.text .no-copy}
ERROR 1808 (HY000): Schema mismatch (Column v main type mismatch.)
```

To fix the error, upgrade Percona XtraBackup to 9.7.2-3 or higher. Then run `--prepare --export` again. For details, see [Minimum Percona XtraBackup version for server features](server-backup-version-comparison.md#minimum-percona-xtrabackup-version-for-server-features).
