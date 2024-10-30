# The xtrabackup command-line options

Here you can find all of the command-line options for the xtrabackup binary.

## Modes of operation

You invoke xtrabackup in one of the following modes:

* `--backup` mode to make a backup in a target directory

* `--prepare` mode to restore data from a backup (created in `--backup` mode)

* `--copy-back` to copy data from a backup to the original location; to move the data instead of copying the data, use the alternate `--move-back` mode.

When you intend to run xtrabackup in any of these modes, use the following syntax:

```{.bash data-prompt="$"}
$ xtrabackup [--defaults-file=#] --backup|--prepare|--copy-back| [OPTIONS]
```

For example, the `--prepare` mode is applied as follows:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --target-dir=/data/backup/mysql/
```

For all modes, the default options are read from the xtrabackup and
mysqld configuration groups from the following files in the given order:

1. `/etc/my.cnf`


2. `/etc/mysql/my.cnf`


3. `/usr/etc/my.cnf`


4. `~/.my.cnf`.

As the first parameter to xtrabackup in place of the `--defaults-file`,
you may supply one of the following:

* `--print-defaults` - prints the argument list and exit.

* `--no-defaults` - forbids reading options from any file but the login file.

* `--defaults-file` -  reads the default options from the given file.

* `--defaults-extra-file` - reads the specified additional file after the global files.

* `--defaults-group-suffix` -  reads the configuration groups with the given suffix. The effective group name is constructed by concatenating the default configuration groups (xtrabackup and mysqld) with the given suffix.

* `--login-path` - reads the given path from the login file.

### InnoDB options

A large group of InnoDB options is usually read from the `my.cnf` configuration file, so xtrabackup boots up its embedded InnoDB in the same configuration as your current server. You typically do not
need to specify them explicitly. These options have the same behavior in InnoDB
and XtraDB. See [`--innodb-miscellaneous`](#innodb-miscellaneous) for more information.

## Options

### apply-log-only

Usage: `--apply-log-only`

This option causes only the redo stage to be performed when preparing a
backup. It is essential for incremental backups.

### backup

Usage: `--backup`

Make a backup and place it in `--target-dir`. See [Create a full backup](create-full-backup.md)

### backup-lock-timeout

Usage: `--backup-lock-timeout`

The timeout in seconds for attempts to acquire metadata locks.

### backup-lock-retry-count

Usage: `--backup-lock-retry-count`

The number of attempts to acquire metadata locks.

### backup-locks

Usage: `--backup-locks`

This option controls if [Backup locks] are used instead of `FLUSH TABLES
WITH READ LOCK` on the backup stage. The option has no effect when the server does not support backup locks. This option is enabled by default,
disable with [`--no-backup-locks`](#no-backup-locks).

### check-privileges

Usage: `check-privileges`

This option checks if Percona XtraBackup has all the required privileges.
If a required privilege is missing for the current operation,
the operation terminates and prints an error message.
If a privilege is not needed for the current operation but is missing and may be necessary for another XtraBackup operation, the operation is not aborted, and a warning is printed.

??? example "Example output"

        ```{.text .no-copy}
        xtrabackup: Error: missing required privilege LOCK TABLES on *.*
        xtrabackup: Warning: missing required privilege REPLICATION CLIENT on *.*
        ```

### close-files

Usage: `--close-files`

Do not keep files opened. When xtrabackup opens a tablespace, xtrabackup normally
doesn’t close its file handle. This operation allows xtrabackup to handle the DDL operations
correctly. However, if the number of tablespaces is huge and can not
fit into any limit, there is an option to close file handles once they are
no longer accessed. Percona XtraBackup can produce inconsistent backups
with this option enabled. Use at your own risk.

### compress

Usage: `--compress`

This option tells xtrabackup to compress all output data, including the
transaction log and metadata files, using either the `ZSTD` or the `lz4` compression algorithm. `ZSTD` is the default compression algorithm.

`--compress` produces `\*.zst` files. You can extract the contents of these files using the `--decompress` option. You can specify the `ZSTD` compression level with the [`--compress-zstd-level`](#compress-zstd-level) option.

`--compress=lz4` produces `\*.lz4` files. You can extract the contents of
these files by using the `lz4` program.

### compress-chunk-size

Usage: `--compress-chunk-size=#`

Size of working buffer(s) for compression threads in bytes. The default
value is 64K.

### compress-threads

Usage: `--compress-threads=#`

This option specifies the number of worker threads xtrabackup uses for parallel data compression. This option defaults to `1` and can be used with [parallel](#parallel) file copying.

For example, `--parallel=4 --compress --compress-threads=2`
creates four I/O threads that read and pipe the data to two compression threads.

### compress-zstd-level

Usage: `--compress-zstd-level=#`

This option specifies `ZSTD` compression level. Compression levels provide a trade-off between the compression speed and the compressed files' size. A lower compression level provides faster compression speed but larger file sizes. A higher compression level provides lower compression speed but smaller file sizes. For example, set level 1 if the compression speed is the most important for you. Set level 19 if the size of the compressed files is the most important.

The default value is 1. Allowed range of values is from 1 to 19.

### copy-back

Usage: `--copy-back`

Copy all the files in a previously made backup from the backup directory to
their original locations. This option will not copy over existing files
unless the [`--force-non-empty-directories`](#force-non-empty-directories) option is specified.

### core-file

Usage: `--core-file`

Write core on fatal signals.

### databases

Usage: `--databases=#`

This option specifies a list of databases and tables that should be backed
up. The option accepts the list of the form `"databasename1[.table_name1]
databasename2[.table_name2] . . ."`.

### databases-exclude

Usage: `--databases-exclude=name`

Databases are excluded based on name. This option operates the same way as `--databases` but excludes the matched names from the backup.

This option has a higher priority than `--databases`.

### databases-file

Usage: `--databases-file=#`

This option specifies the path to the file containing the list of databases
and tables that should be backed up. The file can contain the list elements
of the form `databasename1[.table_name1]`, one element per line.

### datadir

Usage: `--datadir=DIRECTORY`

The source directory for the backup. This should be the same as the datadir
for your server, so it should be read from `my.cnf` if that
exists; otherwise, specify the directory on the command line.

When combined with the [`--copy-back`](#copy-back) or the
[`--move-back`](#move-back) option, this option refers to the destination directory.

To perform a backup, you must have the
`READ` and `EXECUTE` permissions at a filesystem level in the
server’s datadir.

### debug-sleep-before-unlock

Usage: `--debug-sleep-before-unlock=#`

This option is only used by the xtrabackup test suite.

### debug-sync

Usage: `--debug-sync=name`

This option is only used by the xtrabackup test suite.

### decompress

Usage: `--decompress`

Decompresses all files in a backup previously
made with the `--compress` option. The
`--parallel` option lets multiple files be
decrypted simultaneously.

Percona XtraBackup does not automatically remove the compressed files. Users should use the `--remove-original` option to clean up the backup directory.

### decompress-threads

Usage: `--decompress-threads=#`

Force xbstream to use the specified number of threads for decompressing.

### decrypt

Usage: `--decrypt=ENCRYPTION-ALGORITHM`

Decrypts all files with the `xbcrypt` extension in a backup
previously made with [`--encrypt`](#encrypt) option. The
[`--parallel`](#parallel) option lets multiple files be
decrypted simultaneously. Percona XtraBackup doesn’t
automatically remove the encrypted files; use `--`remove-original`](#remove-original) option.

### defaults-extra-file

Usage: `--defaults-extra-file=[MY.CNF]`

Read this file after the global files are read. The option must be the first
option on the command line.

### defaults-file

Usage: `--defaults-file=[MY.CNF]`

Only read default options from the given file. The value must be the first
option on the command line and cannot be a symbolic link.

### defaults-group

Usage: `--defaults-group=GROUP-NAME`

This option sets the group that should be read from the configuration file and is needed for `mysqld_multi` deployments.

### defaults-group-suffix

Usage: `--defaults-group-suffix=#`

Also reads groups with concat(group, suffix).

### dump-innodb-buffer-pool

Usage: `--dump-innodb-buffer-pool`

This option controls creating a new dump of the buffer pool content.

The xtrabackup binary requests the server to start the buffer pool dump. This operation may take time to complete and is done in the background. The
beginning of a backup with the option reports that the dump has been
completed.

```{.bash data-prompt="$"}
$ xtrabackup --backup --dump-innodb-buffer-pool --target-dir=/home/user/backup
```

By default, this option is set to OFF.

If [`innodb_buffer_pool_dump_status`](https://dev.mysql.com/doc/refman/8.3/en/server-status-variables.html#statvar_Innodb_buffer_pool_dump_status) reports that there is a running dump of the buffer pool, xtrabackup waits for the dump to complete
using the value of [`--dump-innodb-buffer-pool-timeout`](#dump-innodb-buffer-pool-timeout)

The file `ib_buffer_pool` stores the tablespace ID and page ID
data used to warm up the buffer pool sooner.

### dump-innodb-buffer-pool-pct

Usage: `--dump-innodb-buffer-pool-pct`

This option contains the percentage of the most recently used buffer pool
pages to dump.

This option is effective if `--dump-innodb-buffer-pool` option is set
to ON. If this option contains a value, xtrabackup sets the MySQL
system variable [`innodb_buffer_pool_dump_pct`](https://dev.mysql.com/doc/refman/8.3/en/innodb-parameters.html#sysvar_innodb_buffer_pool_dump_pct). As soon as the buffer pool
dump completes or is stopped (see
`--dump-innodb-buffer-pool-timeout`), the value of the MySQL system
variable is restored.

### dump-innodb-buffer-pool-timeout

Usage: `--dump-innodb-buffer-pool-timeout`

This option contains the number of seconds that xtrabackup should
monitor the value of [`innodb_buffer_pool_dump_status`](https://dev.mysql.com/doc/refman/8.0/en/server-status-variables.html#statvar_Innodb_buffer_pool_dump_status) to
determine if the buffer pool dump has been completed.

This option is used in combination with
[`--dump-innodb-buffer-pool`](#dump-innodb-buffer-pool). By default, it is set to 10 seconds.

### encrypt

Usage: `--encrypt=ENCRYPTION_ALGORITHM`

This option instructs xtrabackup to encrypt backup copies of InnoDB data
files using the algorithm specified in the ENCRYPTION_ALGORITHM. Currently
supported algorithms are: `AES128`, `AES192` and `AES256`

### encrypt-key

Usage: `--encrypt-key=ENCRYPTION_KEY`

A proper length encryption key to use. This key can be viewed as part of the process info. We do not recommend using this option with uncontrolled access to the machine.

### encrypt-key-file

Usage: `--encrypt-key-file=ENCRYPTION_KEY_FILE`

The name of a file where the raw key of the appropriate length can be read
from. The file must be a simple binary (or text) file that contains exactly
the key to be used.

It is passed directly to the xtrabackup child process. See the
xtrabackup documentation for more details.

### encrypt-threads

Usage: `--encrypt-threads=#`

This option specifies the number of worker threads that will be used for
parallel encryption/decryption.
See the xtrabackup documentation for more details.

### encrypt-chunk-size

Usage: `--encrypt-chunk-size=#`

This option specifies the size of the internal working buffer for each
encryption thread, measured in bytes. It is passed directly to the
xtrabackup child process.

To adjust the chunk size for encrypted files, use [`--read-buffer-size`](#read-buffer-size) and this option.

### estimate-memory

Usage: `--estimate-memory=#`

This option is in [tech preview](glossary.md#tech-preview).

The option lets you enable or disable the [Smart memory estimation](smart-memory-estimation.md) feature. The default value is OFF. Enable the feature by setting `--estimate-memory=ON` in the backup phase and setting the `--use-free-memory-pct` option in the `--prepare` phase. If the `--estimate-memory` setting is disabled, the `--use-free-memory-pct` setting is ignored.

An example of how to enable the Smart memory estimation feature:

```{.bash data-prompt="$"}
$ xtrabackup --backup --estimate-memory=ON --target-dir=/data/backups/
```

```{.bash data-prompt="$"}
$ xtrabackup --prepare --use-free-memory-pct=50 --target-dir=/data/backups/
```

### export

Usage: `--export`

Create files necessary for exporting tables. For more details, see [Restore individual tables](restore-individual-tables.md).

### extra-lsndir

Usage: `--extra-lsndir=DIRECTORY`

(for –backup): save an extra copy of the `xtrabackup_checkpoints`
and `xtrabackup_info` files in the specified directory.

### force-non-empty-directories

Usage: `--force-non-empty-directories`

When specified, the `-`-copy-back` and `--move-back` options transfer files to non-empty directories. No existing files are overwritten. If files that need to
be copied/moved from the backup directory already exist in the destination
directory, the operation fails with an error.

### ftwrl-wait-timeout

Usage: `--ftwrl-wait-timeout=SECONDS`

This option specifies the time in seconds that xtrabackup should wait for
queries that would block `FLUSH TABLES WITH READ LOCK` before running it.
If there are still such queries when the timeout expires, xtrabackup
terminates with an error.

The default value is `0`, xtrabackup does not wait
for queries to complete and starts `FLUSH TABLES WITH READ LOCK`
immediately. Where supported, xtrabackup automatically uses the [Backup locks] as a lightweight alternative to `FLUSH TABLES WITH READ LOCK` to copy
non-InnoDB data to avoid blocking DML queries that modify the InnoDB tables.

### ftwrl-wait-threshold

Usage: `--ftwrl-wait-threshold=SECONDS`

This option specifies the query run time threshold which is used by
xtrabackup to detect long-running queries with a non-zero value of
`--ftwrl-wait-timeout`. `FLUSH TABLES WITH READ LOCK`
is not started until such long-running queries exist.

This option has no effect if `--ftwrl-wait-timeout` is `0`. The default value
is `60` seconds. The xtrabackup binary automatically uses [Backup locks] as a lightweight alternative to `FLUSH TABLES WITH READ LOCK` to copy
non-InnoDB data to avoid blocking DML queries that modify InnoDB tables when backup locks are supported.

### ftwrl-wait-query-type

Usage: `--ftwrl-wait-query-type=all|update`This option specifies which queries can be completed before xtrabackup issues the global lock. The default value is `all`.

### galera-info

Usage: `--galera-info`

This option creates the `xtrabackup_galera_info` file, which contains the local node state at the backup time. This option should be used when
performing the backup of a Percona XtraDB Cluster. The option has no effect when [Backup locks] are used to create the backup.

### generate-new-master-key

Usage: `--generate-new-master-key`

Generate a new master key when doing a copy-back.

### generate-transition-key

Usage: `--generate-transition-key`

xtrabackup needs to access the same keyring file or vault server
during prepare and copy-back operations but it should not depend on whether the
server keys have been purged.

`--generate-transition-key` creates and adds to the keyring
a transition key for xtrabackup to use if the master key used for
encryption is not found because that key has been rotated and purged.

### get-server-public-key

Usage: `--get-server-public-key`

Get the server public key

### help

Usage: `--help`

This option displays information about how to run the program along with supported options and variables with the default values, where appropriate.

### history

Usage: `--history=NAME`

This option enables the tracking of backup history in the
`PERCONA_SCHEMA.xtrabackup_history` table. You can specify a history series name placed with the current backup's history record.

### host

Usage: `--host=HOST`

This option accepts a string argument that specifies the host to use when
connecting to the database server with TCP/IP. It is passed to the mysql
child process without alteration. See mysql --help for details.

### incremental-basedir

Usage: `--incremental-basedir=DIRECTORY`

This is the directory that contains the full backup, which is the base dataset for the incremental backups.

### incremental-dir

Usage: `--incremental-dir=DIRECTORY`

This is the directory where the incremental backup is combined with the full backup to make a new full backup.

### incremental-force-scan

Usage: `--incremental-force-scan`

When creating an incremental backup, force a full scan of the data pages in
that instance.

### incremental-history-name

Usage: `--incremental-history-name=name`

This option specifies the name of the backup series stored in the
`PERCONA_SCHEMA.xtrabackup_history` used as a base for an incremental backup. xtrabackup searches the history table looking for the most
recent (highest `innodb_to_lsn`), successful backup in the series and takes the `to_lsn`` value to use as the starting `lsn` for the incremental
backup.

This options is mutually exclusive with
[`--incremental-history-uuid`](#incremental-history-uuid), [`--incremental-basedir`](#incremental-basedir), and
[`--incremental-lsn`](#incremental-lsn).

If no valid lsn can be found, either no series by that
name or no successful backups by that name, xtrabackup returns an
error.

The option is used with the `--incremental` option.

### incremental-history-uuid

Usage: `--incremental-history-uuid=name`

This option specifies the Universal Unique Identifier (UUID) of the history record in `PERCONA_SCHEMA.xtrabackup_history` used as the base for an incremental backup.

This options is mutually exclusive with [`--incremental-history-name`](#incremental-history-name), [`--incremental-basedir`](#incremental-basedir), and
[`--incremental-lsn`](#incremental-lsn).

If there is no success record with that UUID, xtrabackup returns an error.

The option is used with the `-–incremental` option.

### incremental-lsn

Usage: `--incremental-lsn=LSN`

When creating an incremental backup, you can specify the log sequence number
(LSN), a single 64-bit integer, instead of the  [`--incremental-basedir`](#incremental-basedir).

!!! important

    Percona XtraBackup does not detect if an incorrect LSN value is specified; the backup is unusable. Be careful!

### innodb

Usage: `--innodb=name`

This option is ignored for MySQL option compatibility.

### innodb-miscellaneous

Usage: `--innodb-miscellaneous
xtrabackup boots up its embedded InnoDB with the same configuration as your current server using the InnoDB options read from that server's `my.cnf` file. You do not need to specify these options explicitly.

These options behave the same in either InnoDB or XtraDB.

### keyring-file-data

Usage: `--keyring-file-data=FILENAME`

Defines the path to the keyring file. You can combine this option with
[`--xtrabackup-plugin-dir`](#xtrabackup-plugin-dir).

### kill-long-queries-timeout

Usage: `--kill-long-queries-timeout=SECONDS`

This option specifies the number of seconds xtrabackup waits between
starting `FLUSH TABLES WITH READ LOCK` and killing those queries that block
it. The default value is 0 (zero) seconds, which means xtrabackup does not kill
any queries.

To use this option xtrabackup user should have the
`PROCESS` and `SUPER` privileges.

Where supported, xtrabackup
automatically uses [Backup locks] as a lightweight alternative to `FLUSH TABLES WITH READ LOCK` to copy non-InnoDB data to avoid blocking DML queries that modify InnoDB tables.

### kill-long-query-type

Usage: `--kill-long-query-type=all|select`

This option specifies which queries should be killed to unblock the
global lock. The default value is “select”.

### lock-ddl

Usage: `--lock-ddl`

Enabled by default to ensure that any DDL event does not corrupt the backup. Any DML events continue to occur. A DDL lock protects table and view definitions.

The available values are the following:

|Option| Description|
|-------|-----------|
|`--lock-ddl=ON`| The backup lock is enabled and is taken at the beginning of the backup.|
|`--lock-ddl=OFF`|The backup lock is not taken.|
|`--lock-ddl=REDUCED`|This option value is a [tech preview](./glossary.md#tech-preview). <br><br> The option value has been added in [Percona XtraBackup 8.4.0-2](./release-notes/8.4.0-2.md) to reduce the time the instance remains under backup lock. The backup lock is taken after copying the `.ibd` files and before copying the `non-InnoDB` files.|

With the `--lock-ddl=ON` option the backup process is as follows:
{ .power-number }

1. Set a backup lock on the server to prevent any DDL operations, such as creating or altering tables.

2. Parse and copy the redo logs from the checkpoint up to the current `Log Sequence Number` (LSN), and start tracking new file operations.

3. Identify and copy the `.ibd` files.

4. Copy `non-InnoDB` files.

5. Gather a sync point from all engines (InnoDB LSN, binlog, Global Transaction Identifier (GTID), etc.) by querying the log status.

6. Stop the redo thread once it copies at least up to sync point.

7. Release the backup lock on the server.

If the backup lock is disabled with the [`--lock-ddl=OFF`](./xtrabackup-option-reference.md/#lock-ddl) option, a backup continues while concurrent DDL operations are executed. These backups may be invalid and may fail at either the `backup` or the `--prepare` step.

Use a [safe-slave-backup](#safe-slave-backup) option to stop a SQL replica thread before copying the InnoDB files.

### lock-ddl-per-table

Usage: `--lock-ddl-per-table`

Deprecated in Percona XtraBackup 8.0. Use the [`–lock-ddl`](#lock-ddl) option instead
<!--26-1-24-->
Lock DDL for each table before xtrabackup starts to copy it and until the backup is completed.

### lock-ddl-timeout

Usage: `--lock-ddl-timeout`

If `LOCK TABLES FOR BACKUP` or `LOCK INSTANCE FOR BACKUP` does not return
within a given time, abort the backup.

### log

Usage: `--log`

This option is ignored for MySQL

### log-bin

Usage: `--log-bin`

The base name for the log sequence.

### log-bin-index

Usage: `--log-bin-index=name`

The file that stores the names for binary log files.

### log-copy-interval

Usage: `--log-copy-interval=#`

This option specifies the time interval between checks done by the log
copying thread in milliseconds. The default value is 1 second.

### login-path

Usage: `--login-path`

Read the given path from the login file.

### move-back

Usage: `--move-back`

Move all files in a previous backup from the backup directory to
their original locations.

Use this option with caution since the operation removes backup files.

### no-backup-locks

Usage: `--no-backup-locks`

Explicity disables the [`--backup-locks`](#backup-locks) option which is enabled by default.

### no-defaults

Usage: `--no-defaults`

The default options are only read from the login file.

### no-lock

Usage: `--no-lock`

Disables the table lock with `FLUSH TABLES WITH READ
LOCK`. Use it only if all your tables are InnoDB and you do not care
about the binary log position of the backup. This option shouldn’t be used if any DDL statements are being executed or updates are
happening on non-InnoDB tables; this includes the system MyISAM tables in the
mysql database. Otherwise, those operations could lead to an inconsistent backup.

Where supported, xtrabackup will automatically use [Backup locks] as a lightweight alternative to `FLUSH TABLES WITH READ LOCK` to copy
non-InnoDB data to avoid blocking DML queries that modify InnoDB tables.

If you consider using this option because your backups fail to acquire
the lock, maybe incoming replication events prevent
the lock from succeeding. Try the `--safe-slave-backup` option to stop the replication replica thread momentarily. The `--safe-slave-backup` option may help the backup to succeed and avoid using this option.

### no-server-version-check

Usage: `--no-server-version-check`

The `--no-server-version-check` option disables the server version check.

The default behavior runs a check that compares the source system version to the Percona XtraBackup version. If the source system version is higher than the XtraBackup version, the backup is aborted with a message.

Adding the option overrides this check, and the backup proceeds, but there may be issues with the backup.

See [Server Version and Backup Version Comparison](server-backup-version-comparison.md) for more information.

### no-version-check

Usage: `--no-version-check`

This option disables the version check. 

If you do not pass this option, xtrabackup implicitly enables the
automatic version check in the `--backup` mode. 

To disable the version check, invoke xtrabackup and explicitly pass this option.

When the automatic version check is enabled, xtrabackup performs a
version check against the server on the backup stage after creating a server
connection. xtrabackup sends the following information to the server:

* MySQL flavour and version

* Operating system name

* Percona Toolkit version

* Perl version

Each piece of information has a unique identifier. This identifier is a MD5 hash value
that Percona Toolkit uses to obtain statistics about its use. This information is
a random UUID; no client information is collected or stored.

### open-files-limit

Usage: `--open-files-limit=#`

The maximum number of file descriptors to reserve with [setrlimit](https://linux.die.net/man/2/setrlimit)git .

### parallel

Usage: `--parallel=#`

This option specifies the number of threads to use to copy multiple data
files concurrently when creating a backup. The default value is 1, there is no
concurrent transfer. This option can be used with the `--copy-back` option to copy the user data files in parallel. The redo logs and system tablespaces are copied in the main thread.

### password

Usage: `--password=PASSWORD`

This option accepts a string argument that specifies the password used when connecting to the database.

### plugin-load

Usage: `--plugin-load`

A list of plugins to load.

### port

Usage: `--port=PORT`

This option accepts a string argument specifying the TCP/IP port used to connect to the database server. This option is passed to the mysql child process without alteration.

### prepare

Usage: `--prepare`

Makes xtrabackup perform a recovery on a backup created with `--backup`, so that the backup data is ready to use.

For details, see [Prepare a full backup](prepare-full-backup.md).

### print-defaults

Usage: `--print-defaults`

Prints the program argument list and exit and must be the first option on the command line.

### print-param

Usage: `--print-param`

Prints the parameters that can be used for copying the data files back to their original locations to restore them.

### read-buffer-size

Usage: `--read-buffer-size`

Set the read buffer size. The given value is scaled up to page size. The default size is 10MB. Use this option to increase the xbcloud/xbstream chunk size from the default size.

To adjust the chunk size for encrypted files, use [`--read-buffer-size`](#read-buffer-size) and [`--encrypt-chunk-size`](#encrypt-chunk-size).

### register-redo-log-consumer

Usage: `--register-redo-log-consumer`

This option is disabled by default.

When enabled, this options lets Percona XtraBackup register as a redo log consumer at the start of the backup. The server does not remove a redo log that Percona XtraBackup (the consumer) has not yet copied. The consumer reads the redo log and manually advances the log sequence number (LSN). The server blocks the writes during the process. The server determines when to purge the log based on the redo log consumption.

### remove-original

Usage: `--remove-original`

This option removes `.qp`, `.xbcrypt` and `.qp.xbcrypt` files after decryption and decompression.

### rocksdb-datadir

Usage: `--rocksdb-datadir`

Names the RocksDB data directory

### rocksdb-wal-dir

Usage: `--rocksdb-wal-dir`

RocksDB WAL directory.

### rocksdb-checkpoint-max-age

Usage: `--rocksdb-checkpoint-max-age`

The checkpoint cannot be older than this number of seconds when the backup is complete.

### rocksdb-checkpoint-max-count

Usage: `--rocksdb-checkpoint-max-count`

Complete the backup even if the checkpoint age requirement has not been met after this number of checkpoints.

### rollback-prepared-trx

Usage: `--rollback-prepared-trx`

Force rollback prepared InnoDB transactions.

### rsync

Usage: `--rsync`

Uses the rsync utility to optimize local file transfers. The xtrabackup binary uses rsync to copy all non-InnoDB files instead of spawning a separate cp for each file, which can be much faster for servers with many databases or tables.

You cannot use this option with [`--stream`](#stream).

### safe-slave-backup

Usage: `--safe-slave-backup`

When specified, xtrabackup stops the replica SQL thread just before
running `FLUSH TABLES WITH READ LOCK` and waits to start the backup operation until `Replica_open_temp_tables`` in `SHOW STATUS` is zero.

If there are no open temporary tables, the backup takes place, otherwise the SQL thread is started and stopped until there are no open temporary tables. The backup fails if `Replica_open_temp_tables` does not become zero after
[`--safe-slave-backup-timeout`](#safe-slave-backup-timeout
) seconds. The replication SQL thread is restarted when the backup is complete.
This option is implemented to deal with [replication and temporary tables](https://dev.mysql.com/doc/refman/{{vers}}/en/replication-features-temptables.html) and isn’t necessary with row-based replication.

Using a safe-slave-backup option stops the SQL replica thread before copying the InnoDB files.

### safe-slave-backup-timeout

Usage: `--safe-slave-backup-timeout=SECONDS`

How many seconds the `--safe-slave-backup` option waits for the `Replica_open_temp_tables` to become zero. The default value is 300 seconds.

### secure-auth

Usage: `--secure-auth`

Refuse the client from connecting to the server if it uses the old protocol. This option is enabled by default. Disable this options with `–skip-secure-auth`.

### server-id

Usage: `--server-id=#`

The server instance being backed up.

### server-public-key-path

Usage: `--server-public-key-path`

The file path to the server public RSA key in the PEM format.

### skip-tables-compatibility-check

Usage: `--skip-tables-compatibility-check`

See [`--tables-compatibility-check`](#tables-compatibility-check).

### slave-info

Usage: `--slave-info`

This option is useful when backing up a replication replica server. It prints
the binary log position of the source server. It also writes the binary log
coordinates to the `xtrabackup_slave_info` file as a [`CHANGE REPLICATION SOURCE TO`](https://dev.mysql.com/doc/refman/{{vers}}/en/change-replication-source-to.html)
command.

A new replica for this source can be set up by starting a replica server on this backup and issuing a [`CHANGE REPLICATION SOURCE TO`](https://dev.mysql.com/doc/refman/{{vers}}/en/change-replication-source-to.html) command with the binary log
position saved in the `xtrabackup_slave_info` file.

### socket

Usage: `--socket`

This option accepts a string argument that specifies the socket to use when
connecting to the local database server with a UNIX domain socket. It is
passed to the MySQL child process without alteration. See mysql
--help for details.

### ssl

Usage: `--ssl`

Enable secure connection.

### ssl-ca

Usage: `--ssl-ca`

The path of the file contains a list of trusted SSL CAs.

### ssl-capath

Usage: `--ssl-capath`

The directory path that contains trusted SSL CA files in PEM format.

### ssl-cert

Usage: `--ssl-cert`

The path of the file contains the X509 certificate in PEM format.

### ssl-cipher

Usage: `--ssl-cipher`

The list of the permitted ciphers to use for connection encryption.

### ssl-crl

Usage: `--ssl-crl`

The path of the file that contains certificate revocation lists.

### ssl-crlpath

Usage: `--ssl-crlpath`

The path of the directory that contains the certificate revocation list files.

### ssl-fips-mode

Usage: `--ssl-fips-mode`

The SSL FIPS mode applies only for OpenSSL; permitted values are OFF, ON, and STRICT.

### ssl-key

Usage: `--ssl-key`

The path of the file that contains the X509 key in PEM format.

### ssl-mode

Usage: `--ssl-mode`

The security state of connection to the server.

### ssl-verify-server-cert

Usage: `--ssl-verify-server-cert`

Verify the server certificate Common Name value against the hostname used when connecting to the server.

### stream

Usage: `--stream=FORMAT`

Stream all backup files to the standard output in the specified format.
Currently, this option only supports the xbstream format.

### strict

Usage: `--strict`

If this option is specified, xtrabackup fails with an error when invalid
parameters are passed.

### tables

Usage: `--tables=name`

A regular expression against which the full table name in the `databasename.tablename` format is matched. If the name matches, the
table is backed up. See [Create a partial backup](create-partial-backup.md).

### tables-compatibility-check

Usage: `--tables-compatibility-check`

Enables the engine compatibility warning. The default value is
`ON`. To disable the engine compatibility warning, use `--`skip-tables-compatibility-check`](#skip-tables-compatibility-check).

### tables-exclude

Usage: `--tables-exclude=name`

Filtering by regexp for table names. Operates the same
way as [`--tables`](#tables), but matched names are excluded from
backup. Note that this option has a higher priority than
`--tables`.

### tables-file

Usage: `--tables-file=name`

A file containing one table name per line in `databasename.tablename` format.
The backup will be limited to the specified tables.

### target-dir

Usage: `--target-dir=DIRECTORY`

This option specifies the destination directory for the backup. If the
directory does not exist, xtrabackup creates it. If the directory
does exist and is empty, xtrabackup will succeed.
xtrabackup does not overwrite existing files, however, the operation fails with the operating system error 17, `file exists`.

If this option is a relative path, it is interpreted as relative to
the current working directory from which xtrabackup is executed.

To perform a backup, you need `READ`, `WRITE`, and `EXECUTE`
permissions at a filesystem level for the directory that you supply as the
value of `--target-dir`.

### innodb-temp-tablespaces-dir

Usage: `--innodb-temp-tablespaces-dir=DIRECTORY`

The location of the directory for the temp tablespace files. This path can be absolute.

### throttle

Usage: `--throttle=#`

This option limits the number of chunks copied per second. The chunk size is
10 MB.

To limit the bandwidth to 10 MB/s, set the option to 1.

### tls-ciphersuites

Usage: `--tls-ciphersuites`

The TLS v1.3 cipher to use.

### tls-version

Usage: `--tls-version`

Defines which TLS version to use. The permitted values are: TLSv1, TLSv1.1,
TLSv1.2, TLSv1.3.

### tmpdir

Usage: `--tmpdir=name`

Specify the directory used to store temporary files during the
backup

### transition-key

Usage: `--transition-key=name`

This option is used to enable processing the backup without accessing the
keyring vault server. In this case, xtrabackup derives the AES
encryption key from the specified passphrase and uses it to encrypt the tablespace keys of tablespaces being backed up.

If `--transition-key` does not have any
value, xtrabackup will ask for it. The same passphrase should be
specified for the `--prepare` command.

### use-free-memory-pct

Usage: `--use-free-memory-pct`

The `--use-free-memory-pct` is a [tech preview](glossary.md#tech-preview) option.

This option lets you configure the [Smart memory estimation](smart-memory-estimation.md) feature. The option controls the amount of free memory that can be used to `--prepare` a backup. The default value is 0 (zero), which defines the option as disabled. For example, if you set `--use-free-memory-pct=50`, then 50% of the free memory is used to `prepare` a backup. The maximum allowed value is 100.

This option works only if `--estimate-memory` option is enabled. If the `--estimate-memory` option is disabled, the `--use-free-memory-pct` setting is ignored.

An example of how to enable the Smart memory estimation feature:

```{.bash data-prompt="$"}
$ xtrabackup --backup --estimate-memory=ON --target-dir=/data/backups/
```

```{.bash data-prompt="$"}
$ xtrabackup --prepare --use-free-memory-pct=50 --target-dir=/data/backups/
```

### use-memory

Usage: `--use-memory`

This option affects how much memory is allocated and is similar to `innodb_buffer_pool_size`. This option is only relevant in the `--prepare` phase. The default value is 100MB. The recommended value is between 1GB to 2GB. Multiple values are supported if you provide the unit (1MB, 1M, 1GB, 1G).

### user

Usage: `--user=USERNAME`

This option specifies the MySQL username used when connecting to the server if that’s not the current user. The option accepts a string argument. See
mysql –help for details.

### version

Usage: `--version`

This option prints xtrabackup version and exits.

### xtrabackup-plugin-dir

Usage: `--xtrabackup-plugin-dir=DIRNAME`

The absolute path to the directory that contains the `keyring` plugin.

[replicating temporary tables]: https://dev.mysql.com/doc/refman/{{vers}}/en/replication-features-temptables.html
[Backup locks]: https://docs.percona.com/percona-server/innovation-release/backup-locks.html
