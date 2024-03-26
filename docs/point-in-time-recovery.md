# Point-in-time recovery

Recovering up to particular moment in database’s history can be done with
xtrabackup and the binary logs of the server.

Note that the binary log contains the operations that modified the database from
a point in the past. You must have full data directory as a base. Apply a series of operations from the binary log to make the data match the point in time data.

```{.bash data-prompt="$"}
$ xtrabackup --backup --target-dir=/path/to/backup
$ xtrabackup --prepare --target-dir=/path/to/backup
```

For more details on these procedures, see [Create a full backup] and [Prepare a full backup].

Now, suppose that some time has passed, and you want to restore the database to a
certain point in the past, having in mind that there is the constraint of the
point where the snapshot was taken.

To find out what is the situation of binary logging in the server, execute the
following queries:

```{.bash data-prompt="mysql>"}
mysql> SHOW BINARY LOGS;
```

??? example "Expected output"

    ```{.text .no-copy}
    +------------------+-----------+
    | Log_name         | File_size |
    +------------------+-----------+
    | mysql-bin.000001 |       126 |
    | mysql-bin.000002 |      1306 |
    | mysql-bin.000003 |       126 |
    | mysql-bin.000004 |       497 |
    +------------------+-----------+
    ```

This query returns the binary log names and file size.

```{.bash data-prompt="mysql>"}
mysql> SHOW MASTER STATUS;
```

??? example "Expected output"

    ```{.text .no-copy}
    +------------------+----------+--------------+------------------+
    | File             | Position | Binlog_Do_DB | Binlog_Ignore_DB |
    +------------------+----------+--------------+------------------+
    | mysql-bin.000004 |      497 |              |                  |
    +------------------+----------+--------------+------------------+
    ```

The query returns which file is currently being used to record changes, and the current
position within it. Typically,the files are stored in the datadir, unless, when starting the server, another location is specified with the
`--log-bin=` option).

To find out the position of the snapshot taken, see the
`xtrabackup_binlog_info` at the backup’s directory:

```{.bash data-prompt="$"}
$ cat /path/to/backup/xtrabackup_binlog_info
```

??? example "Expected output"

    ```{.text .no-copy}
    mysql-bin.000003      57
    ```

This result tells you which file was used at the moment of the backup for the binary
log and its position. That position will be the effective one when you restore
the backup:

```{.bash data-prompt="$"}
$ xtrabackup --copy-back --target-dir=/path/to/backup
```

As the restoration will not affect the binary log files (you may need to adjust
file permissions, see [Restore a backup]), the next step is
extracting the queries from the binary log with **mysqlbinlog** starting
from the position of the snapshot and redirecting the results to a file.

If you have multiple files for the binary log, as in the example, you
must extract the queries with one process.

```{.bash data-prompt="$"}
$ mysqlbinlog /path/to/datadir/mysql-bin.000003 /path/to/datadir/mysql-bin.000004 \
    --start-position=57 > mybinlog.sql
```

Inspect the file with the queries to determine which position or date
corresponds to the wanted point-in-time. Once determined, pipe it to the
server. For example, if the point is `11-12-25 01:00:00`, the command moves the the database forward to that point-in-time.

```{.bash data-prompt="$"}
$ mysqlbinlog /path/to/datadir/mysql-bin.000003 /path/to/datadir/mysql-bin.000004 \
    --start-position=57 --stop-datetime="11-12-25 01:00:00" | mysql -u root -p
```

[Create a full backup]: create-full-backup.md
[Prepare a full backup]: prepare-full-backup.md
[Restore a backup]: restore-a-backup.md