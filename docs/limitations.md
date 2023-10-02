# Limitations

Percona XtraBackup {{release}} does not support making backups of databases
created in versions prior to {{release}} of MySQL, Percona Server for MySQL or
Percona XtraDB Cluster.

### Additional information

The InnoDB tables are locked while copying non-InnoDB data.
