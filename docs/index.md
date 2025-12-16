
# Percona XtraBackup {{vers}} Documentation

!!! note ""

    This documentation is for the latest release: [Percona XtraBackup {{release}}](release-notes/{{release}}.md) release notes.

Percona XtraBackup is an open source hot backup utility for
MySQL-based servers that keep your database fully available during planned maintenance windows.

Whether it is a 24x7 highly loaded server or a low-transaction-volume
Percona XtraBackup is designed to make backups seamless without disrupting the performance of the server in a production environment. Percona XtraBackup (PXB) is a 100% open source backup solution with [commercial support](https://www.percona.com/mysql-support/) available for organizations who want to benefit from comprehensive, responsive, and cost-flexible database support for MySQL.

## Percona XtraBackup Pro releases

--8<--- "pro-build-announcement.md"

[Percona XtraBackup Pro](pxb-pro.md){.md-button}

## Percona XtraBackup features

Taking your backup with Percona XtraBackup is easy. Follow our documentation guides, and you’ll be set up in quickly.

<div data-grid markdown><div data-banner markdown>

## :material-progress-download: Quickstart guide { .title }

Get started quickly with our Quickstart guide.

[Quickstart guide](quickstart-overview.md){ .md-button }

</div><div data-banner markdown>

### :material-progress-download: Installation guides { .title }

Find the best installation solution with our step-by-step installation instructions.

[Installation instructions](installation.md){ .md-button }

</div><div data-banner markdown>

## :fontawesome-solid-gears: Binaries { .title }

Learn about the Percona XtraBackup binaries: xtrabackup, xbcloud, xbcrypt, and xbstream.

[Binaries](binaries-overview.md){.md-button}

</div><div data-banner markdown>

### :material-backup-restore: Backup management { .title }

Learn about the different types of backups and how to take them.

[Backup management](backup-overview.md){ .md-button }

</div>
</div>

## Supported storage engines

Percona XtraBackup {{vers}} supports backing up data from the following storage engines only on MySQL {{vers}} and Percona Server for MySQL {{vers}}, including Percona XtraDB Cluster {{vers}}:

* InnoDB
	
* XtraDB
	
* MyISAM
	
* MyRocks

It does not support backups on MySQL 8.0 or 9.x servers.

Percona XtraBackup {{vers}} can take full backups of databases using the MyRocks storage engine. 

### Limitations

Percona XtraBackup {{vers}} does not support backing up of databases
created in versions before {{vers}} of MySQL, Percona Server for MySQL or
Percona XtraDB Cluster.

Incremental backups for MyRocks are not optimized. Each time you run an incremental backup, all MyRocks files are copied, even if they haven’t changed since the previous backup.

InnoDB tables are locked while copying non-InnoDB data.

!!! See also

    [Dependency compatibility and limitations](update-curl-utility.md)