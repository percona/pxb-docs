# Restore individual tables

With *Percona XtraBackup*, you can export individual tables from any *InnoDB* database, and
import them into *Percona Server for MySQL* with *XtraDB* or *MySQL* 5.7. The source does not
need to be *XtraDB* or *MySQL* 5.7 but the destination must be. This operation only works on
individual .ibd files. A table that is not contained in its own `.ibd` file cannot be exported.

The following example exports and imports the following table:

```sql
CREATE TABLE export_test (
  a int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

## Export the table

To generate an .ibd file in the target directory, create the table using the `innodb_file_per_table` mode:

```shell
$ find /data/backups/mysql/ -name export_test.*
/data/backups/mysql/test/export_test.ibd
```

During the `--prepare` step, add the `--export` option to the command. For example:

```shell
$ xtrabackup --prepare --export --target-dir=/data/backups/mysql/
```

When restoring an [encrypted InnoDB tablespace](../advanced/encrypted_innodb_tablespace_backups.md#encrypted-innodb-tablespace-backups) table, add the keyring file:
 
```shell
$ xtrabackup --prepare --export --target-dir=/tmp/table \
--keyring-file-data=/var/lib/mysql-keyring/keyring
```

The following files are the only files required to import the table into a server running
Percona Server for MySQL with XtraDB or MySQL 5.7. If the server uses InnoDB Tablespace Encryption, add the `.cfp` file, which contains the transfer key and an encrypted tablespace key.

The files are located in the target directory:

```text
/data/backups/mysql/test/export_test.ibd
/data/backups/mysql/test/export_test.cfg
```

## Import the table

On the destination server, create a table with the same structure, and then perform the following steps:

1. Run the `ALTER TABLE test.export_test DISCARD TABLESPACE;` command. If you see the following error message:

    ```{.text .no-copy}
    ERROR 1030 (HY000): Got error -1 from storage engine` message
    ```
    
    enable [innodb_file_per_table](../glossary.md#innodb_file_per_table) option:
    
    ```shell
    $ set global innodb_file_per_table=ON;
    ```

    Then create the table again.

* Copy the exported files to the `test/` subdirectory of the destination
server’s data directory

* Execute `ALTER TABLE test.export_test IMPORT TABLESPACE;`

The table should now be imported, and you should be able to `SELECT` from it
and see the imported data.

!!! note

    Persistent statistics for imported tablespace will be empty until you run the `ANALYZE TABLE` on the imported table. They are empty because they are stored in the system tables `mysql.innodb_table_stats` and `mysql.innodb_index_stats` and they are not updated by server during the import. This is due to upstream bug [#72368](http://bugs.mysql.com/bug.php?id=72368).

