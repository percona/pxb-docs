# Store backup history on the server

*Percona XtraBackup* supports storing the backups history on the server. Storing backup history on
the server was implemented to provide users with additional information about
backups that are being taken. Backup history information will be stored in the
`PERCONA_SCHEMA.XTRABACKUP_HISTORY` table.

To use this feature the following options are available:

* `--history` =<name> : This option enables the history
feature and allows the user to specify a backup series name that will be
placed within the history record.

* `--incremental-history-name` =<name> : This option allows an
incremental backup to be made based on a specific history series by
name. *xtrabackup* will search the history table looking for the most recent
(highest `to_lsn`) backup in the series and take the `to_lsn` value to use
as it’s starting lsn. This is mutually exclusive with
`--incremental-history-uuid`, `--incremental-basedir` and
`--incremental-lsn` options. If no valid LSN can be found
(no series by that name) *xtrabackup* will return with an error.

* `--incremental-history-uuid` =<uuid> : Allows an incremental backup to
be made based on a specific history record identified by UUID. *xtrabackup*
will search the history table looking for the record matching UUID and take
the `to_lsn` value to use as it’s starting LSN. This options is mutually
exclusive with `--incremental-basedir`, `--incremental-lsn`
and `--incremental-history-name` options. If no valid LSN can be found
(no record by that UUID or missing `to_lsn`), *xtrabackup* will return
with an error.

!!! note
   
    Backup that’s currently being performed will **NOT** exist in the
    xtrabackup_history table within the resulting backup set as the record will
    not be added to that table until after the backup has been taken.

If you want access to backup history outside of your backup set in the case of
some catastrophic event, you will need to either perform a `mysqldump`,
partial backup or `SELECT` \* on the history table after *xtrabackup*
completes and store the results with you backup set.

For the necessary privileges, see [Permissions and Privileges Needed](privileges.md).

## Store backup history on a different server

### Version changes

Percona XtraBackup 9.7.2-2 introduces the `--history-*` options to store the backup history on a different server.

### Overview

By default, Percona XtraBackup writes the history record to the server you back up. The write fails if that server does not accept writes, for example, a replica or a secondary member of a single-primary Group Replication cluster with `super_read_only` enabled. In this case, the server returns error 1290 and does not store the record.

To write the history record to another, writable server, add one or more `--history-*` options that describe the connection to that server:

| Option | Description | Default |
| ------ | ----------- | ------- |
| [`--history-host`](xtrabackup-option-reference.md#history-host) | Host of the history server | Value of `--host` |
| [`--history-port`](xtrabackup-option-reference.md#history-port) | TCP/IP port of the history server | Value of `--port` |
| [`--history-socket`](xtrabackup-option-reference.md#history-socket) | UNIX socket of the history server | Value of `--socket`, if you do not set `--history-host` |
| [`--history-user`](xtrabackup-option-reference.md#history-user) | User account on the history server | Value of `--user` |
| [`--history-password`](xtrabackup-option-reference.md#history-password) | Password of the history user | Value of `--password`, if you do not set `--history-user` |
| [`--history-ssl-mode`](xtrabackup-option-reference.md#history-ssl-mode) | Security state of the connection | Value of `--ssl-mode` |
| [`--history-ssl-ca`](xtrabackup-option-reference.md#history-ssl-ca) | CA file in PEM format | Value of `--ssl-ca` |
| [`--history-ssl-capath`](xtrabackup-option-reference.md#history-ssl-capath) | Directory of CA certificates | Value of `--ssl-capath` |
| [`--history-ssl-cert`](xtrabackup-option-reference.md#history-ssl-cert) | X509 certificate in PEM format | Value of `--ssl-cert` |
| [`--history-ssl-key`](xtrabackup-option-reference.md#history-ssl-key) | X509 key in PEM format | Value of `--ssl-key` |

If you do not set an option, Percona XtraBackup takes the value of the matching connection option for the server you back up, with the following exceptions:

* If you set `--history-host`, Percona XtraBackup ignores the `--socket` value, because that socket belongs to the server you back up.

* If you set `--history-user`, Percona XtraBackup ignores the `--password` value. Set `--history-password` for the history user.

* Percona XtraBackup treats the `--history-ssl-*` options as a group. If you set any of these options, Percona XtraBackup uses only the `--history-ssl-*` values and ignores all `--ssl-*` values for the history connection.

* If you set `--history-ssl-ca` or `--history-ssl-capath` without `--history-ssl-mode`, Percona XtraBackup uses the `VERIFY_CA` SSL mode for the history connection.

The following example backs up a read-only replica and stores the history record on the source server:

```bash
xtrabackup --backup --target-dir=/backups/full \
  --user=bkpuser --password=<backup_password> --socket=/var/run/mysqld/mysqld.sock \
  --history=nightly \
  --history-host=source.example.com --history-port=3306 \
  --history-user=history_user --history-password=<history_password>
```

Percona XtraBackup uses the history server only to store and read the history record. Percona XtraBackup runs all other backup operations, such as locks and redo log copying, on the server you back up.

The [`--incremental-history-name`](xtrabackup-option-reference.md#incremental-history-name) and [`--incremental-history-uuid`](xtrabackup-option-reference.md#incremental-history-uuid) options also read from the history server. For incremental backups, pass the same `--history-*` options so that Percona XtraBackup reads the base LSN from the server that stores the records:

```bash
xtrabackup --backup --incremental --target-dir=/backups/inc1 \
  --user=bkpuser --password=<backup_password> --socket=/var/run/mysqld/mysqld.sock \
  --incremental-history-name=nightly \
  --history-host=source.example.com --history-port=3306 \
  --history-user=history_user --history-password=<history_password>
```

### Requirements and behavior

* The `--history-*` options require [`--history`](xtrabackup-option-reference.md#history), [`--incremental-history-name`](xtrabackup-option-reference.md#incremental-history-name), or [`--incremental-history-uuid`](xtrabackup-option-reference.md#incremental-history-uuid). If you set a `--history-*` option without any of these options, Percona XtraBackup reports an error and does not start the backup.

* Percona XtraBackup connects to the history server when the backup starts. If the connection fails, Percona XtraBackup stops the backup before copying any data.

* If Percona XtraBackup cannot apply the TLS settings to the history connection, Percona XtraBackup does not connect to the history server.

* If you set `--history-ssl-ca` or `--history-ssl-capath` and set `--history-ssl-mode` lower than `VERIFY_CA`, Percona XtraBackup prints a warning that the certificate of the history server remains unverified.

* Percona XtraBackup hides the `--history-password` value in the same way as the `--password` value: in the process list, in the log, and in the `tool_command` column of the history record.

### History server privileges

If you store the backup history on a different server with the `--history-*` options, Percona XtraBackup checks the `CREATE`, `ALTER`, `INSERT`, and `SELECT` privileges on `PERCONA_SCHEMA` for the history user on the history server, not for the backup user. The backup user does not need these privileges.

The history user needs the following privileges on the history server:

* `CREATE`, `ALTER`, and `INSERT` on `PERCONA_SCHEMA` to use `--history`. The history user needs the `CREATE` privilege even if the `PERCONA_SCHEMA.xtrabackup_history` table already exists.

* `SELECT` on `PERCONA_SCHEMA.xtrabackup_history` to use `--incremental-history-name` or `--incremental-history-uuid`.

* `SELECT` on `performance_schema.replication_group_members`.

To create a history user with the minimum privileges, run the following statements on the history server:

```sql
CREATE USER 'history_user'@'%' IDENTIFIED BY '<history_password>';
GRANT CREATE, ALTER, INSERT, SELECT ON PERCONA_SCHEMA.* TO 'history_user'@'%';
GRANT SELECT ON performance_schema.replication_group_members TO 'history_user'@'%';
```

### PERCONA_SCHEMA.XTRABACKUP_HISTORY table

This table contains the information about the previous server
backups. Information about the backups will only be written if the backup was
taken with `--history` option.

| Column Name       | Description                                                                                                                         |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| uuid              | Unique backup id                                                                                                                    |
| name              | User provided name of backup series. There may be multiple entries with the same name used to identify related backups in a series. |
| tool_name         | Name of tool used to take backup                                                                                                    |
| tool_command      | Exact command line given to the tool, with the --password, --history-password, and --encryption_key values hidden                  |
| tool_version      | Version of tool used to take backup                                                                                                 |
| ibbackup_version  | Version of the xtrabackup binary used to take backup                                                                                |
| server_version    | Server version on which backup was taken                                                                                            |
| start_time        | Time at the start of the backup                                                                                                     |
| end_time          | Time at the end of the backup                                                                                                       |
| lock_time         | Amount of time, in seconds, spent calling and holding locks for ``FLUSH TABLES WITH READ LOCK``                                     |
| binlog_pos        | Binlog file and position at end of ``FLUSH TABLES WITH READ LOCK``                                                                  |
| innodb_from_lsn   | LSN at beginning of backup which can be used to determine prior backups                                                             |
| innodb_to_lsn     | LSN at end of backup which can be used as the starting lsn for the next incremental                                                 |
| partial           | Is this a partial backup, if ``N`` that means that it's the full backup                                                             |
| incremental       | Is this an incremental backup                                                                                                       |
| format            | Description of result format (``xbstream``)                                                                                         |
| compressed        | Is this a compressed backup                                                                                                         |
| encrypted         | Is this an encrypted backup                                                                                                         |

### Limitations

* `--history` option must be specified only on the command
line and not within a configuration file in order to be effective.

* `--incremental-history-name` and `--incremental-history-uuid`
options must be specified only on the command line and not within
a configuration file in order to be effective.
