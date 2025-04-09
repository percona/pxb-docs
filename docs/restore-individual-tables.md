# Move single tables between databases

Sometimes, you must move just one table instead of a whole database. Percona XtraBackup helps you do this. This guide shows you how to move specific tables between different database systems while keeping your data safe.

This process only works with InnoDB tables that use the `file-per-table` setup. This setup stores each table's data in its `.ibd` file. You can move these tables to systems running Percona Server for MySQL with XtraDB or MySQL 8.0. Your source database can be any type, but the target database must be XtraDB or MySQL 8.0.

When moving tables, you'll work with several important files. Each file has a specific job in the restoration process:

| File                             | Description |
|----------------------------------|-------------|
| ibdata1                          | The main system file in InnoDB that holds necessary metadata and sometimes table data. You need this file for any InnoDB restoration, including when recovering just one table. |
| undo_001 and undo_002            | Files that help undo transactions that weren't finished. These files help recover from crashes during the preparation phase. They're an essential part of a complete backup plan. |
| mysql.ibd                        | A file that contains table definitions and structure information. This file is necessary when restoring individual tables. |
| xtrabackup_info                  | A file with information about the backup, including which server version was used and when the backup was made. |
| xtrabackup_checkpoints           | A file that keeps track of important points in the backup process. These checkpoints help with crash recovery. |
| xtrabackup_logfile               | The transaction log that records all database changes. This log ensures your backup stays consistent throughout the restoration. |
| xtrabackup_tablespaces           | This is a list of tablespaces stored outside the main data directory. During restoration, XtraBackup tries to rebuild file paths to match their original locations. |
| .ibd from all tables you want to restore | The most critical files for single-table restoration. Each InnoDB table in file-per-table mode has its .ibd file containing data and indexes. You must have the .ibd file for each table you want to restore. |

The following example shows the export and import process for a table called `export_test`:

```{.bash data-prompt="$"}
mysql -u <username> -p -e "CREATE DATABASE create_database_test;"
```

```{.bash data-prompt="$"}
mysql> CREATE TABLE export_test (
a int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

## Save the schema

Before importing any table, you must save the schema definition for all tables you want to restore. Think of the schema as a blueprint for your table. XtraBackup only backs up data files, not these blueprints. Without the original schema, MySQL won't be able to use the restored .ibd files.

When you back up your database, you may not know which tables to restore later. This operation prepares you for any future restoration needs. Also, table structures might change between the time when you create the backup and when you use mysqldump. Saving the most current structure helps ensure everything works during restoration.

Review the script in [Dump schema for all tables](dump-schema.md) for an easier way to save schemas. You'll likely need to adjust this script to fit your setup.

By saving schemas ahead of time, you ensure that all the table blueprints are ready when you start restoring from backups, making data recovery go more smoothly.

## Export the table

First, create the table using the `innodb_file_per_table` setting. This setting tells MySQL to create a separate `.ibd` file for each table in your source directory. Run this command to find the created file in your system:

```{.bash data-prompt="$"}
$ find /data/backups/mysql/ -name export_test.*
/data/backups/mysql/test/export_test.ibd
```

Next, when you run the `--prepare` phase, add the [--export] option to your command. This option tells XtraBackup to create any extra files needed for moving the table:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --export --target-dir=/data/backups/mysql/
```

If you're working with encrypted tables (ones that use transparent data encryption), you'll need extra security settings. You must include the keyring file that has the encryption keys:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --export --target-dir=/tmp/table \
--keyring-file-data=/var/lib/mysql-keyring/keyring
```

After these commands finish successfully, you'll need these files for the table import.

```text
/data/backups/mysql/test/export_test.ibd
/data/backups/mysql/test/export_test.cfg
/data/backups/mysql/test/export_test.cfp
```

## Import the table

Now that we've exported the table, we can move it to the destination system. You need to follow these steps in order on the target server:

* Use the saved schema definition to create an empty table at the destination. This schema provides the framework for your imported data.

* Copy all three important files (.ibd, .cfp, and .cfg) from your source directory to the matching directory in the destination system.


The following is the detailed process:

1. Use the schema and create an empty table copy in the new location on your target server (which must be running Percona Server for MySQL with XtraDB or MySQL 8.0).

    ```{.bash data-prompt="$"}
    $ mysql -uroot < ./schema_dumps/test/create_database_test.sql;
    $ mysql -uroot < ./schema_dumps/test/export_test.sql;
    ```

2. Run this SQL command to disconnect the new table from its default tablespace. This command prepares it to receive the imported data:

    ```{.bash data-prompt="mysql>"}
    mysql> ALTER TABLE test.export_test DISCARD TABLESPACE;
    ```

    If you see an error like “ERROR 1809 (HY000): Table ‘test/export_test’ in the system tablespace, " the `innodb_file_per_table` setting is disabled on your target server. Enable this in your server setup, then try the steps again.

3. Copy all the table files (export_test.ibd, export_test.cfp, and export_test.cfg) from the source directory to the matching destination schema directory inside the server data directory.

4. Run this SQL command to attach the moved tablespace to the destination table, finishing the data move:

    ```{.bash data-prompt="mysql>"}
    mysql> ALTER TABLE test.export_test IMPORT TABLESPACE;
    ```

After these steps are finished successfully, your table move is complete and the data is ready to use. You can run a `SELECT` query on the newly imported table to check that the imported data is correct.
    
[--export]: xtrabackup-option-reference.md#export
