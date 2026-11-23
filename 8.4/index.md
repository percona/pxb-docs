> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-xtrabackup/8.4/llms.txt).

# Percona XtraBackup 8.4 Documentation

This documentation is for the latest release: [Percona XtraBackup 8.4.0-8](https://docs.percona.com/percona-xtrabackup/8.4/release-notes/8.4.0-8.html) release notes.

Percona XtraBackup is an open source hot backup utility for MySQL-based servers that keep your database fully available during planned maintenance windows.

Whether it is a 24x7 highly loaded server or a low-transaction-volume Percona XtraBackup is designed to make backups seamless without disrupting the performance of the server in a production environment. Percona XtraBackup (PXB) is a 100% open source backup solution with [commercial support](https://www.percona.com/services/expert-support/) available for organizations who want to benefit from comprehensive, responsive, and cost-flexible database support for MySQL.

## Percona XtraBackup features

Taking your backup with Percona XtraBackup is easy. Follow our documentation guides, and you’ll be set up quickly.

## Quickstart guide

Get started quickly with our Quickstart guide.

[Quickstart guide](https://docs.percona.com/percona-xtrabackup/8.4/quickstart-overview.html)

### Installation guides

Find the best installation solution with our step-by-step installation instructions.

[Installation instructions](https://docs.percona.com/percona-xtrabackup/8.4/installation.html)

## Binaries

Learn about the Percona XtraBackup binaries: xtrabackup, xbcloud, xbcrypt, and xbstream.

[Binaries](https://docs.percona.com/percona-xtrabackup/8.4/binaries-overview.html)

### Backup management

Learn about the different types of backups and how to take them.

[Backup management](https://docs.percona.com/percona-xtrabackup/8.4/backup-overview.html)

## Supported storage engines

Percona XtraBackup 8.4 supports backing up data from the following storage engines only on MySQL 8.4 and Percona Server for MySQL 8.4, including Percona XtraDB Cluster 8.4:

- InnoDB
- XtraDB
- MyISAM
- MyRocks

It does not support backups on MySQL 8.0 or 9.x servers.

Percona XtraBackup 8.4 can take full backups of databases using the MyRocks storage engine.

### Limitations

Percona XtraBackup 8.4 does not support backing up of databases created in versions before 8.4 of MySQL, Percona Server for MySQL or Percona XtraDB Cluster.

Incremental backups for MyRocks are not optimized. Each time you run an incremental backup, all MyRocks files are copied, even if they haven’t changed since the previous backup.

InnoDB tables are locked while copying non-InnoDB data.

See also

[Dependency compatibility and limitations](https://docs.percona.com/percona-xtrabackup/8.4/update-curl-utility.html)
