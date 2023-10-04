# Restore individual tables

Percona XtraBackup can export a table that is contained in its own .ibd file. With Percona XtraBackup, you can export individual tables from any InnoDB database, and import them into Percona Server for MySQL with XtraDB or MySQL {{release}}. The source doesn’t have to be XtraDB or MySQL {{release}}, but the destination does. This method only works on individual .ibd files.

The following example exports and imports the following table:

```text
CREATE TABLE export_test (
a int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

## Export the table

To generate an .ibd file in the target directory, create the table using the `innodb_file_per_table` mode:

```{.bash data-prompt="$"}
$ find /data/backups/mysql/ -name export_test.*
/data/backups/mysql/test/export_test.ibd
```

During the `--prepare` step, add the `--export` option to the
command. For example:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --export --target-dir=/data/backups/mysql/
```

When restoring an encrypted InnoDB tablespace table, add the keyring file:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --export --target-dir=/tmp/table \
--keyring-file-data=/var/lib/mysql-keyring/keyring
```

The following files are the only files required to import the table into a server running Percona Server for MySQL with XtraDB or MySQL {{release}}. If the server uses InnoDB Tablespace Encryption, add the .cfp file, which contains the transfer key and an encrypted tablespace key.

The files are located in the target directory:

```text
/data/backups/mysql/test/export_test.ibd
/data/backups/mysql/test/export_test.cfg
```

## Import the table

On the destination server running Percona Server for MySQL with XtraDB or MySQL {{release}}, create a table with the same structure, and then perform the following steps:
{.power-number}

1. Run the `ALTER TABLE test.export_test DISCARD TABLESPACE;` command. If you see the following error message:

    ??? example "Error message"

        ```{.text .no-copy}
        ERROR 1809 (HY000): Table 'test/export_test' in system tablespace
        ```

    enable `innodb_file_per_table` option on the server and create the table again.

    ```{.bash data-prompt="$"}
    $ set global innodb_file_per_table=ON;
    ```

2. Copy the exported files to the `test/` subdirectory of the destination server’s data directory.

3. Run `ALTER TABLE test.export_test IMPORT TABLESPACE;`

    The table is imported, and you can run a `SELECT` to see the imported data.
