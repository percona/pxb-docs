# How to create a new (or repair a broken) GTID-based replica

*MySQL* 5.6 introduced the Global Transaction
ID ([GTID](http://dev.mysql.com/doc/refman/5.6/en/replication-gtids-concepts.html))
support in replication. *Percona XtraBackup* automatically
stores the `GTID` value in the `xtrabackup_binlog_info` when doing the
backup of *MySQL* and *Percona Server for MySQL* 5.7 with the `GTID` mode
enabled. This
information can be used to create a new (or repair a broken) `GTID`-based
replica.

## 1. Take a backup from any server on the replication environment, source or replica

The following command takes a backup and saves it in
the `/data/backups/$TIMESTAMP` folder:

```{.bash data-prompt="$"}
$ xtrabackup --backup --target-dirs=/data/backups/
```

In the destination folder, there will be a file with the name
`xtrabackup_binlog_info`. This file contains both binary log coordinates
and the `GTID` information.

```{.bash data-prompt="$"}
$ cat xtrabackup_binlog_info
```
The result could look like this:

??? example "Expected output"

    ```{.text .no-copy}
    mysql-bin.000002    1232        c777888a-b6df-11e2-a604-080027635ef5:1-4
    ```

That information is also printed by xtrabackup after taking the backup:

??? example "Expected output"

    ```{.text .no-copy}
    xtrabackup: MySQL binlog position: filename 'mysql-bin.000002', position 1232, GTID of the last change 'c777888a-b6df-11e2-a604-080027635ef5:1-4'
    ```

## 2. Prepare the backup

The backup will be prepared with the following command on the Source:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --target-dir=/data/backup
```

You need to select the path where your snapshot has been taken, for example
`/data/backups/2013-05-07_08-33-33`. If everything is ok you should get the
same OK message. Now, the transaction logs are applied to the data files,
and new
ones are created: your data files are ready to be used by the MySQL server.

## 3. Move the backup to the destination server

Use **rsync** or **scp** to copy the data to the destination
server. If you are synchronizing the data directly to the already running
replica’s data
directory it is advised to stop the *MySQL* server there.

```{.bash data-prompt="$"}
$ rsync -avprP -e ssh /path/to/backupdir/$TIMESTAMP NewSlave:/path/to/mysql/
```

After you copy the data over, make sure *MySQL* has proper permissions to
access them.

```{.bash data-prompt="$"}
$ chown mysql:mysql /path/to/mysql/datadir
```

## 4. Configure and start replication

Set the `gtid_purged` variable to the `GTID` from
`xtrabackup_binlog_info`. Then, update the information about the
source node and, finally, start the replica. Run the following commands on
the replica if you are using a version before 8.0.22:

```{.bash data-prompt="#"}
# Using the mysql shell
 > SET SESSION wsrep_on = 0;
 > RESET MASTER;
 > SET SESSION wsrep_on = 1;
 > SET GLOBAL gtid_purged='<gtid_string_found_in_xtrabackup_binlog_info>';
 > CHANGE MASTER TO
             MASTER_HOST="$masterip",
             MASTER_USER="repl",
             MASTER_PASSWORD="$slavepass",
             MASTER_AUTO_POSITION = 1;
 > START SLAVE;
```

If you are using version 8.0.22 or later, use `START REPLICA` instead
of `START SLAVE`. `START SLAVE` is deprecated as of that release. If you
are using version 8.0.21 or earlier, use `START SLAVE`.

If you are using a version 8.0.23 or later, run the following commands:

```{.bash data-prompt="#"}
# Using the mysql shell
 > SET SESSION wsrep_on = 0;
 > RESET MASTER;
 > SET SESSION wsrep_on = 1;
 > SET GLOBAL gtid_purged='<gtid_string_found_in_xtrabackup_binlog_info>';
 > CHANGE REPLICATION SOURCE TO
             SOURCE_HOST="$masterip",
             SOURCE_USER="repl",
             SOURCE_PASSWORD="$slavepass",
             SOURCE_AUTO_POSITION = 1;
 > START REPLICA;
```

If you are using version 8.0.23 or later,
use [CHANGE_REPLICATION_SOURCE_TO and the appropriate options](https://dev.mysql.com/doc/refman/8.0/en/change-replication-source-to.html). `CHANGE_MASTER_TO` is deprecated as of that release.

!!! note
   
    The example above is applicable to Percona XtraDB Cluster.
    The `wsrep_on` variable is set to 0 before resetting the source (`RESET MASTER`). The reason is that Percona XtraDB Cluster will not allow resetting the source if `wsrep_on=1`.

## 5. Check the replication status

The following command returns the replica status:

```{.bash data-prompt="mysql>"}
mysql> SHOW REPLICA STATUS\G
```
The results should be similar to the following:

??? example "Expected output"

    ```{.text .no-copy}
    [..]
    Slave_IO_Running: Yes
    Slave_SQL_Running: Yes
    [...]
    Retrieved_Gtid_Set: c777888a-b6df-11e2-a604-080027635ef5:5
    Executed_Gtid_Set: c777888a-b6df-11e2-a604-080027635ef5:1-5
    ```

!!! note
   
    The command [SHOW SLAVE STATUS](https://dev.mysql.com/doc/refman/8.0/en/show-slave-status.html) is deprecated. Use [SHOW REPLICA STATUS](https://dev.mysql.com/doc/refman/8.0/en/show-replica-status.html).

We can see that the replica has retrieved a new transaction with number 5,
so transactions from 1 to 5 are already on this slave.

We have created a new replica in our `GTID` based replication
environment.
