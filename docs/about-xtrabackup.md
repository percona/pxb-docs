# About Percona XtraBackup

Percona XtraBackup is the world’s only open source, free MySQL hot backup
software that performs non-blocking backups for InnoDB and XtraDB
databases. 

Percona XtraBackup has the following benefits:

* Complete a backup quickly and reliably

* Process transactions uninterrupted during a back up

* Save on disk space and network bandwidth

* Verify backup automatically

Percona XtraBackup makes hot backups for Percona Server for MySQL and MySQL, takes streaming, compressed, and incremental MySQL backups, and supports encryption.

Percona’s enterprise-grade commercial [MySQL Support](http://www.percona.com/mysql-support/) contracts include support for Percona XtraBackup. We recommend support for critical production deployments.

## Supported storage engines

Percona XtraBackup can back up data from InnoDB, XtraDB,
MyISAM, and MyRocks tables on MySQL {{release}} servers as well as Percona Server for MySQL
with XtraDB, and Percona XtraDB Cluster {{release}}.

Percona XtraBackup supports the MyRocks storage engine. An incremental backup on the MyRocks storage engine does not determine if an earlier full or incremental backup contains the same files. Percona XtraBackup copies all MyRocks files each time it takes a backup. Percona XtraBackup does not support the TokuDB storage engine.




