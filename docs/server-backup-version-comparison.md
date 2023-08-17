<!--- will this be in 8.1?
 --->

# Server version and backup version comparison

A MySQL change to a feature, such as the structure of a redo log
record, can cause older versions of Percona XtraBackup to fail. To
ensure that you can back up and restore your data, use a Percona
XtraBackup version that is equal to or above your source server version.

!!! admonition "See also"
   
    [How XtraBackup works](how-xtrabackup-works.md)

The `--no-server-version-check` option performs the following test.
Before the backup starts, XtraBackup compares the source system version to
the Percona XtraBackup version. If the source system version is greater
than the XtraBackup version, XtraBackup stops the backup and returns an
error message. This comparison prevents a failed backup or a corrupted
backup due to source system changes.

The parameter checks for the following scenarios:

* The source system and the PXB version are the same, the backup proceeds

* The source system is less than the PXB version, the backup proceeds

* The source system is greater than the PXB version, and the parameter is not overridden, the backup is stopped and returns an error message

* The source system is greater than the PXB version, and the parameter is  overridden, the backup proceeds

Explicitly adding the `--no-server-version-check` parameter, like the
example, overrides the parameter and the backup proceeds.

```{.bash data-prompt="$"}
$ xtrabackup --backup --no-server-version-check --target-dir=$mysql/backup1
```

When you override the parameter, the following events can happen:

* Backup fails

* Creates a corrupted backup

* Backup successful
