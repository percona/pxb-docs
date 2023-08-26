# Limitations

Percona XtraBackup 8.1 does not support making backups of databases
created in versions prior to 8.1 of MySQL, Percona Server for MySQL or
Percona XtraDB Cluster.

## Additional information

The InnoDB tables are locked while copying non-InnoDB data.
