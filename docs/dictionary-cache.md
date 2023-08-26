<!---
    assumes the Percona XtraBackup 8.0.33-28 changes are default in 8.1
    --->

# Dictionary cache 

Percona XtraBackup is based on how [`crash recovery`](https://dev.mysql.com/doc/refman/8.0/en/glossary.html#glos_crash_recovery) works. Percona XtraBackup copies the InnoDB data files, which results in data that is internally inconsistent; then the `prepare` phase performs crash recovery on the files to make a consistent, usable database again.

The `--prepare` phase has the following operations:

* Applies the redo log
* Applies the undo log

As a physical operation, the changes from the redo log modifications are applied to a page. In the redo log operation, there is no concept of row or transaction. The redo apply operation does not make the database consistent with a transaction. An uncommitted transaction can be flushed or written to the redo log by the server. Percona XtraBackup applies changes recorded in the redo log.

Percona XtraBackup physically modifies a specific offset of a page within a tablespace (IBD file) when applying a redo log. 

As a logical operation, Percona XtraBackup applies the undo log on a specific row. When the redo log completes, XtraBackup uses the undo log to roll back changes from uncommitted transactions during the backup.

## Undo log

There are two types of undo log records:

* INSERT
* UPDATE

An undo log record contains a `table_id`. Percona XtraBackup uses this `table_id` to find the table definition, and then uses that information to parse the records on an index page. The transaction rollback reads the undo log records and applies the changes. 

After initializing the data dictionary engine and the data dictionary cache, the storage engine can request the `table_id` and uses this ID to fetch the table schema. An index search tuple (key) is created from the table schema and key fields from the undo log record. The server finds the record using the search tuple (key) and performs the undo operation.

For example, InnoDB uses the `table_id` (also known as the `se_private_id`) for a table definition. Percona XtraBackup does not behave like a server and does not have access to the data dictionary. XtraBackup initializes the InnoDB engine and uses the `InnoDB table object` (`dict_table_t`) when needed. XtraBackup relies on Serialized Dictionary Information (SDI) that is stored in the tablespace. SDI is a JSON representation of a table.

## Version changes
<!---
Prior to Percona XtraBackup 8.0.33-28, XtraBackup loads the SDI from every `.IBD` file and all tables into cache as non-evictable. Making the tables non-evictable essentially disables the LRU cache. Every table remains in memory until the operation ends. 

This method has the following issues:

* Unnecessary IO operations from reading SDI pages to load the tables that are not required for rollback
* All tables loaded into the cache increases the time required in the `--prepare` phase
* Unnecessary tables can lead to out-of-memory errors
* Huge number of tables and IBD files may cause an exit in the `--prepare` phase
--->
In Percona XtraBackup 8.1, tables are loaded as `evictable`. XtraBackup scans the B-tree index of the data dictionary tables `mysql.indexes` and `mysql.index_partitions` to establish a relationship between the `table_id` and the `tablespace(space_id)`. XtraBackup uses this relationship during transaction rollback. XtraBackup does not load user tables unless there is a transaction rollback on them.

A background thread or a Percona XtraBackup main thread handles the cache eviction when the cache size limit is reached.

This  design provides the following benefits during the `--prepare` phase:

* Uses less memory
* Uses less IO
* Improves the time taken in the `--prepare` phase
* Completes successfully, even if the `--prepare` phase has a huge number of tables
* Completes the Percona XtraDB Cluster SST process faster

