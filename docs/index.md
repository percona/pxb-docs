
# Percona XtraBackup {{release}} Documentation

!!! note ""

    This documentation is for the latest release: Percona XtraBackup {{release}} ([Release Notes](release-notes/{{release}}.md)).

Percona XtraBackup is an open source hot backup utility for
MySQL-based servers that keep your database fully available during planned maintenance windows.

Whether it is a 24x7 highly loaded server or a low-transaction-volume
Percona XtraBackup is designed to make backups seamless
without disrupting the server's performance in a production
environment. Percona XtraBackup (PXB) is a 100% open source backup solution with [commercial support](https://www.percona.com/mysql-support/) available for organizations who want to benefit from comprehensive, responsive, and cost-flexible database support for MySQL.

## Supported storage engines

Percona XtraBackup can back up data from InnoDB, XtraDB,
MyISAM, MyRocks tables on the following servers:

* MySQL {{vers}}
* Percona Server for MySQL {{release}}

Percona XtraBackup {{release}} supports the MyRocks storage engine. An incremental backup on the MyRocks storage engine does not determine if an earlier full or incremental backup contains duplicate files. Percona XtraBackup copies all MyRocks files each time it takes a backup.

### Limitations

Percona XtraBackup {{release}} does not support making backups of databases
created in versions before {{release}} Innovation series of MySQL, Percona Server for MySQL or
Percona XtraDB Cluster.


