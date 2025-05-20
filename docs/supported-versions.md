# Supported versions

Percona XtraBackup {{release}} supports backing up databases compatible with server version 8.0.34 and later. Percona XtraBackup {{release}} can create backups of older server versions when you override the server version check and enable specific options, such as `lock-ddl=ON`. This flexibility helps you maintain compatibility and perform backups across mixed-version environments.

Percona XtraBackup {{release}} supports taking backups of the following MySQL-compatible databases:

* Percona Server for MySQL 8.0.34, and MySQL 8.0.34

* Percona Server for MySQL 8.0.35, and MySQL 8.0.35

* Percona Server for MySQL 8.0.36 and MySQL 8.0.36 and any later 8.0.x release

For more information, see [Percona XtraBackup Version Compatibility and Server Version Checks].

[For details on the backup process, see How XtraBackup Works.]



[For details on the backup process, see How XtraBackup Works.]: how-xtrabackup-works.md

[Percona XtraBackup Version Compatibility and Server Version Checks]: server-backup-version-comparison.md
