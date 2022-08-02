# The xtrabackup Binary

The *xtrabackup* binary is a compiled C program that is linked with the *InnoDB*
libraries and the standard *MySQL* client libraries.

*xtrabackup* enables point-in-time backups of *InnoDB* / *XtraDB* tables
together with the schema definitions, *MyISAM* tables, and other portions of the
server.

The *InnoDB* libraries provide the functionality to apply a log to data
files. The *MySQL* client libraries are used to parse command-line options and
configuration file.

The tool runs in either `--backup` or `--prepare` mode,
corresponding to the two main functions it performs. There are several
variations on these functions to accomplish different tasks, and there are two
less commonly used modes, `--stats` and `--print-param`.

## Other Types of Backups


* [Incremental Backups](incremental_backups.md)


* [Partial Backups](partial_backups.md)


## Advanced Features

<!-- NB: the following section has been removed because it is a
duplicate of a section in source/advanced:

throttling_backups -->

* [Analyzing Table Statistics](analyzing_table_statistics.md)


* [Working with Binary Logs](working_with_binary_logs.md)


* [Restoring Individual Tables](restoring_individual_tables.md)


* [LRU dump backup](lru_dump.md)


* [Streaming Backups](backup.streaming.md)


* [Encrypting Backups](backup.encrypting.md)


* [`FLUSH TABLES WITH READ LOCK` option](flush-tables-with-read-lock.md)


* [Accelerating the backup process](backup.accelerating.md)


* [Point-In-Time recovery](point-in-time-recovery.md)


* [Making Backups in Replication Environments](replication.md)


* [Store backup history on the server](backup.history.md)


## Implementation


* [Implementation Details](implementation_details.md)


* [*xtrabackup* Exit Codes](xtrabackup_exit_codes.md)


## References


* [The **xtrabackup** Option Reference](xbk_option_reference.md)
