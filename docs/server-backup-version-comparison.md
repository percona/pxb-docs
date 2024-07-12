# Server version and backup version comparison

When the server undergoes internal changes, such as modifying the structure of the redo log records, older versions of Percona XtraBackup may either fail or produce corrupted backups. To prevent these issues, XtraBackup checks the version of the source system before starting the backup and compares it to the Percona XtraBackup version.

Here are the possible scenarios and the actions taken:

| Scenario                                                                                  | Actions Taken                                                                                                                                            |
|----|----|
| Server version is the same as Percona XtraBackup version                                  | The backup process continues without any issues. This is the ideal scenario because both the server and the backup tool are fully compatible.         |
| Server version is older than Percona XtraBackup version                                  | The backup process continues without any issues. Percona XtraBackup is designed to handle older versions of the server without problems.             |
| Server version is newer than Percona XtraBackup version                                  | The backup process stops with an error unless you explicitly override the version check. This happens because the backup tool may not support new features or changes introduced in the newer server version. |
| Server version is newer than Percona XtraBackup version, and the version check is overridden | The backup process continues, but there is a risk of failure or corruption. Overriding the version check can be risky because the backup tool might not be able to handle new features or changes correctly. |

Until version 8.0.34, to ensure successful backups and restores, it is recommended to use a Percona XtraBackup version that matches or is newer than your server version. However, version 8.0.34 can back up newer server versions and older server versions if you set the `lock-ddl=ON` option.

## Version updates

Percona XtraBackup 8.0.34: disabled the server-version-check.

Percona XtraBackup 8.0.22-15: introduced `--no-server-version-check`. This option allows you to override the version comparison process. This option is off by default, meaning the comparison occurs unless explicitly overridden.

### Override Server Version check

You can add the `--no-server-version-check` option to your backup command to override the server version check and proceed with the backup. Here’s an example of how to use this option:

```{.bash data-prompt="$"}
$ xtrabackup --backup --no-server-version-check --target-dir=$mysql/backup1
```

## Additional resources

For more details, refer to the documentation on [How XtraBackup Works].

For more information, refer to [Supported versions].

[How XtraBackup Works]: how-xtrabackup-works.md

[Supported versions]: supported-versions.md