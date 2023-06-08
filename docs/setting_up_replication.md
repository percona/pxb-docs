# How to set up a replica for replication in 6 simple steps with Percona XtraBackup

Data is, by far, the most valuable part of a system. Having a backup done
systematically and available for a rapid recovery in case of failure is
admittedly essential to a system. However, it is not common practice
because of
its costs, infrastructure needed or even the boredom associated to the
task. Percona XtraBackup is designed to solve this problem.

You can have almost real-time backups in 6 simple steps by setting up a
replication environment with Percona XtraBackup.

## All the things you will need

Setting up a replica for replication with *Percona XtraBackup* is a
straightforward procedure. In order to keep it simple, here is a list of
the
things you need to follow the steps without hassles:

`Source`

A system with a *MySQL*-based server installed, configured and running. This
system will be called `Source`, as it is where your data is stored and the one to be replicated. We will assume the following about this system:

* the *MySQL* server is able to communicate with others by the standard TCP/IP port;


* the *SSH* server is installed and configured;


* you have a user account in the system with the appropriate permissions;


* you have a MySQL’s user account with appropriate privileges.


* server has binlogs enabled and server-id set up to 1.

`Replica`

Another system, with a *MySQL*-based server installed on it. We
will refer to this machine as `Replica` and we will assume the same things
we did about `Source`, except that the server-id on `Replica` is 2.

`Percona XtraBackup`

The backup tool we will use. It should be installed in both computers for convenience.

!!! note
   
    It is not recommended to mix MySQL variants (Percona Server, MySQL) in your replication setup. This may produce incorrect `xtrabackup_slave_info` file when adding a new replica. 

## Version updates

The 8.0.23 version deprecates the `CHANGE_MASTER_TO` command. In that 
version and later, use
the [CHANGE_REPLICATION_SOURCE_TO and the appropriate options](https://dev.mysql.com/doc/refman/8.0/en/change-replication-source-to.html) instead.

The 8.0.22 version deprecates the`START SLAVE` command. In that version or 
later, use `START REPLICA` instead.


## 1. Make a backup on the `Source` and prepare it

At the  `Source`, issue the following to a shell:

```{.bash data-prompt="$"}
$ xtrabackup --backup --user=yourDBuser --password=MaGiCdB1 --target-dir=/path/to/backupdir
```

After this is finished you should get:

??? example "Expected output"

    ```{.text .no-copy}
    xtrabackup: completed OK!
    ```

This will make a copy of your *MySQL* data dir
to the `/path/to/backupdir` directory.
You have told *Percona XtraBackup* to connect to the database server
using your database user and password,
and do a hot backup of all your data in it
(all *MyISAM*, *InnoDB* tables and indexes in them).

In order for snapshot to be consistent you need to prepare the data on the
source:

```{.bash data-prompt="$"}
$ xtrabackup --user=yourDBuser --password=MaGiCdB1 \
            --prepare --target-dir=/path/to/backupdir
```

You need to select path where your snapshot has been taken.
If everything is ok you should get the same OK message.
Now the transaction logs are applied to the data files,
and new ones are created:
your data files are ready to be used by the MySQL server.

*Percona XtraBackup* knows where your data is by reading your my.cnf file.
If you have your configuration file in a non-standard place,
you should use the flag `--defaults-file` `=/location/of/my.cnf`.

If you want to skip writing the username and password
every time you want to access *MySQL*,
you can set it up in `.mylogin.cnf` as follows:

```
mysql_config_editor set --login-path=client --host=localhost --user=root --password
```

For more information, see [MySQL Configuration
Utility](https://dev.mysql.com/doc/refman/8.0/en/mysql-config-editor.html).

This statement provides root access to MySQL.

## 2.  Copy backed up data to the Replica

On the Source, use rsync or scp to copy the data from the Source to the
Replica. If you are syncing the data directly to replica’s data directory,
we recommend that you stop the `mysqld` there.

```{.bash data-prompt="$"}
$ rsync -avpP -e ssh /path/to/backupdir Replica:/path/to/mysql/
```

After data has been copied, you can back up the original or previously
installed *MySQL* datadir (**NOTE**: Make sure mysqld is shut down before
you move the contents of its datadir, or move the snapshot into its
datadir.). Run the following commands on the Replica:

```{.bash data-prompt="$"}
$ mv /path/to/mysql/datadir /path/to/mysql/datadir_bak
```

and move the snapshot from the `Source` in its place:

```{.bash data-prompt="$"}
$ xtrabackup --move-back --target-dir=/path/to/mysql/backupdir
```

After you copy data over, make sure the Replica *MySQL* has the proper
permissions to access them.

```{.bash data-prompt="$"}
$ chown mysql:mysql /path/to/mysql/datadir
```

If the ibdata and iblog files are located in directories outside the
datadir, you must put these files in their proper place after the logs have
been applied.

## 3. Configure the Source’s MySQL server

On the source, run the following command to add the appropriate grant. This
grant allows the replica to be able to connect to source:

```{.bash data-prompt="mysql>"}
mysql> GRANT REPLICATION SLAVE ON *.*  TO 'repl'@'$replicaip'
IDENTIFIED BY '$replicapass';
```

Also make sure that firewall rules are correct and that the `Replica` can
connect to the `Source`. Run the following command on the Replica to test
that you can run the mysql client on `Replica`, connect to the `Source`,
and authenticate.

```{.bash data-prompt="mysql>"}
mysql> mysql --host=Source --user=repl --password=$replicapass
```

Verify the privileges.

```{.bash data-prompt="mysql>"}
mysql> SHOW GRANTS;
```

## 4. Configure the Replica’s MySQL server

Copy the `my.cnf` file from the `Source` to the `Replica`:

```{.bash data-prompt="$"}
$ scp user@Source:/etc/mysql/my.cnf /etc/mysql/my.cnf
```

and change the following options in /etc/mysql/my.cnf:

```
server-id=2
```

and start/restart mysqld on the `Replica`.

In case you’re using init script on Debian-based system to start mysqld, be
sure that the password for `debian-sys-maint` user has been updated, and
it’s the same as that user’s password on the `Source`. Password can be seen
and updated in `/etc/mysql/debian.cnf`.

## 5. Start the replication

On the `Replica`, review the content of the file `xtrabackup_binlog_info`,
it will be something like:

```{.bash data-prompt="$"}
$ cat /var/lib/mysql/xtrabackup_binlog_info
```

The results should resemble the following:

??? example "Expected output"

    ```{.text .no-copy}
    Source-bin.000001     481
    ```

[The term `master` is deprecated](#version-updates). Do the following on a 
MySQL console and use the username and
password you’ve set up in STEP 3 :

* Version 8.0.23 or later, use the `CHANGE_REPLICATION_SOURCE_TO` statement

* Before 8.0.23, use the `CHANGE MASTER` statement


```sql
CHANGE REPLICATION SOURCE TO
    SOURCE_HOST='$sourceip',
    SOURCE_USER='repl',
    SOURCE_PASSWORD='$replicapass',
    SOURCE_LOG_FILE='Source-bin.000001',
    SOURCE_LOG_POS=481;
```

Start the replica:

```sql
START REPLICA;
```

The [term `slave` is deprecated](#version-updates). Do the following:

* Version 8.0.22 or later, use `START REPLICA`
* Before version 8.0.22, use `START SLAVE`

## 6. Check

On the `Replica`, check that everything went OK with:

```sql
SHOW REPLICA STATUS\G
```

The result shows the status:

??? example "Expected output"

    ```{.text .no-copy}
    Slave_IO_Running: Yes
    Slave_SQL_Running: Yes
    Seconds_Behind_Master: 13
    ```

Both `IO` and `SQL` threads need to be running. The `Seconds_Behind_Master`
means the `SQL` currently being executed has a `current_timestamp` of 13
seconds ago. It is an estimation of the lag between the `Source` and
the `Replica`. Note that at the beginning, a high value could be shown
because the `Replica` has to “catch up” with the `Source`.

## Adding more replicas to the Source

You can use this procedure with slight variation to add new replicas to a
source. We will use *Percona XtraBackup* to clone an already configured
replica. We will continue using the previous scenario for convenience, but
we will add a `NewReplica` to the plot.

At the `Replica`, do a full backup:

```{.bash data-prompt="$"}
$ xtrabackup --user=yourDBuser --password=MaGiCiGaM \
   --backup --slave-info --target-dir=/path/to/backupdir
```

By using the `--slave-info` *Percona XtraBackup* creates additional file
called `xtrabackup_slave_info`.

Apply the logs:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --use-memory=2G --target-dir=/path/to/backupdir/
```

!!! note

    In the ``prepare`` phase, the `--use-memory` parameter speeds up the process if the amount of RAM assigned to the option is available. Use the parameter only in the `prepare` phase. In the other phases the parameter makes the application lazy allocate this memory (reserve) but does not affect database pages.

Copy the directory from the `Replica` to the `NewReplica` (**NOTE**: Make
sure mysqld is shut down on the `NewReplica` before you copy the contents
the snapshot into its datadir.):

```
rsync -avprP -e ssh /path/to/backupdir NewReplica:/path/to/mysql/datadir
```

For example, to set up a new user, `user2`, you add another grant on
the Source:

```{.bash data-prompt=">"}
> GRANT REPLICATION SLAVE ON *.*  TO 'user2'@'$newreplicaip'
 IDENTIFIED BY '$replicapass';
```

On the `NewReplica`, copy the configuration file from the `Replica`:

```{.bash data-prompt="$"}
$ scp user@Replica:/etc/mysql/my.cnf /etc/mysql/my.cnf
```

Make sure you change the server-id variable in `/etc/mysql/my.cnf` to 3 and
disable the replication on start:

```
skip-slave-start
server-id=3
```

After setting `server_id`, start **mysqld**.

Fetch the master_log_file and master_log_pos from the
file `xtrabackup_slave_info`, execute the statement for setting up the
source and the log file for the NewReplica:

```{.bash data-prompt=">"}
> CHANGE MASTER TO
     MASTER_HOST='$Sourceip',
     MASTER_USER='repl',
     MASTER_PASSWORD='$replicapass',
     MASTER_LOG_FILE='Source-bin.000001',
     MASTER_LOG_POS=481;
```

[The term `master` is deprecated](#version-updates). Do the following 
and then start the replica:

* Version 8.0.23 or later, use the `CHANGE_REPLICATION_SOURCE_TO` statement

* Before 8.0.23, use the `CHANGE MASTER` statement

[The term `slave` is deprecated](#version-updates). Do the following:

* Version 8.0.22 or later, use `START REPLICA`.
* Before version 8.0.22, use `START SLAVE`

```{.bash data-prompt=">"}
> START REPLICA;
```

If both IO and SQL threads are running when you check the `NewReplica`,
server is replicating the `Source`.

!!! admoniton "See also"

    [How to create a new (or repair a broken) GTID based slave](./recipes_ibkx_gtid.md)