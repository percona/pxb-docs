> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-xtrabackup/9.7/llms.txt).

# Percona XtraBackup 9.7 Documentation

This documentation is for the latest release: [Percona XtraBackup 9.7.2-2](https://docs.percona.com/percona-xtrabackup/9.7/release-notes/9.7.2-2.md) release notes.

Percona XtraBackup is an open source hot backup utility for MySQL-based servers that keep your database fully available during planned maintenance windows.

Whether it is a 24x7 highly loaded server or a low-transaction-volume Percona XtraBackup is designed to make backups seamless without disrupting the performance of the server in a production environment. Percona XtraBackup (PXB) is a 100% open source backup solution with [commercial support](https://www.percona.com/services/expert-support/) available for organizations who want to benefit from comprehensive, responsive, and cost-flexible database support for MySQL.

## Percona XtraBackup features

Taking your backup with Percona XtraBackup is easy. Follow our documentation guides, and you’ll be set up quickly.

## Quickstart guide

Get started quickly with our Quickstart guide.

[Quickstart guide](https://docs.percona.com/percona-xtrabackup/9.7/quickstart-overview.md)

### Installation guides

Find the best installation solution with our step-by-step installation instructions.

[Installation instructions](https://docs.percona.com/percona-xtrabackup/9.7/installation.md)

## Binaries

Learn about the Percona XtraBackup binaries: xtrabackup, xbcloud, xbcrypt, and xbstream.

[Binaries](https://docs.percona.com/percona-xtrabackup/9.7/binaries-overview.md)

### Backup management

Learn about the different types of backups and how to take them.

[Backup management](https://docs.percona.com/percona-xtrabackup/9.7/backup-overview.md)

## Supported storage engines

Percona XtraBackup 9.7 supports backing up data from the following storage engines only on MySQL 9.7 and Percona Server for MySQL 9.7, including Percona XtraDB Cluster 9.7:

- InnoDB
- XtraDB
- MyISAM
- MyRocks

It does not support backups on MySQL 8.0 or 8.4 servers.

Percona XtraBackup 9.7 can take full backups of databases using the MyRocks storage engine.

### Limitations

Percona XtraBackup 9.7 does not support backing up of databases created in versions before 9.7 of MySQL, Percona Server for MySQL or Percona XtraDB Cluster.

Incremental backups for MyRocks are not optimized. Each time you run an incremental backup, all MyRocks files are copied, even if they haven’t changed since the previous backup.

InnoDB tables are locked while copying non-InnoDB data.

Percona XtraBackup 9.7.2-2 creates invalid backups of Percona Server for MySQL 9.7.4-4 databases with vector indexes. Use Percona XtraBackup 9.7.2-3 or higher.

See also

[Dependency compatibility and limitations](https://docs.percona.com/percona-xtrabackup/9.7/update-curl-utility.md)

[Server version and backup version comparison](https://docs.percona.com/percona-xtrabackup/9.7/server-backup-version-comparison.md)
