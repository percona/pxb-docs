# Glossary

## .CSM

Each table with the CSV Storage Engine has `.CSM` file which contains the metadata of it.

## .CSV

Each table with the CSV Storage engine has `.CSV` file which contains the data of it (which is a standard Comma Separated Value file).

## .exp

Files with the `.exp` extension are created by Percona XtraBackup per each InnoDB tablespace when the [`--export`](xtrabackup-option-reference.md#–-export) option is used on prepare. See [restore individual tables](restore-individual-tables.md).

## .frm

For each table, the server will create a file with the `.frm` extension containing the table definition (for all storage engines).

## General availability (GA)

A finalized version of the product which is made available to the general public. It is the final stage in the software release cycle.

## .ibd

On a multiple tablespace setup ([innodb\_file\_per\_table] enabled), MySQL will store each newly created table on a file with a `.ibd` extension.

## .MRG

Each table using the MERGE storage engine, besides of a `.frm` file, 
will have `.MRG` file containing the names of the MyISAM tables 
associated with it.

## .MYD

Each MyISAM table has `.MYD` (MYData) file which contains the data on it.

## .MYI

Each MyISAM table has `.MYI` (MYIndex) file which contains the table’s indexes.

## .opt

MySQL stores options of a database (like charset) in a file with a `.opt` extension in the database directory.

## .par

Each partitioned table has `.par` file which contains metadata about the partitions.

## .TRG

The file contains the triggers associated with a table, for example, `\mytable.TRG`. With the `.TRN` file, they represent all the trigger definitions.

## .TRN

The file contains the names of triggers that are associated with a table, for example, `\mytable.TRN`. With the `.TRG` file, they represent all the trigger definitions.

## backup

The process of copying data or tables to be stored in a different location.

## compression

The method that produces backups in a reduced size.

## configuration file

The file that contains the server startup options.

## crash

An unexpected shutdown which does not allow the normal server shutdown cleanup activities.

## crash recovery

The actions that occur when MySQL is restarted after a crash.

## data dictionary

The metadata for the tables, indexes, and table columns stored in the InnoDB system tablespace.

## datadir

The directory in which the database server stores its data files. Most Linux distribution use `/var/lib/mysql` by default.

## full backup

A backup that contains the complete source data from an instance.

## ibdata

The default prefix for tablespace files. For example, `ibdata1` is a 10MB auto-extensible file that MySQL creates for a shared tablespace by default.

## incremental backup

A backup stores data from a specific point in time.

## InnoDB

Storage engine which provides ACID-compliant transactions and foreign 
key support, among others improvements over MyISAM. It is the default 
engine for MySQL as of the {{release}} series.

## innodb\_buffer\_pool\_size

The size in bytes of the memory buffer to cache data and indexes of InnoDB’s tables. This aims to reduce disk access to provide better performance. 

> \[mysqld\]<br/>
> innodb\_buffer\_pool\_size=8MB

## innodb\_data\_home\_dir

The directory (relative to `datadir`) where the database server stores 
the files in a shared tablespace setup. This option does not affect the location of `innodb\_file\_per\_table`. For example:

> \[mysqld\]<br/>
> innodb\_data\_home\_dir = ./

## innodb\_data\_file\_path

Specifies the names, sizes and location of shared tablespace files:

> \[mysqld\]<br/>
> innodb\_data\_file\_path=ibdata1:50M;ibdata2:50M:autoextend

## innodb\_file\_per\_table

By default, InnoDB creates tables and indexes in a [file-per-tablespace](https://dev.mysql.com/doc/refman/8.1/en/innodb-file-per-table-tablespaces.html). If the `innodb_file_per_table` variable is disabled, you can enable the variable in your configuration file:

> \[mysqld\]<br/>
> innodb\_file\_per\_table <br/>
> or <br/>
> start the server with `--innodb_file_per_table`.

## innodb\_log\_group\_home\_dir

Specifies the location of the InnoDB log files:

> \[mysqld\]<br/>
> innodb\_log\_group\_home=/var/lib/mysql

## logical backup

A backup which contains a set of SQL statements. The statements can be used to recreate the databases.

## LSN

Each InnoDB page contains a log sequence number(LSN). The LSN is the system version number for the database. Each page’s LSN shows how recently it was changed.

## my.cnf

The database server’s main configuration file. Most Linux distributions place it as `/etc/mysql/my.cnf` or `/etc/my.cnf`, but the location and name depends on the particular installation. Note that this method is not the only way of configuring the server, some systems rely on the command options.

## MyISAM

The MySQL default storage engine until version 5.5. It doesn’t fully 
support transactions but in some scenarios may be faster than InnoDB. 
Each table is stored on disk in 3 files: `.frm`, `.MYD`, `.MYI`.

## physical backup

A backup that copies the data files.

## point in time recovery

This method restores the data into the state it was at any selected point of time.

## prepared backup

A consistent set of backup data that is ready to be restored.

## restore

Copies the database backups taken using the backup command to the original location or a different location. A restore returns data that has been either lost, corrupted, or stolen to the original condition at a specific point in time.

## Tech preview

A tech preview item can be a feature, a variable, or a value within a variable. Before using this feature in production, we recommend that you test restoring production from physical backups in your environment and also use an alternative backup method for redundancy. A tech preview item is included in a release for users to provide feedback. The item is either updated and released as [general availability(GA)](#general-availability-ga) or removed if not useful. The functionality can change from tech preview to GA.

## xbcrypt

To support the encryption and the decryption of the backups. This utility has been modeled after the xbstream binary to perform encryption and decryption outside Percona XtraBackup.

## xbstream

To support simultaneous compression and streaming, Percona XtraBackup uses the xbstream format. For more information see [xbstream](xbstream-binary-overview.md)

## XtraDB

Percona XtraDB is an enhanced version of the InnoDB storage engine, designed to better scale on modern hardware. Percona XtraDB includes features which are useful in a high performance environment. It is fully backward-compatible, and is a drop-in replacement for the standard InnoDB storage engine. For more information, see [The Percona XtraDB Storage Engine](https://www.percona.com/doc/percona-server/8.1/percona-xtradb.html).

## Zstandard (ZSTD)

`ZSTD` is a fast lossless compression algorithm that targets real-time compression scenarios and better compression ratios.


