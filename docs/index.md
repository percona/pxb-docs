# Percona XtraBackup - Documentation

!!! note ""

    This documentation is for the latest release: Percona XtraBackup {{release}} ([Release Notes](release-notes/2.4/{{release}}.md)).

*Percona XtraBackup* is an open-source hot backup utility for *MySQL* - based
servers that does not lock your database during the backup. It can back up data
from *InnoDB*, XtraDB, and *MyISAM* tables on *MySQL* 5.1 , 5.5, 5.6 and 5.7 servers, as well as Percona Server with XtraDB.

!!! note

    Support for InnoDB 5.1 builtin has been removed in *Percona XtraBackup* 2.1

For a high-level overview of many of its advanced features, including a feature
comparison, please see [About Percona XtraBackup](intro.md).

Whether it is a 24x7 highly loaded server or a low-transaction-volume
environment, *Percona XtraBackup* is designed to make backups a seamless
procedure without disrupting the performance of the server in a production
environment. [Commercial support contracts are available](https://www.percona.com/mysql-support/).

!!! important

    Percona XtraBackup 2.4 does not support making backups of databases created in *MySQL 8.0*, *Percona Server for MySQL 8.0*, or *Percona XtraDB Cluster 8.0*. Use Percona XtraBackup 8.0 for the version 8.0 databases.

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