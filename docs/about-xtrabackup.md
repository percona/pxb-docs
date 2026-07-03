# About Percona XtraBackup

This page gives a short overview of Percona XtraBackup: what it is, why use it, and where to go next in the docs.

## What is Percona XtraBackup?

Percona XtraBackup is the an open source, free MySQL hot backup
software that performs non-blocking backups for InnoDB and XtraDB
databases.

Percona XtraBackup makes hot backups for Percona Server for MySQL and MySQL-compatible servers. It supports streaming, compressed, and incremental backups, and encryption.

## Benefits

With Percona XtraBackup you can:

* Complete a backup quickly and reliably

* Process transactions uninterrupted during a backup

* Save on disk space and network bandwidth

* Verify backup automatically

## Support

Percona’s enterprise-grade commercial [MySQL Support :octicons-link-external-16:](https://www.percona.com/services/expert-support/) contracts include support for Percona XtraBackup. We recommend support for critical production deployments.

## Supported storage engines

Percona XtraBackup can back up data from InnoDB, XtraDB, MyISAM, and MyRocks tables on MySQL {{vers}} servers as well as Percona Server for MySQL {{vers}}.

Percona XtraBackup supports the MyRocks storage engine. Percona XtraBackup copies all MyRocks files on every backup. Incremental backups for MyRocks are not truly incremental: each one copies all MyRocks files, whether or not those files were already in a full or earlier incremental backup.

## Where to go next

| If you want to… | Go to |
|-----------------|--------|
| Get running quickly | [Quickstart guide](quickstart-overview.md) |
| Install on your system | [Installation](installation.md) |
| Understand how backups work | [How Percona XtraBackup works](how-xtrabackup-works.md) |
| See backup types and workflows | [Backup overview](backup-overview.md) |
| Use the backup tools (xtrabackup, xbcloud, xbcrypt, xbstream) | [Binaries overview](binaries-overview.md) |
