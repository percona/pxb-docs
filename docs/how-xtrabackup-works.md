# How Percona XtraBackup works

Percona XtraBackup is based on InnoDB’s crash-recovery functionality.
The application copies your InnoDB data files, resulting in internally inconsistent data, and performs crash 
recovery on the files to make them a consistent, usable database again. This operation works because InnoDB maintains a redo log called the transaction log. This log contains a record of every change to the InnoDB data. When InnoDB
starts, the application inspects the data files and the transaction log and does the following:

* Applies committed transaction log entries to the data files

* Removes uncommitted transactions - any change made within those transactions is discarded

## Version changes

[Percona XtraBackup 8.0.30-23](release-notes/8.0/8.0.30-23.0.md) adds 
the [--register-redo-log-consumer] parameter. This parameter is 
disabled by default. When enabled, the parameter lets Percona XtraBackup 
register as a redo log consumer at the start of the backup. The server 
does not remove a redo log that Percona XtraBackup (the consumer) 
has not yet copied. The consumer reads the redo log and manually 
advances the log sequence number (LSN). The server blocks the writes 
during the process. The server determines when to purge the log based on the redo log consumption.


Percona XtraBackup works by remembering the LSN when it starts and then 
copying away the data files. It takes some time to do this, so if the files change, they reflect the 
state of the database at different points. At the same time, Percona XtraBackup runs a background 
process that watches the transaction log files and copies changes from them. 
Percona XtraBackup does this continually because the
transaction logs are written round-robin and can be reused. Percona XtraBackup needs the transaction log record for every change to the data files since it began execution.

## Locks

Locks are used in a backup to ensure data consistency. You cannot insert new data or modify data during the backup. Locking can cause performance issues, especially for frequently accessed tables.

Percona XtraBackup uses `LOCK INSTANCE FOR BACKUP` to take a backup log for the entire process, including InnoDB and non-InnoDB data. The `xtrabackup` binary copies the InnoDB data and then copies the MyISAM tables and files. 

The `xtrabackup` binary backs up the following file types:

* .FRM

* .MRG

* .MYD

* .MYI

* .CSM

* .CSV

* .SDI

* .PAR 

### LOCK INSTANCE FOR BACKUP

The `LOCK INSTANCE FOR BACKUP` statement is a feature introduced in MySQL 8.0 that allows you to acquire an instance-level backup lock. Executing the `LOCK INSTANCE FOR BACKUP` statement prevents any other session from acquiring a backup lock at the instance level. It ensures no changes to the data files while the backup process is running. This statement is executed after backing up all InnoDB/XtraDB data and logs and locks all non-InnoDB tables to safely copy non-InnoDB data without blocking any Data Manipulation Language (DML)  queries that modify InnoDB tables. The `LOCK INSTANCE FOR BACKUP` statement provides a more efficient and targeted way to lock the necessary tables during the backup process, reducing the impact on the database's availability and performance.

The `BACKUP_ADMIN` privilege is required to execute the `LOCK INSTANCE FOR BACKUP` statement. This privilege manages database backups, ensures data consistency, and performs backup-related tasks.

### Locking the binary log

The `performance_schema.log_status` table in MySQL is a valuable resource for backups. This table provides critical information that 
allows a backup tool to copy necessary log files without locking the resources for the duration of the copy process. When queried, 
the `log_status` table causes the server to momentarily block logging and related administrative changes to populate the table 
with data, and then the server releases the resources. This table identifies the point in the 
source's binary log and `gtid_executed` record the backup should copy, including the relay log for each replication channel. 
Additionally, it offers essential details, such as the last log sequence number (LSN) and the 
LSN of the previous checkpoint for InnoDB.

To use the `log_status` table effectively, you must have the `BACKUP_ADMIN` privilege and the `SELECT` privilege.

The table contains several columns, including `SERVER_UUID`, which is the server's unique identifier, and `LOCAL`, which provides the log 
position state information from the source as a JSON object. This table includes the current binary log file name and position, 
as well as the `gtid_executed` value at the time the table was accessed. The `REPLICATION` section is a JSON array containing detailed information about each replication channel, such as the channel name, current relay log file, and position. The `STORAGE_ENGINES` section provides 
JSON objects with keys for each applicable storage engine, detailing their specific log information.

To perform a backup using the `log_status` table, one would typically follow these steps:
1. Ensure you have the necessary privileges to access the `log_status` table.
2. Query the `log_status` table to retrieve the current logging state.
3. Use the information from the `LOCAL` and `REPLICATION` sections to determine the log files and positions that need to be copied.
4. Copy the log files up to the specified positions without the need to lock the resources for an extended period.
5. Use the information from the `STORAGE_ENGINES` section to handle engine-specific log data, if applicable.

It's important to note that the `log_status` table does not have indexes, and you cannot do operations like `TRUNCATE TABLE`.


## Prepare phase

The `prepare` phase uses the MySQL crash recovery process. This automated process uses transaction logs to return the database to a consistent state. The process works in the following way:

* MySQL checks the InnoDB transaction log files to determine the database state

* MySQL applies any uncommitted changes from the transaction logs to the database

Percona XtraBackup performs crash recovery in the prepare phase before restoring the database. 

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

* Copies the log files

### move-back option

Use the [`--move-back`] option when there is not enough free disk space to hold both the data files and their backup copies. This option allows you to restore the backup by moving the files to their target locations instead of copying them. Be aware to use this option with caution because the operation removes the backup files.

If your scenario meets these criteria, restore a backup using the `--move-back` option. The restore process for this option is similar to [--copy-back].


[--register-redo-log-consumer]: xtrabackup-option-reference.md#register-redo-log-consumer
[--copy-back]: xtrabackup-option-reference.md#copy-back
[--move-back]: xtrabackup-option-reference.md#move-back
[--slave-info]: xtrabackup-option-reference.md#slave-info
[Backup locks]: https://docs.percona.com/percona-server/innovation-release/backup-locks.html
[xtrabackup]: xtrabackup-binary-overview.md
