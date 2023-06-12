# Restore a partial backup

Restoring should be done by restoring individual tables in the partial backup to the server.

It can also be done by copying back the prepared backup to a “clean”
datadir (in that case, make sure to include the `mysql`
database) to the datadir you are moving the backup to. A system database can be created with the following:

```{.bash data-prompt="$"}
$ sudo mysql --initialize --user=mysql
```

Once you start the server, you may see mysql complaining about missing tablespaces:

??? example "Expected output"

    ```{.text .no-copy}
    2021-07-19T12:42:11.077200Z 1 [Warning] [MY-012351] [InnoDB] Tablespace 4, name 'test1/t1', file './d2/test1.ibd' is missing!
    2021-07-19T12:42:11.077300Z 1 [Warning] [MY-012351] [InnoDB] Tablespace 4, name 'test1/t1', file './d2/test1.ibd' is missing!
    ```

In order to clean the orphan database from the data dictionary, you must manually create the missing database directory and then `DROP` this database from the server.

Example of creating the missing database:

```{.bash data-prompt="$"}
$ mkdir /var/lib/mysql/test1/d2
```

Example of dropping the database from the server:

```{.bash data-prompt="mysql>"}
mysql> DROP DATABASE d2;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 2 rows affected (0.5 sec)
    ```