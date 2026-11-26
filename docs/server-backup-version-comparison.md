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
| Percona Server for MySQL 9.7.4-4 | Vector index | 9.7.2-3 |

### Vector index

Percona Server for MySQL 9.7.4-4 adds the vector (HNSW) index. Starting with Percona XtraBackup 9.7.2-3, Percona XtraBackup handles vector indexes. To back up a Percona Server for MySQL 9.7.4-4 database with vector indexes, use Percona XtraBackup 9.7.2-3 or higher.

The `VECTOR` data type is available in all Percona Server for MySQL 9.7 releases. Percona XtraBackup backs up and restores tables with `VECTOR` columns and no vector index.

The export and import of tablespaces depend on the table:

* For a table with `VECTOR` columns and no vector index, `--prepare --export` and the import of the exported tablespace work starting with Percona XtraBackup 9.7.2-3.

* For a table with a vector index, `--prepare --export` succeeds and creates the `.cfg` file. You cannot import the tablespace because vector index support is at the minimum viable product (MVP) stage.

!!! warning

    If the server has vector indexes, do not trust backups taken with Percona XtraBackup 9.7.2-2. These backups are invalid. The backup and prepare steps can still succeed. To get a valid backup, upgrade Percona XtraBackup to 9.7.2-3 or higher and take the backup again.
