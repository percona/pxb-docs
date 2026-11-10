# Server version and backup version comparison

A MySQL change to a feature, such as the structure of a redo log
record, can cause older versions of Percona XtraBackup to fail. To
ensure that you can back up and restore your data, use a Percona
XtraBackup version that is equal to your source server major version. This means if you use Percona XtraBackup {{vers}}.x, you can safely back up the source server from {{vers}}.x to {{vers}}.xx.

!!! admonition "See also"
   
    [How XtraBackup works](how-xtrabackup-works.md)

## The `--no-server-version-check` option

The `--no-server-version-check` option has no effect in Percona XtraBackup {{vers}}. XtraBackup accepts the option. The backup result is the same with or without the option.

To back up the source server, use a Percona XtraBackup version that matches the source server major version.
