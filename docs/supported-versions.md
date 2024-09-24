# Supported versions

Percona XtraBackup 8.0.34-29 supports backing up databases compatible with server version 8.0.34 and later. Percona XtraBackup 8.0.34-29 can create backups of older server versions if specific conditions are met. This capability is useful for maintaining compatibility and ensuring backups can be performed across different server versions. You might need to override server version check and set specific options, such as `lock-ddl=ON`.

Specifically, Percona XtraBackup {{release}} supports taking backups of the following MySQL-compatible databases:

* Percona Server for MySQL 8.0.34, and MySQL 8.0.34

* Percona Server for MySQL 8.0.35, and MySQL 8.0.35

* Percona Server for MySQL 8.0.36 and MySQL 8.0.36 (and any later versions in the 8.0 series)

For more information, see [Percona XtraBackup Version Compatibility and Server Version Checks].

For details on the backup process, see [How XtraBackup Works].



[How XtraBackup Works]: how-xtrabackup-works.md

[Percona XtraBackup Version Compatibility and Server Version Checks]: server-backup-version-comparison.md
