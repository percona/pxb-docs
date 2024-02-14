
# Percona XtraBackup {{vers}} Documentation

!!! note ""

    This documentation is for the latest release: [Percona XtraBackup {{release}}](release-notes/{{release}}.md) release notes.
    This is an Innovation release. This type of release is only supported for a short time and is designed to be used in an environment with fast upgrade cycles. Developers and DBAs are exposed to the latest features and improvements.

Percona XtraBackup is an open source hot backup utility for
MySQL-based servers that keep your database fully available during planned maintenance windows.

Whether it is a 24x7 highly loaded server or a low-transaction-volume
Percona XtraBackup is designed to make backups seamless without disrupting the performance of the server in a production environment. Percona XtraBackup (PXB) is a 100% open source backup solution with [commercial support](https://www.percona.com/mysql-support/) available for organizations who want to benefit from comprehensive, responsive, and cost-flexible database support for MySQL.

This is an Innovation release. This type of release is only supported for a short time and is designed to be used in an environment with fast upgrade cycles. Developers and DBAs are exposed to the latest features and improvements.

Taking your backup with Percona XtraBackup is easy. Follow our documentation guides, and you’ll be set up in quickly.

<div data-grid markdown><div data-banner markdown>

## :material-progress-download: Quickstart guide { .title }

Get started quickly with our Quickstart guide.

[Quickstart guide :material-arrow-right:](quickstart-overview.md){ .md-button }

</div><div data-banner markdown>

### :material-progress-download: Installation guides { .title }

Find the best installation solution with our step-by-step installation instructions.

[Installation instructions :material-arrow-right:](installation.md){ .md-button }

</div><div data-banner markdown>

## :fontawesome-solid-gears: Binaries { .title }

Learn about the Percona XtraBackup binaries: xtrabackup, xbcloud, xbcrypt, and xbstream.

[Binaries :material-arrow-right:](binaries-overview.md){.md-button}

</div><div data-banner markdown>

### :material-backup-restore: Backup management { .title }

Learn about the different types of backups and how to take them.

[Backup management :material-arrow-right:](backup-overview.md){ .md-button }

</div>
</div>

## Supported storage engines

Percona XtraBackup can back up data from InnoDB, XtraDB,
MyISAM, MyRocks tables on MySQL {{vers}} servers and Percona Server for MySQL with XtraDB, Percona Server for MySQL {{vers}}, and Percona XtraDB Cluster {{vers}}.

Percona XtraBackup {{vers}} supports the MyRocks storage engine. An incremental backup on the MyRocks storage engine does not determine if an earlier full or incremental backup contains duplicate files. Percona XtraBackup copies all MyRocks files each time it takes a backup.

### Limitations

Percona XtraBackup {{vers}} does not support making backups of databases
created in versions before {{vers}} of MySQL, Percona Server for MySQL or
Percona XtraDB Cluster.

<script>
    (function(h,o,t,j,a,r){
        h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
        h._hjSettings={hjid:3857510,hjsv:6};
        a=o.getElementsByTagName('head')[0];
        r=o.createElement('script');r.async=1;
        r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
        a.appendChild(r);
    })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
</script>

