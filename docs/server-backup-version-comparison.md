# Server version and backup version comparison

A MySQL change to a feature, such as the structure of a redo log
record, can cause older versions of Percona XtraBackup to fail. To
ensure that you can back up and restore your data, use a Percona
XtraBackup version that is equal to your source server major version. This means if you use Percona XtraBackup {{vers}}.x, you can safely back up the source server from {{vers}}.x to {{vers}}.xx.

Some server features require a minimum Percona XtraBackup patch version. See [Minimum Percona XtraBackup version for server features](#minimum-percona-xtrabackup-version-for-server-features).

!!! admonition "See also"
   
    [How XtraBackup works](how-xtrabackup-works.md)

The `--no-server-version-check` option performs the following test.
Before the backup/prepare starts, XtraBackup compares the source server version to
the Percona XtraBackup version. If the source server version is greater
than the XtraBackup major version, XtraBackup stops the backup and returns an
error message. This comparison prevents a failed backup or a corrupted
backup due to source server changes.

The parameter checks for the following scenarios:

* The source server and the PXB major version are the same, the backup proceeds

* The source server is greater than the PXB major version, and the parameter is not overridden, the backup is stopped and returns an error message

* The source server is less than the PXB major version, and the parameter is not overridden, the backup is stopped, and returns an error message

* The source server is greater than the PXB major version up to the last release in the LTS series, and the parameter is overridden, the backup proceeds

Explicitly adding the `--no-server-version-check` parameter, like the
example, overrides the parameter and the backup proceeds.

```shell
xtrabackup --backup --no-server-version-check --target-dir=$mysql/backup1
```

Overriding the `--no-server-version-check` parameter allows taking backups using a Percona XtraBackup version that is equal to a version of your source server up to the last release in the LTS series. This means if you use Percona XtraBackup {{vers}}.x, you can back up the source server from {{vers}}.x to 9.7.xx.

When you override the parameter, the following events can happen:

* Backup fails

* Creates a corrupted backup

* Backup successful

## Minimum Percona XtraBackup version for server features

Some server features add redo log record types. A Percona XtraBackup version without support for the record type cannot create a backup of a database with the feature.

| Server version | Feature | Minimum Percona XtraBackup version |
| -------------- | ------- | ---------------------------------- |
| Percona Server for MySQL 9.7.4-4 | Vector Search data type | 9.7.2-3 |

### Vector Search data type

Starting with Percona XtraBackup 9.7.2-3, Percona XtraBackup handles the Vector Search data type. A backup of a Percona Server for MySQL 9.7.4-4 database with Vector Search requires Percona XtraBackup 9.7.2-3 or higher. Percona XtraBackup 9.7.2-3 fully supports the backup, prepare, and restore steps for Vector Search data. Support includes `--prepare --export` and the import of exported tablespaces.

Earlier Percona XtraBackup 9.7 versions cannot create a backup of Vector Search data:

* If the database has no table with a vector index, the backup and prepare succeed. The same result applies to tables with a `VECTOR` column and no vector index. The import of an exported tablespace is an exception.

* If Percona XtraBackup reads a Vector Search redo log record, the backup fails with exit code `2`. Percona XtraBackup prints the following error message:

    ```text
    [ERROR] [MY-012519] [InnoDB] ############### CORRUPT LOG RECORD FOUND ###############
    [Note] [MY-012520] [InnoDB] Log record type 62, page 4294967295:4294967295. Log parsing proceeded successfully up to 19604413.
    [ERROR] [MY-014008] [InnoDB] [FATAL] Index log version 251 did not match. Max index version is 1. Recovery can't continue.
    ```

    The record type is `MLOG_TABLE_DYNAMIC_META` (log record type 62). The LSN and the index log version number in the message vary.

    The backup fails on the first Vector Search redo log record that Percona XtraBackup parses. The backup does not wait for the end.

* A user can create a table with a vector index during a backup by an earlier version. The result depends on the table data:

    * If the user inserts no rows, the backup, prepare, and restore succeed.

    * If the user inserts rows, the backup fails with the error in the previous item.

* If the backup succeeds, `--prepare` can still fail on a table with a vector index. The failure occurs in two cases:

    * A transaction that changed the table, such as a `DELETE`, was still open when the backup ended. The `--prepare` step rolls back this transaction.

    * You run `--prepare --export`.

    In both cases, `xtrabackup --prepare` crashes with signal 11 and exit code `2`. The stack trace includes `dict_table_read_dynamic_metadata`. The saved table metadata holds a value that the earlier version cannot read.

* If you run `--prepare --export` on a table with a `VECTOR` column, the export succeeds. The earlier version writes a wrong column type to the `.cfg` file. The `ALTER TABLE ... IMPORT TABLESPACE` statement then fails with the following error:

    ```text
    ERROR 1808 (HY000): Schema mismatch (Column v main type mismatch.)
    ```

To fix these failures, upgrade Percona XtraBackup to 9.7.2-3 or higher. Then take the backup again. For the import failure, run `--prepare --export` again.
