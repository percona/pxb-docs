# Server version and backup version comparison

A MySQL change to a feature, such as the structure of a redo log
record, can cause older versions of Percona XtraBackup to fail. To
ensure that you can back up and restore your data, use a Percona
XtraBackup version that is equal to your source server major version. This means if you use Percona XtraBackup 8.1.x, you can safely back up the source server from 8.1.x to 8.1.xx.

!!! admonition "See also"
   
    [How XtraBackup works](how-xtrabackup-works.md)

The `--no-server-version-check` option performs the following test.
Before the backup starts, XtraBackup compares the source server version to
the Percona XtraBackup version. If the source server version is greater
than the XtraBackup major version, XtraBackup stops the backup and returns an
error message. This comparison prevents a failed backup or a corrupted
backup due to source server changes.

The parameter checks for the following scenarios:

* The source server and the PXB major version are the same, the backup proceeds

* The source server is greater than the PXB major version, and the parameter is not overridden, the backup is stopped and returns an error message

* The source server is less than the PXB major version, and the parameter is not overridden, the backup is stopped and returns an error message

* The source server is greater than the PXB major version up to the last release in the LTS series, and the parameter is overridden, the backup proceeds

Explicitly adding the `--no-server-version-check` parameter, like the
example, overrides the parameter and the backup proceeds.

```{.bash data-prompt="$"}
$ xtrabackup --backup --no-server-version-check --target-dir=$mysql/backup1
```

Overriding the `--no-server-version-check` parameter allows taking backups using a Percona XtraBackup version that is equal to a version of your source server up to the last release in the LTS series. This means if you use Percona XtraBackup 8.1.x, you can back up the source server from 8.1.x to 8.4.xx.

When you override the parameter, the following events can happen:

* Backup fails

* Creates a corrupted backup

* Backup successful
