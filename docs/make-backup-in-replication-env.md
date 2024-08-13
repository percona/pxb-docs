# Make backups in replication environments

There are options specific to back up from a replication replica.

## The `--slave-info` option

This option is useful when backing up a replication replica server. It prints the
binary log position and name of the source server. It also writes this
information to the `xtrabackup_slave_info` file as a `CHANGE REPLICATION SOURCE TO`
statement.

This option is useful for setting up a new replica for this source.
You can start a replica server with this backup and issue the statement saved in the
`xtrabackup_slave_info` file. More details of this procedure can be found
in How to setup a replica for replication in 6 simple steps with Percona XtraBackup.

## The `--safe-slave-backup` option

In order to assure a consistent replication state, this option stops the replication
SQL thread and waits to start backing up until `Replica_open_temp_tables` in
`SHOW STATUS` is zero. If there are no open temporary tables, the backup will
take place, otherwise the SQL thread will be started and stopped until there are
no open temporary tables. The backup will fail if `Replica_open_temp_tables`
does not become zero after `--safe-slave-backup-timeout`
seconds (defaults to 300 seconds). The replication SQL thread will be restarted when
the backup finishes.

!!! note

    Using a safe-slave-backup option stops the SQL replica thread before copying the InnoDB files.

Using this option is always recommended when taking backups from a replica server.

!!! warning
   
    Make sure your replica is a true replica of the source before using it as a
    source for backup. A good tool to validate a replica is [pt-table-checksum].

[pt-table-checksum]: https://docs.percona.com/percona-toolkit/pt-table-checksum.html

