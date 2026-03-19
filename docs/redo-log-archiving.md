# InnoDB Redo Log Archiving

<!-- Varify the instruction for 9.7 version-->

A physical backup includes raw copies of database contents and related files, such as configuration files and logs. During crash recovery, InnoDB uses the redo log to correct data from incomplete transactions. The redo log contains entries that restore the database to a consistent state. An LSN value identifies the position of data in the redo log.

InnoDB continuously appends data to the redo log. When a file fills, InnoDB creates a new file. The checkpoint process truncates old data and removes obsolete files.

If the server generates redo logs faster than the backup system can store them, the backup may fall behind and risk data loss. This can happen when the server is under heavy load or when the backup storage is slower than the redo log storage.

## Pre-archiving strategies

Before redo log archiving, users relied on the following strategies:

* Increase the redo log size

* Check for I/O congestion if read speed is slow

* Check for I/O or network congestion if write speed is slow

* Schedule backups during off-peak hours

## When to Use Redo Log Archiving

Use redo log archiving when:

* You see heavy write activity during backups.

* Increasing redo log size alone does not prevent wrap-around during long backups.

* I/O congestion slows read or write throughput to the backup target.

* You cannot schedule backups during low-traffic periods.


## Enable redo log archiving

Redo log archiving allows the server to write redo logs to a separate directory for backup purposes. To enable archiving, follow these steps:

1. Create one or more archive directories and set ownership and permissions so the `mysqld` OS user can write to them.

2. Register those directories with the `innodb_redo_log_archive_dirs` global variable, then start archiving with the `innodb_redo_log_archive_start()` function.

### Create an archive directory

Before enabling redo log archiving, create a directory to store archived redo logs. The system user running `mysqld` must own the directory and have read and write access.

Use the following commands to create and secure the directory:

```shell
sudo mkdir -p /var/lib/mysql-redo-archive/backup1
sudo chown -R mysql:mysql /var/lib/mysql-redo-archive
sudo chmod -R 700 /var/lib/mysql-redo-archive/
```

* `mkdir -p` creates the directory and any missing parent directories

* `chown` assigns ownership to the mysql user

* `chmod` restricts access to the owner only

Ensure that the path you use matches the label and directory in your `innodb_redo_log_archive_dirs` configuration.

Adjust `mysql:mysql` if your MySQL server runs under a different user or group.

### Register the Archive Directory

The `innodb_redo_log_archive_dirs` variable defines labeled archive paths. Use a semicolon to separate multiple entries. Each entry uses the format `label:/path/to/archive`.

Set and persist the variable:

```sql
SET PERSIST innodb_redo_log_archive_dirs='backup1:/var/lib/mysql-redo-archive/';
```

Verify the configuration:

```sql
SHOW GLOBAL VARIABLES LIKE 'innodb_redo_log_ar%';
```

??? example "Expected output"
    ```{.text .no-copy}
    +------------------------------+--------------------------------------+
    | Variable_name                | Value                                |
    +------------------------------+--------------------------------------+
    | innodb_redo_log_archive_dirs | backup1:/var/lib/mysql-redo-archive/ |
    +------------------------------+--------------------------------------+
    1 row in set (0.0025 sec)
    ```

## Start and stop archiving

Users with the `INNODB_REDO_LOG_ARCHIVE` privilege can start or stop archiving with the following functions:

* `innodb_redo_log_archive_start(label, label)`

* `innodb_redo_log_archive_stop(label)`

### Start archiving

To begin archiving redo logs, call `innodb_redo_log_archive_start()`. This function activates the archiving process for the specified label and writes redo log data to the associated directory.

Use the same label defined in the `innodb_redo_log_archive_dirs` variable. The function requires the `INNODB_REDO_LOG_ARCHIVE` privilege.

```sql
SELECT innodb_redo_log_archive_start('backup1','backup1');
```

* The first argument is the label used in the configuration

* The second argument is the destination label for the archive stream

If successful, the function returns `0`. A non-zero value indicates an error.

### Stop archiving

To stop redo log archiving, call `innodb_redo_log_archive_stop()`. This function halts the archiving process for the specified label and closes the associated archive stream.

You must use the same label as when you started archiving. The function requires the `INNODB_REDO_LOG_ARCHIVE` privilege.

```sql
SELECT innodb_redo_log_archive_stop('backup1');
```

* The argument is the label defined in the archive configuration

If successful, the function returns `0`. A non-zero value indicates an error.

## Troubleshooting redo log archiving

If redo log archiving fails or behaves unexpectedly, check the following:

* Confirm that the archive directory exists and is writable by the `mysqld` user

* Verify that the label matches the one defined in `innodb_redo_log_archive_dirs`

* Ensure that the user calling the function has the `INNODB_REDO_LOG_ARCHIVE` privilege

* Check for SELinux or AppArmor restrictions that may block access to the archive path

* Review the MySQL error log for messages related to archiving failures

* If using Percona XtraBackup, run it as the same user that owns the mysqld process

* Look for "Permission denied" errors in the backup log output

The archiving functions return `0` on success. Any other value indicates a failure that requires investigation.

## Run Percona XtraBackup with archiving

Percona XtraBackup supports redo log archiving. If the archive directory is not configured, XtraBackup creates a temporary directory. Run XtraBackup as the same user that owns the mysqld process. If permissions are incorrect, XtraBackup returns a "Permission denied" error and skips archiving.

Run XtraBackup as the mysql user:

```shell
sudo -H -u mysql bash
xtrabackup --no-lock=1 --compress --parallel=4 \
  --host=localhost --user=root --password='password_string' \
  --backup=1 --target-dir=/Backup/13oct \
  2> /tmp/b0-with-redo-archiving-as-mysql-os-user.log
```

Use the following command to verify that archiving has occurred:

```shell
cat /tmp/b0-with-redo-archiving-as-mysql-os-user.log
```

??? example "Expected output"
    ```{.text .no-copy}
    [Note] [MY-011825] [Xtrabackup] recognized server arguments: --datadir=/var/lib/mysql
    [Note] [MY-011825] [Xtrabackup] recognized client arguments: --no-lock=1 --compress --parallel=4 --host=localhost --user=root --password=* --backup=1 --target-dir=/Backup/22Aug  xtrabackup version 8.4.0-3 based on MySQL server 8.4.0-3 Linux (aarch64) (revision id: cccec763) 250721 13:36:02  version_check Connecting to MySQL server with DSN 'dbi:mysql:;mysql_read_default_group=xtrabackup;host=localhost' as 'root'  (using password: YES). 250721 13:36:02  version_check Connected to MySQL server 250721 13:36:02  version_check Executing a version check against the server... 250721 13:36:02  version_check Done. 
       [Note] [MY-011825] [Xtrabackup] Connecting to MySQL server host: localhost, user: root, password: set, port: not set, socket: not set 
       [Note] [MY-011825] [Xtrabackup] Using server version 8.4.0-3 
    ...
    [Note] [MY-011825] [Xtrabackup] xtrabackup redo_log_arch_dir is set to 
    backup1:/var/lib/mysql-redo-archive/  
    [Note] [MY-011825] [Xtrabackup] Waiting for archive file 
    '/var/lib/mysql-redo-archive//1692711362986/archive.94f4ab58-3d1c-11ee-9e4f-0af1fd7c44c9.000001.log'  
    [Note] [MY-011825] [Xtrabackup] >> log scanned up to (19630018)
    ...
    ```

Look for messages confirming the use of the archive directory and successful log scanning.

