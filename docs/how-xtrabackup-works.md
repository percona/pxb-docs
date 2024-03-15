# How Percona XtraBackup works

Percona XtraBackup is based on InnoDB’s crash-recovery functionality.
`xtrabackup` copies your InnoDB data files, resulting in internally inconsistent data, and performs crash recovery on the files to make them a consistent, usable database again. This operation works because InnoDB maintains a redo log called the transaction log. This log contains a record of every change to the InnoDB data. 

When InnoDB starts, `xtrabackup` inspects the data files and the transaction log and does the following:

* Applies committed transaction log entries to the data files

* Removes uncommitted transactions - any change made within those transactions is discarded

`xtrabackup` reads undo log records and rollbacks the uncommitted transaction changes.

## Version changes

[Percona XtraBackup 8.0.30-23](release-notes/8.0/8.0.30-23.0.md) adds 
the [--register-redo-log-consumer] parameter. This parameter is 
disabled by default. When enabled, the parameter lets Percona XtraBackup 
register as a redo log consumer at the start of the backup. The server 
does not remove a redo log that Percona XtraBackup (the consumer) 
has not yet copied. The consumer reads the redo log and manually advances the log sequence number (LSN). The server blocks the writes during the process. The server determines when to purge the log based on the redo log consumption.

## Privileges and permissions

The `BACKUP_ADMIN` privilege is required to execute the `LOCK INSTANCE FOR BACKUP` statement. This privilege manages database backups, ensures data consistency, and performs backup-related tasks.

You must have the necessary [permissions and privileges] to open files. 

## XtraBackup process

Percona XtraBackup works by remembering the LSN when it starts and then 
copying away the data files. It takes some time to do this, so if the files change, they reflect the state of the database at different points. At the same time, Percona XtraBackup runs a background process that watches the transaction log files and copies changes from them. Percona XtraBackup does this continually because the transaction logs are written round-robin and can be reused. Percona XtraBackup needs the transaction log record for every change to the data files since it started.

Percona XtraBackup copies the InnoDB data files. A backup of Percona Server for MySQL copies non-InnoDB tables and any other database files. 

The `xtrabackup` binary backs up the following file types:

* .FRM

* .IBD

* .IBU

* .MRG

* .MYD

* .MYI

* .CSM

* .CSV

* .SDI

* .PAR 

## Locks

Locks are used in a backup to ensure data consistency. Only DDL operations are blocked.

Percona XtraBackup uses `LOCK INSTANCE FOR BACKUP` to take a backup log for the entire process, including InnoDB and non-InnoDB data. The `xtrabackup` binary copies the InnoDB data and then copies the MyISAM tables and files. 

Both `LOCK TABLES FOR BACKUP` and `LOCK INSTANCE FOR BACKUP` are methods used in Percona XtraBackup to ensure data consistency during backups, but they differ in their approach and impact:

### LOCK TABLES FOR BACKUP (Traditional Method)

* **Availability:** Available in MySQL 5.1 and above, but not recommended in newer versions due to limitations.
* **Locking Mechanism:** Creates a global Metadata Lock (MDL) that blocks all Data Definition Language (DDL) statements and updates to specific table types like MyISAM, CSV, MEMORY, ARCHIVE, TokuDB, and MyRocks.
* **Impact:** This lock can significantly impact performance as it prevents any modifications to the locked tables. Connections trying to modify these tables will wait until the backup finishes. `LOCK TABLES FOR BACKUP` also blocks DML operations on MyISAM tables.
* **Use Case:** Primarily used with older MySQL versions where `LOCK INSTANCE FOR BACKUP` isn't available.

### LOCK INSTANCE FOR BACKUP (Modern Method)

* **Availability:** Introduced in MySQL 8.0 and available with Percona Server for MySQL 5.6 or later.
* **Locking Mechanism:** Creates a lightweight instance-level lock that restricts writes (updates) but allows reads to continue.
* **Impact:** Performance impact is minimal as reads are still allowed. This is a more favorable option for production environments.
* **Use Case:** Preferred method for backups in MySQL 8.0 and newer or with Percona Server for MySQL 5.6 or later due to its minimal performance impact.


### LOCK INSTANCE FOR BACKUP

The `LOCK INSTANCE FOR BACKUP` statement is a feature introduced in MySQL 8.0 that allows you to acquire an instance-level backup lock. Executing the `LOCK INSTANCE FOR BACKUP` statement prevents any other session from doing DDL at the instance level.

The "Lock Instance for Backup" procedure in Percona XtraBackup involves locking the MySQL instance to ensure a consistent state during the backup process. Here's an overview of the steps involved in this procedure:

Prepare the Environment: Before initiating the backup, ensure the environment is configured correctly and meets the requirements for running Percona XtraBackup. This preparation includes having the necessary permissions and access to the MySQL instance. 
XtraBackup takes a backup lock to ensure files are not added or removed and copies all the files in the directory.

Start Backup: Initiate the backup process using Percona XtraBackup. When using the "Lock Instance for Backup" method, `xtrabackup` automatically locks the MySQL instance to prevent DDL changes to the database while the backup is in progress.

`xtrabackup` starts copying a redo log operation. The redo log contains transactions that have not yet been written in the data files. This operation ensures that changes recorded in the redo log are safely included in the backup, allowing for consistent data recovery during the [`prepare`] phase.

Transaction Logs: Percona XtraBackup also copies transaction logs to capture any changes that occur during the backup process. These logs are essential for ensuring that the backup reflects a consistent state of the database at a specific time.

In MySQL, after the InnoDB data files are copied, then xtrabackup executes a `FLUSH TABLES WITH READ LOCK`, which closes all table objects and makes the server temporarily read-only. Then non-InnoDB tables, and any other database files are copied. At that point, the `FLUSH TABLES WITH READ LOCK` is released.

After the file copy process completes, `xtrabackup` queries the Performance_Schema.log_status table for the following data to make the backup consistent across storage engines:

### Locking the binary log

The `performance_schema.log_status` table in MySQL is a valuable resource for backups. This table provides critical information that allows a backup tool to copy necessary log files without locking the resources for the duration of the copy process.

When queried, the `log_status` table causes the server to momentarily block logging and related administrative changes to populate the table 
with data, and then the server releases the resources. This table identifies the point in the 
source's binary log and `gtid_executed` record the backup should copy, including the relay log for each replication channel. Additionally, it offers essential details, such as the last log sequence number (LSN) and the LSN of the previous checkpoint for InnoDB.

Percona XtraBackup ensures a consistent position across all logs, which is crucial for maintaining data integrity during backups. This consistency is important when dealing with multiple storage engines, as the consistent position allows for accurate point-in-time recovery and seamless replication setup.

The tool achieves this by integrating with the log_status table, which lets it print out the backup's corresponding binary log position. This position can then be used to provision a new replica or perform point-in-time recovery, ensuring that the backup aligns perfectly with the binary log sequence. The `xtrabackup_binlog_info` file, created in the target directory, contains the binary log file name and position, providing a reliable reference for database administrators to manage backup and recovery processes effectively.

The file has the following information:

* checkpoint_lsn - the position in the redo log where a checkpoint occurred

* write_lsn - the last log sequence number (LSN) written to the redo log

* binlog position - the position in the binary log (binlog) files

During the backup process, `xtrabackup` must ensure it captures a consistent database state without interfering with its operation. To achieve this, it copies the redo log files, which record all changes to the database. The `write_lsn`, or write log sequence number, is a crucial checkpoint in this process. This checkpoint represents the exact point at which the data has been written in the database and thus must be included in the backup.

`xtrabackup` writes the binlog information and the global transaction identifier (GTID) into the xtrabackup_binlog_info file. For information on how you can use a GTID-based replica, see [create a GTID-based replica].

At this point, `xtrabackup` releases the backup lock. Once the backup process is complete, Percona XtraBackup releases the locks on the MySQL instance, allowing  DDL operations to resume. The backup files should be prepare in the specified backup directory and then used the copy-back or move-back operation to restore.


### PS_log_status

One feature in Percona XtraBackup is the `PS_log_status` command. This command helps monitor the status of the Percona XtraBackup process, providing helpful information about the backup operation.

Using the `PS_log_status` command helps you monitor and troubleshoot the backup process. By logging the status, you can:

* Ensure the backup is progressing as expected.

* Identify and resolve any issues quickly.

* Keep a record of backup operations for auditing purposes.

#### What is Percona XtraBackup PS_log_status?

The `PS_log_status` command in Percona XtraBackup is used to log the status of the backup process. This status includes various details about the backup, such as the progress of the backup, any issues encountered, and other relevant information.

#### How to Use PS_log_status

When you run a backup using Percona XtraBackup, you can include the `--log-status` option followed by the file name where you want to save the log. This log file will contain detailed information about the backup process.

#### Example Command

Here is an example command to run a backup and log the status:

```{.bash data_prompt="$"}
$ xtrabackup --backup --target-dir=/path/to/backup --log-status=/path/to/logfile
```

This command has the following options:

* `xtrabackup` is the Percona XtraBackup command.

* `--backup` tells XtraBackup to perform a backup.

* `--target-dir=/path/to/backup` specifies the directory where the backup files will be stored.

* `--log-status=/path/to/logfile` specifies the file where the status log will be saved.

The log file contains various pieces of information, such as:

* **Progress Information**: Details on how much of the backup process is complete.

* **Time Stamps**: The times at which different stages of the backup process start and finish.

* **Errors and Warnings**: Any issues encountered during the backup process, such as missing files or permission problems.

* **File Details**: Information about the files being backed up, including their sizes and locations.

To read the log file, you can use any text editor or command-line tool. For example, you can use the `cat` command to display the contents of the log file in the terminal:

```{.bash data-prompt="$"}
$ cat /path/to/logfile
```

### Error handling

xtrabackup returns 0 (zero) on success and a non-zero value on failure.

An error or inconsistency that causes the backup to abort. 

| Type | Description |
|---|---|
| Data corruption | Data corrupted due to hardware failures, software bugs, or other issues |
| Incomplete backups | Interruptions during the backup process, such as network failures or power outages |
| Incorrect backup settings | Misconfigured backup settings can cause problems. |

You can create an error log when you create a backup to capture any errors.

```{.bash data-prompt="$"}
$ xtrabackup --backup --target-dir=/data/backups/ 2>xtrabackup_error.log
```

In the command, the `2>xtrabackup_error.log` part redirects the standard error (stderr) to a file named `xtrabackup_error.log`. Error messages or warnings generated during the backup process are captured in this log.

It's crucial to have robust backup procedures, monitoring systems, and contingency plans to mitigate the risks associated with backup failures. Regular testing and validation of backup procedures can also help ensure the reliability and integrity of backup data.

## Prepare phase

The `prepare` phase uses the automated MySQL crash recovery process to return the database to a consistent state. The process works in the following way:

* Initialization: The MySQL server restarts, prompting InnoDB to initiate recovery.

* Tablespace Discovery: InnoDB meticulously identifies all tablespaces requiring the application of redo logs. These logs contain the most recent database transactions that were not yet physically written to disk at the time of the crash.

* Redo Log Application: During initialization, InnoDB applies the redo logs to the identified tablespaces. This operation ensures all committed transactions are reflected in the database.

* Undo Log Rollback: In parallel with the redo log application, InnoDB scans the undo logs to identify uncommitted transactions. These transactions are rolled back, ensuring the database reflects a consistent state and avoids persisting incomplete data modifications.

* Recovery Completion: When the redo log application and the undo log rollback operations are complete, InnoDB signals a successful crash recovery. The server is now prepared to accept new connections and resume normal operations.

The backed-up MyISAM and InnoDB tables are eventually consistent because, after the prepare (recovery) process, InnoDB’s data is rolled forward to the point at which the backup is completed, not rolled back to where it started. This point matches where the lock was taken, so the MyISAM data and the prepared InnoDB data are in sync.

In brief, though, the `xtrabackup` binary enables you to do operations such as streaming and incremental backups with various combinations of copying the data files, copying the log files, and applying the logs to the data.

## Restoring a backup

To restore a backup with `xtrabackup`, you can use the [--copy-back] or [--move-back] options.

The `xtrabackup` binary checks if the following directories exist in the `my.cnf` configuration file and then reads from the following locations:

* datadir

* innodb_data_home_dir

* innodb_data_file_path

* innodb_log_group_home_dir


### copy-back option

When you are restoring a database using XtraBackup, you would use the `--copy-back` option in the following scenario:

* You have previously taken a backup of your database using XtraBackup.

* You want to restore the database from the backup files.

* Instead of manually copying the backup files to the appropriate locations, you can use the `--copy-back` option.

This option automatically copies the MyISAM tables, indexes, InnoDB tables, indexes, and log files from the backup location to their respective locations in the MySQL data directory and preserves the file attributes during the copying process. Note that after using the `--copy-back` option, you may need to change the ownership of the copied files to the `mysql` user before starting the database server.

The restore happens in the following order:

* Copies the MyISAM tables, indexes, and the .MRG, .MYD, .MYI, .CSM, .CSV, `.sdi`, and `par` files 

* Copies the InnoDB tables and indexes 


### move-back option

Use the [`--move-back`] option when there is not enough free disk space to hold both the data files and their backup copies. This option allows you to restore the backup by moving the files to their target locations instead of copying them. Be aware to use this option with caution because the operation removes the backup files.

If your scenario meets these criteria, restore a backup using the `--move-back` option. The restore process for this option is similar to [--copy-back].


[--register-redo-log-consumer]: xtrabackup-option-reference.md#register-redo-log-consumer
[--copy-back]: xtrabackup-option-reference.md#copy-back
[--move-back]: xtrabackup-option-reference.md#move-back
[--slave-info]: xtrabackup-option-reference.md#slave-info
[Backup locks]: https://docs.percona.com/percona-server/innovation-release/backup-locks.html
[xtrabackup]: xtrabackup-binary-overview.md
[permissions and privileges]: privileges.md
[create a GTID-based replica]: create-gtid-replica.md
