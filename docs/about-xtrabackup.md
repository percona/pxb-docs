# About Percona XtraBackup

*Percona XtraBackup* is the world’s only open source, free *MySQL* hot backup
software that performs non-blocking backups for *InnoDB* and *XtraDB*
databases. 

With *Percona XtraBackup*, you can achieve the following benefits:

* Backups that complete quickly and reliably

* Uninterrupted transaction processing during backups

* Savings on disk space and network bandwidth

* Automatic backup verification

* Higher uptime due to faster restore time

*Percona XtraBackup* makes *MySQL* hot backups for all versions of Percona
Server for MySQL, and *MySQL*. It performs streaming, compressed, and incremental *MySQL*
backups.

!!! important

    **Percona XtraBackup** 2.4 supports *MySQL* and *Percona Server for MySQL* 
    5.6 and 5.7 databases. Due to changes in the MySQL redo log and data 
    dictionary formats, the **Percona XtraBackup** 8.0.x versions are only 
    compatible with *MySQL* 8.0.x, *Percona Server for MySQL* 8.0.x, and 
    compatible versions.

Percona’s enterprise-grade commercial [MySQL Support](http://www.percona.com/mysql-support/) contracts include support for *Percona
XtraBackup*. We recommend support for critical production deployments. Percona XtraDB Backup supports encryption.

## Supported storage engines

*Percona XtraBackup* can back up data from *InnoDB*, *XtraDB*,
*MyISAM*, and MyRocks tables on *MySQL* 8.0 servers as well as *Percona Server for MySQL*
with *XtraDB*, [*Percona Server for MySQL* 8.0](https://docs.percona.com/percona-server/8.0/), and [*Percona XtraDB Cluster* 8.0](https://docs.percona.com/percona-xtradb-cluster/8.0/).

!!! admonition "Version updates"
   
    Version 8.0.6 and later supports the MyRocks storage engine. 
    An incremental backup on the MyRocks storage engine does not 
    determine if an earlier full or incremental backup 
    contains the same files. **Percona XtraBackup** copies all 
    MyRocks files each time it takes a backup.
    **Percona 
    XtraBackup** does not support the TokuDB storage engine.

!!! admonition "See also"
   
    [Percona TokuBackup](https://docs.percona.com/percona-server/latest/tokudb/toku_backup.html)

## Limitations

*Percona XtraBackup* 8.0 does not support making backups of databases
created in versions prior to 8.0 of *MySQL*, *Percona Server for MySQL* or
*Percona XtraDB Cluster*. As the changes that *MySQL* 8.0 introduced
in *data dictionaries*, *redo log* and *undo log* are incompatible
with previous versions, it is currently impossible for *Percona XtraBackup* 8.0 to also support versions prior to 8.0.

Due to changes in MySQL 8.0.20 released by Oracle at the end of April 2020,
*Percona XtraBackup* 8.0, up to version 8.0.11, is not compatible with MySQL version 8.0.20 or
higher, or Percona products that are based on it: Percona Server for MySQL and
Percona XtraDB Cluster.

For more information, see [Percona XtraBackup 8.x and MySQL 8.0.20](https://www.percona.com/blog/2020/04/28/percona-xtrabackup-8-x-and-mysql-8-0-20/)

## What are the features of Percona XtraBackup?

Here is a short list of the Percona XtraBackup features. See the documentation
for more.


* Create hot InnoDB backups without pausing your database


* Make incremental backups of MySQL


* Stream compressed MySQL backups to another server


* Move tables between MySQL servers on-line


* Create new MySQL replication replicas easily


* Backup MySQL without adding load to the server


* Percona XtraBackup performs throttling based on the number of IO operations per second


* Percona XtraBackup skips secondary index pages and recreates them when a compact backup is prepared


* Percona XtraBackup can export individual tables even from a full backup, regardless of the InnoDB version


* Backup locks is a lightweight alternative to `FLUSH TABLES WITH READ LOCK` available in Percona Server. Percona XtraBackup uses them automatically to copy non-InnoDB data to avoid blocking DML queries that modify InnoDB tables.

!!! admonition "See also"
   
    [How Percona XtraBackup works](how-xtrabackup-works.md)

### Additional information

The *InnoDB* tables are locked while copying non-*InnoDB* data.
