# Restore individual tables

Percona XtraBackup can export individual tables from any InnoDB database, if they are individual `.ibd` files, and import them into Percona Server for MySQL with XtraDB or MySQL 8.0. The source doesn’t have to be XtraDB or MySQL 8.0, but the destination must be.

The example exports and imports the following table:

```text
CREATE TABLE export_test (
a int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

## Export the table

To generate an `.ibd` file in the target directory, create the table using the `innodb_file_per_table` mode:

```{.bash data-prompt="$"}
$ find /data/backups/mysql/ -name export_test.*
/data/backups/mysql/test/export_test.ibd
```

During the `--prepare` step, add the [--export] option to the
command. For example:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --export --target-dir=/data/backups/mysql/
```

When restoring an encrypted InnoDB tablespace table, add the keyring file:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --export --target-dir=/tmp/table \
--keyring-file-data=/var/lib/mysql-keyring/keyring
```

The following files are the only files required to import the table into a server running Percona Server for MySQL with XtraDB or MySQL 8.0. If the server uses InnoDB Tablespace Encryption, add the `.cfp` file, which contains the transfer key and an encrypted tablespace key.

The files are located in the target directory:

```text
/data/backups/mysql/test/export_test.ibd
/data/backups/mysql/test/export_test.cfg
```

## Import the table

Import the table by doing the following:

* Create a copy of the table
* Discard the table's original tablespace
* Copy the `.ibd` and `.cfg` files to the location
* Import the tablespace

To import that table, do the following steps:

1. On the destination server, running Percona Server for MySQL with XtraDB or MySQL 8.0, create a table with the same structure.

2. Run the `ALTER TABLE ... DISCARD TABLESPACE` command to discard the new table's tablespace:

    ```{.bash data-prompt="mysql>"}
    mysql> ALTER TABLE test.export_test DISCARD TABLESPACE;
    ```

    If you see the an error message like "ERROR 1809 (HY000): Table 'test/export_test' in system tablespace", enable the `innodb_file_per_table` option on the server and do step 1 and 2 again.

3. Copy the exported files to the `test/` subdirectory of the destination server’s data directory.

4. Run `ALTER TABLE ... IMPORT TABLESPACE`.

    ```{.bash data-prompt="mysql>"}
    mysql> ALTER TABLE test.export_test IMPORT TABLESPACE;
    ```

    The table is imported, and you can run a `SELECT` to see the imported data.

[--export]: xtrabackup-option-reference.md#export
