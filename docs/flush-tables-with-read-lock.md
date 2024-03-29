
# FLUSH TABLES WITH READ LOCK option

The `FLUSH TABLES WITH READ LOCK` option does the following with a global read lock:

* Closes all open tables

* Locks all tables for all databases

Release the lock with `UNLOCK TABLES`.

!!! note
   
    `FLUSH TABLES WITH READ LOCK` does not prevent inserting rows into the log tables.

To ensure consistent backups, use the `FLUSH TABLES WITH READ LOCK` option before taking a non-InnoDB file backup. The option does not affect long-running queries.

Enabling `FLUSH TABLES WITH READ LOCK` when the server has long-running queries can leave the server in a read-only mode until the queries finish. If the server is in either the `Waiting for table flush` or the `Waiting for master to send event` state, stopping the `FLUSH TABLES WITH READ LOCK` operation does not help. Stop any long-running queries to return to normal operation.

To prevent the server staying in a read-only mode until the queries finish, xtrabackup does the following:

* checks if any queries run longer than specified in `--ftwrl-wait-threshold`. If xtrabackup finds such queries, xtrabackup waits for one second and checks again. If xtrabackup waits longer than specified in `--ftwrl-wait-timeout`, the backup is aborted. As soon as xtrabackup finds no queries running longer than specified in `--ftwrl-wait-threshold`, xtrabackup issues the global lock.

* kills all queries or only the SELECT queries which prevent the global lock from being acquired.

!!! note
   
    All operations described in this section have no effect when [Backup locks] are used.

    Percona XtraBackup uses [Backup locks] where available as a lightweight alternative to `FLUSH TABLES WITH READ
    LOCK`. This operation automatically copies non-InnoDB data and avoids blocking DML queries that modify InnoDB tables.

## Wait for queries to finish

You should issue a global lock when no long queries are running. Waiting to issue the global lock for extended period of time is not a good method. The wait can extend the time needed for
backup to take place. The `–ftwrl-wait-timeout` option can limit the
waiting time. If it cannot issue the lock during this
time, xtrabackup stops the option, exits with an error message, and backup is
not be taken.

The option's default value is zero (0), which turns off the option.

Another possibility is to specify the type of query to wait on. In this case
`--ftwrl-wait-query-type`.

The possible values are `all` and
`update`. When `all` is used xtrabackup will wait for all long running
queries (execution time longer than allowed by `--ftwrl-wait-threshold`)
to finish before running the `FLUSH TABLES WITH READ LOCK`. When `update` is
used xtrabackup will wait on `UPDATE/ALTER/REPLACE/INSERT` queries to
finish.

The time needed for a specific query to complete is hard to predict. We assume that the long-running queries will not finish in a timely manner. Other queries which run for a short time finish quickly. xtrabackup uses the value of
`–ftwrl-wait-threshold option to specify the long-running queries
and will block a global lock. To use this option
xtrabackup user should have `PROCESS` and `CONNECTION_ADMIN` privileges.

## Kill the blocking queries

The second option is to kill all the queries which prevent from acquiring the
global lock. In this case, all queries which run longer than `FLUSH TABLES WITH READ LOCK` are potential blockers. Although all queries can be killed,
additional time can be specified for the short running queries to finish using
the `--kill-long-queries-timeout` option. This option specifies a query time limit. After the specified time is reached, the server kills the query. The default value is zero, which turns this
feature off.

The `--kill-long-query-type` option can be used to specify all or only
`SELECT` queries that are preventing global lock from being acquired. To use this option xtrabackup user should have `PROCESS` and `CONNECTION_ADMIN` privileges.

## Options summary

* `--ftwrl-wait-timeout` (seconds) - how long to wait for a
good moment. Default is 0, not to wait.


* `--ftwrl-wait-query-type` - which long queries
should be finished before `FLUSH TABLES WITH READ LOCK` is run. Default is
all.

* `--ftwrl-wait-threshold` (seconds) - how long query
should be running before we consider it long running and potential blocker of
global lock.

* `--kill-long-queries-timeout` (seconds) - how many time
we give for queries to complete after `FLUSH TABLES WITH READ LOCK` is
issued before start to kill. Default if `0`, not to kill.

* `--kill-long-query-type` - which queries should be killed once `kill-long-queries-timeout` has expired.

### Example

Running the xtrabackup with the following options will cause xtrabackup
to spend no longer than 3 minutes waiting for all queries older than 40 seconds
to complete.

```{.bash data-prompt="$"}
$  xtrabackup --backup --ftwrl-wait-threshold=40 \
--ftwrl-wait-query-type=all --ftwrl-wait-timeout=180 \
--kill-long-queries-timeout=20 --kill-long-query-type=all \
--target-dir=/data/backups/
```

After `FLUSH TABLES WITH READ LOCK` is issued, xtrabackup will wait for 20
seconds for lock to be acquired. If lock is still not acquired after 20 seconds,
it will kill all queries which are running longer that the `FLUSH TABLES WITH READ LOCK`.

[backup locks]: https://docs.percona.com/percona-server/innovation-release/backup-locks.html
[Backup locks]: https://docs.percona.com/percona-server/innovation-release/backup-locks.html
