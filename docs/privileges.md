# Connection and privileges needed

Percona XtraBackup needs to be able to connect to the database server and
perform operations on the server and the datadir when creating a
backup, when preparing in some scenarios and when restoring it. In order to do
so, there are privileges and permission requirements on its execution that
must be fulfilled.

Privilege refers to the operations that a system user is permitted to do in
the database server. They are set at the database server and only apply to
users in the database server.

Permissions are those which permits a user to perform operations on the system,
like reading, writing or executing on a certain directory or start/stop a
system service. They are set at a system level and only apply to system
users.

When xtrabackup is used, there are two actors involved: the user invoking the
program - a system user - and the user performing action in the database
server - a database user. Note that these are different users in different
places, even though they may have the same username.

All the invocations of xtrabackup in this documentation assume that the system
user has the appropriate permissions, and you are providing the relevant options
for connecting the database server - besides the options for the action to be
performed - and the database user has adequate privileges.

## Connect to the server

The database user used to connect to the server and its password are specified
by the `--user` and `--password` option:

```{.bash data-prompt="$"}
$ xtrabackup --user=DVADER --password=14MY0URF4TH3R --backup \
--target-dir=/data/bkps/
```

If you don’t use the `--user` option, Percona XtraBackup will assume
the database user whose name is the system user executing it.

### Other connection options

According to your system, you may need to specify one or more of the following
options to connect to the server:

| Option | Description                                                  |
|------------|------------------------------------------------------------------|
| -port      | Use this port when connecting to the database with TCP/IP        |
| -socket    | Use this socket when connecting to the local database.           |
| -host      | Use this host when connecting to the database server with TCP/IP |

These options are passed to the mysql child process without
alteration, see `mysql --help` for details.

!!! note
 
    In case of multiple server instances, the correct connection parameters
    (port, socket, host) must be specified in order for xtrabackup to talk to
    the correct server.

## Privileges needed

Once connected to the server, in order to perform a backup you need
`READ` and `EXECUTE` permissions at a filesystem level in the server’s datadir.

The database user needs the following privileges to back up tables or databases:

* `RELOAD` and `LOCK TABLES` (unless the `--no-lock`
option is specified) in order to run `FLUSH TABLES WITH READ LOCK` and
`FLUSH ENGINE LOGS` prior to start copying the files, and requires this
privilege when [Backup Locks](https://docs.percona.com/percona-server/8.1/backup-locks.html)
are used

* `BACKUP_ADMIN` privilege is needed to query the
performance_schema.log_status table, and run `LOCK INSTANCE FOR BACKUP`,
`LOCK BINLOG FOR BACKUP`, or `LOCK TABLES FOR BACKUP`.

* `REPLICATION CLIENT` in order to obtain the binary log position,

* `CREATE TABLESPACE` in order to import tables (see Restoring Individual Tables),

* `PROCESS` in order to run `SHOW ENGINE INNODB STATUS` (which is
mandatory), and optionally to see all threads which are running on the
server (see FLUSH TABLES WITH READ LOCK option),

* `SUPER` in order to start/stop the replication threads in a replication
environment,

* `CREATE` privilege in order to create the
PERCONA_SCHEMA.xtrabackup_history database and
table,

* `ALTER` privilege in order to upgrade the
PERCONA_SCHEMA.xtrabackup_history database and
table,

* `INSERT` privilege in order to add history records to the
PERCONA_SCHEMA.xtrabackup_history table,

* `SELECT` privilege in order to use
`--incremental-history-name` or
`--incremental-history-uuid` in order for the feature
to look up the `innodb_to_lsn` values in the
PERCONA_SCHEMA.xtrabackup_history table.

* `SELECT` privilege on the [keyring_component_status table](https://dev.mysql.com/doc/refman/8.1/en/performance-schema-keyring-component-status-table.html) to view the attributes and status of the installed keyring component when in use.

* `SELECT` privilege on the [replication_group_members table](https://dev.mysql.com/doc/refman/8.1/en/performance-schema-replication-group-members-table.html) to validate if the instance is part of group replication cluster.

A SQL example of creating a database user with the minimum privileges required to take full backups would be:

```{.bash data-prompt="mysql>"}
mysql> CREATE USER 'bkpuser'@'localhost' IDENTIFIED BY 's3cr%T';
mysql> GRANT BACKUP_ADMIN, PROCESS, RELOAD, LOCK TABLES, REPLICATION CLIENT ON *.* TO 'bkpuser'@'localhost';
mysql> GRANT SELECT ON performance_schema.log_status TO 'bkpuser'@'localhost';
mysql> GRANT SELECT ON performance_schema.keyring_component_status TO bkpuser@'localhost';
mysql> GRANT SELECT ON performance_schema.replication_group_members TO bkpuser@'localhost';
mysql> FLUSH PRIVILEGES;
```

### Query the privileges

To query the privileges that your database user has been granted at the console of the server execute:

```{.bash data-prompt="mysql>"}
mysql> SHOW GRANTS;
```

or for a particular user with:

```{.bash data-prompt="mysql>"}
mysql> SHOW GRANTS FOR 'db-user'@'host';
```

It will display the privileges using the same format as for
the [GRANT statement](https://dev.mysql.com/doc/refman/8.1/en/show-grants.html).

Note that privileges may vary across versions of the server. To list the
exact list of privileges that your server support (and a brief description
of them) execute:

```{.bash data-prompt="mysql>"}
mysql> SHOW PRIVILEGES;
```

!!! admonition "See also"

    [Permissions needed](permissions.md)