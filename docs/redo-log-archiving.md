# InnoDB redo log archiving

A physical backup contains raw copies of the database contents and any related files, such as configuration files or logs. During crash recovery, InnoDB corrects the data from incomplete transactions using the redo log. A redo log contains the entries necessary to bring the database back to a consistent state. An LSN value represents the data in the redo log.

Data in the redo log is always appended, and the movement of the checkpoint truncates old data. When a file is full, a new file is created and the movement of the checkpoint truncates the old files.
If the MySQL server has significant activity during a backup operation and the redo log file storage media operates faster than the backup storage media, the backup operation may fail to keep pace with the redo log generation and cause data loss.

Before the redo log archiving feature, the solutions were:

* Increasing the redo log size

* Checking for I/O congestion if the read speed is slow

* Checking for I/O or network congestion if the write speed is slow

* Taking the backup at an off-peak time

## redo log archiving

MySQL 8.0.17 added redo log archiving. To enable this feature, the following actions are required:

* Create a directory for the archiving logs

* Call the function to start the archiving process

It would help if you created a directory for the redo log archives. The system user running `mysqld` must have access to this directory.

You can verify if MySQL has configured the archive directory with the following command. The result provides the path or returns NULL, meaning you have not set the archiving directory.

```{.bash data-prompt"}
$ mkdir -p /var/lib/mysql-redo-archive/backup1
$ chown mysql. -R /var/lib/mysql-redo-archive
$ chmod _R 700 /var/lib/mysql-redo-archive/
```

The `innodb_redo_log_archive_dirs` global variable contains labeled directories. The format is `label:directory-path`. Multiple objects can be listed with a semi-colon between each set.

```{.bash data-prompt="mysql>"}
mysql> SET PERSIST innodb_redo_log_archive_dirs='backup1:/var/lib/mysql-redo-archive/';
```

Verify that the archive was created with the following command:

```{.bash data-prompt="mysql>"}
mysql> SHOW GLOBAL VARIABLES LIKE 'innodb_redo_log_ar%';
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

Users with the [INNODB_REDO_LOG_ARCHIVE] privilege can call the `innodb_redo_log_archive_start()` or `innodb_redo_log_archive_stop()` functions. to either start or stop archiving. 

```{.bash data-prompt="mysql>"}
mysql> SELECT innodb_redo_log_archive_start('backup1','backup1');
```

??? example "Expected output"
    ```{.text .no-copy}
    +-----------------------------------------------------+
    | innodb_redo_log_archive_start('backup1','backup1')  |
    +------------------------------+----------------------+
    |                                                   0 |
    +------------------- ---------------------------------+
    1 row in set (0.00225 sec)
    ```

## Percona XtraBackup and redo log archiving

Percona XtraBackup 8.0.34-29 added the [redo-log-arch-dir](xtrabackup-option-reference.md#-redo-log-arch-dirname) option. If the archiving directory is not configured in MySQL, Percona XtraBackup creates a temporary directory for the archive file. To use this option, you must run Percona XtraBackup as the same owner as `mysqld`. If Percona XtraBackup does not have the appropriate permissions, the action generates a "Permission denied" error, and archiving is not used.

## Example of reading a log

```{.bash data-prompt}
$ sudo -H -u mysql bash
$ xtrabackup --no-lock=1 --compress --parallel=4 --host=localhost --user=root --password='password_string' --backup=1 --target-dir=/Backup/13oct 2> /tmp/b0-with-redo-archiving-as-mysql-os-user.log
```

Verify that the archiving is used:

```{.bash data-prompt}
$ cat /tmp/b0-with-redo-archiving-as-mysql-os-user.log
```

??? example "Expected output"
    ```{.text .no-copy}
    [Note] [MY-011825] [Xtrabackup] recognized server arguments: --datadir=/var/lib/mysql  
    [Note] [MY-011825] [Xtrabackup] recognized client arguments: --no-lock=1 --compress --parallel=4 --host=localhost --user=root --password=* --backup=1 --target-dir=/Backup/22Aug  xtrabackup version 8.0.34-29 based on MySQL server 8.0.34 Linux (x86_64) (revision id: 5ba706ee) 230822 13:36:02  version_check Connecting to MySQL server with DSN 'dbi:mysql:;mysql_read_default_group=xtrabackup;host=localhost' as 'root'  (using password: YES). 230822 13:36:02  version_check Connected to MySQL server 230822 13:36:02  version_check Executing a version check against the server... 230822 13:36:02  version_check Done. 
    [Note] [MY-011825] [Xtrabackup] Connecting to MySQL server host: localhost, user: root, password: set, port: not set, socket: not set 
    [Note] [MY-011825] [Xtrabackup] Using server version 8.0.34 
    .... 
    .... 
    [Note] [MY-011825] [Xtrabackup] Connecting to MySQL server host: localhost, user: root, password: set, port: not set, socket: not set 
    [Note] [MY-011825] [Xtrabackup] xtrabackup redo_log_arch_dir is set to backup1:/var/lib/mysql-redo-archive/ 
    [Note] [MY-011825] [Xtrabackup] Waiting for archive file '/var/lib/mysql-redo-archive//1692711362986/archive.94f4ab58-3d1c-11ee-9e4f-0af1fd7c44c9.000001.log' 
    [Note] [MY-011825] [Xtrabackup] >> log scanned up to (19630018) 
    .... 
    .... 
    [Note] [MY-011825] [Xtrabackup] Done: Compressing file /Backup/22Aug/xtrabackup_info.zst 
    [Note] [MY-011825] [Xtrabackup] Transaction log of lsn (19630018) to (19630028) was copied. 
    [Note] [MY-011825] [Xtrabackup] completed OK!
    ```



[INNODB_REDO_LOG_ARCHIVE]: https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_innodb-redo-log-archive