# Server version and backup version comparison

A MySQL change to a feature, for example, changing the redo log
record structure, can cause older versions of Percona XtraBackup to fail. To
ensure that you can back up and restore your data, use a Percona
XtraBackup version that is equal to or above your source server version.

!!! admonition "See also"
   
    [How XtraBackup works](how-xtrabackup-works.md)

## Version changes

With the release of Percona XtraBackup 8.0.34-29, Percona XtraBackup allows backups on version 8.0.35 and higher. 

Percona XtraBackup 8.0.21 adds the `--no-server-version-check` option.

## Version check

Before the backup starts, XtraBackup compares the source system version to
the Percona XtraBackup version. If the source system version is greater than the XtraBackup version, XtraBackup stops the backup and returns an
error message. This comparison prevents a failed or corrupted
backup due to source system changes.

The parameter checks for the following scenarios:

* The source system and the Percona XtraBackup version are the same; the backup proceeds

* The source system is less than the Percona XtraBackup version, the backup proceeds

* The source system is greater than the Percona XtraBackup version, and the parameter is not overridden; the backup is stopped and returns an error message

* The source system is greater than the Percona XtraBackup version, and the parameter is  overridden; the backup proceeds


### Override check

Explicitly adding the `--no-server-version-check` option overrides the parameter, and the backup proceeds.

```{.bash data-prompt="$"}
$ xtrabackup --backup --no-server-version-check --target-dir=$mysql/backup1
```

Using this option may cause the following events:

* Backup fails

* Creates a corrupted backup

* Backup successful
