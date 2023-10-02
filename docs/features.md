# Percona XtraBackup features

The following is a short list of the Percona XtraBackup features:

* Creates hot InnoDB backups without pausing your database

* Makes incremental backups of MySQL

* Streams compressed MySQL backups to another server

* Moves tables between MySQL servers on-line

* Creates new MySQL replication replicas easily

* Backs up MySQL without adding load to the server

* Performs throttling based on the number of IO operations per second

* Skips secondary index pages and recreates them when a compact backup is prepared

* Exports individual tables from a full InnoDB backup

Percona XtraBackup automatically uses backup locks, a lightweight alternative to `FLUSH TABLES WITH READ LOCK` available in Percona Server, to copy non-InnoDB data. This operation avoids blocking DML queries that modify InnoDB tables.

!!! admonition "See also"

    [How Percona XtraBackup works](how-xtrabackup-works.md)
