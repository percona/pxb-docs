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

Some server features write new redo log record types. A Percona XtraBackup version that does not know the record type cannot back up a database that uses the feature.

| Server version | Feature | Minimum Percona XtraBackup version |
| -------------- | ------- | ---------------------------------- |
| Percona Server for MySQL 9.7.4-4 | Vector Search data type | 9.7.2-3 |

### Vector Search data type

Starting with Percona XtraBackup 9.7.2-3, Percona XtraBackup handles the Vector Search data type. Percona XtraBackup 9.7.2-3 or later is required to back up Percona Server for MySQL 9.7.4-4 databases that use Vector Search. [Insert whether Percona XtraBackup 9.7.2-3 backs up and prepares Vector Search data fully, or only fails safely]

Earlier Percona XtraBackup 9.7 versions cannot back up Vector Search data:

* If the database does not use Vector Search, the backup succeeds.

* If Percona XtraBackup reads the new record type in the redo log, the backup fails with exit code 1 and the following error message:

    ```text
    [Insert exact error message and the redo log record type that triggers the error]
    ```

    [Insert whether the backup fails on the first Vector Search redo log record or at the end of the backup]

* If a user creates a table with a Vector Search column while an earlier version runs a backup, [Insert the result].

To fix the failed backup, upgrade Percona XtraBackup to 9.7.2-3 or later and take the backup again.
