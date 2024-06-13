# Restore a single table

Backing up and restoring a full database can take a lot of time. If you need to restore just one table that has, for example, been changed by mistake, you can use either of the following procedures.

The advantages of doing this operation are the following:

| Advantage               | Description                                                                                                            |
|-----------------------|------------------------------------------------------------------------------------------------------------------------|
| Targeted Restoration  | You can restore just one table instead of the entire database. This saves time and effort, especially when you only need data from a specific table. |
| Efficient Use of Resources | By restoring a single table, you reduce the amount of data that needs processing. This can lead to faster recovery times and less strain on system resources. |
| Flexibility           | You have the flexibility to restore data without affecting the rest of the database. This is useful if you want to recover data without disrupting other operations. |
| Space Saving          | Restoring one table instead of the whole database can save disk space. You only bring back the necessary data, leaving out unnecessary tables. |
| Minimal Downtime      | Restoring a single table can be quicker and cause less downtime compared to restoring the entire database. This is beneficial for maintaining high availability. |

The disadvantages of doing this operation are the following:

| Disadvantage             | Description                                                                                                                                                                                   |
|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Complexity               | The process of restoring one table can be complex. It involves multiple steps like preparing the backup, exporting tablespaces, and importing them into the database. This can be challenging for beginners. |
| Risk of Schema Mismatch  | If the schema of the table in the backup differs from the current schema, you may encounter issues. You need to ensure that the table structure matches exactly to avoid problems.                    |
| Dependency on Tools      | Restoring a single table requires specific tools and commands. You need to be familiar with tools like Percona XtraBackup and SQL commands, which can be a learning curve for beginners.                |
| Potential Data Inconsistency | If the table you restore depends on other tables (like foreign keys or constraints), you might face data consistency issues. You need to ensure that related data remains consistent.                  |
| Manual Effort            | The process involves several manual steps, such as creating a dummy table, discarding the tablespace, and importing the tablespace. This requires careful execution to avoid mistakes.                 |

The following procedure walks you through backing up and restoring a single table.

1. Verify the table checksum

    Before starting, let's confirm the current state of `mytable`. Use the `CHECKSUM TABLE` command to get a checksum value. This value represents a fingerprint of the table's contents. We'll use this command again after the restore to verify success.

    Concurrent writes can affect the result of `CHECKSUM TABLE`. The command acquires a read lock on the table during the calculation. This lock prevents table modifications but does not block writes completely. The checksum may be incorrect if inserting new data or existing data is modified during the calculation. The calculation is based on the data at the time the snapshot is taken.

    ```{.bash data-prompt="mysql>"}
    mysql> CHECKSUM TABLE mytable;
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        +--------------+-----------+
        | Table        | Checksum  |
        +--------------+-----------+
        | test.mytable | 5B4C39B1  |
        +--------------+-----------+
        ```

2. Back up the table:

    Now, let's back up just the mytable table. Run the `xtrabackup` command with the `--tables` option to specify the table and other connection details.

    ```{.bash data-prompt="$"}
    $ ./xtrabackup --user=backup --password=password --backup --tables=mytable --target-dir=$HOME/dbbackup -S $HOME/test/socket.sock --datadir=$HOME/test/data
    ```

    XtraBackup copies the `mytable.ibd` file and other required files to the backup directory.

3. Prepare the backup

    Next, we need to prepare the backup for restore. Use `xtrabackup` again with the `--prepare` and `--export` options. This step creates a configuration file specifically for `mytable`.

    ```{.bash data-prompt="$"}
    $ ./xtrabackup --prepare --export --target-dir=$HOME/test
    ```

    This step prepares the table configuration, resulting in `mytable.ibd` and `mytable.cfg` files in the backup directory.

4. Remove existing tablespace

    Before restoring the table, we need to remove the existing tablespace from the database. Use the ALTER TABLE command with the DISCARD TABLESPACE option.

    ```{.bash data-prompt="mysql>"}
    mysql> ALTER TABLE mytable DISCARD TABLESPACE;
    ```

5. Copy table files

    Now, copy the table files (mytable.ibd and mytable.cfg) from the backup directory to the Percona Server data directory ($HOME/test/data). Depending on your security settings, you might need to disable SELinux or AppArmor temporarily. After copying, make sure the files are owned by the MySQL user.

    ```{.bash data-prompt="$"}
    $ cp $HOME/test/mytable.* $HOME/test/data/
    ```

6. Import the Tablespace:

    Finally, use the ALTER TABLE command again, but this time with the IMPORT TABLESPACE option to restore the table from the backup files.

    ```{.bash data-prompt="mysql>"}
    mysql> ALTER TABLE mytable IMPORT TABLESPACE;
    ```
7. Verify the Restore (After Backup):

    Let's confirm that the restore was successful. Run the CHECKSUM TABLE command again to get a new checksum value for mytable.

    ```{.bash data-prompt="mysql>"}
    mysql> CHECKSUM TABLE mytable;
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        +--------------+-----------+
        | Table        | Checksum  |
        +--------------+-----------+
        | test.mytable | 5B4C39B1  |
        +--------------+-----------+
        ```

    You have successfully restored the table.

## Backup and restore a full database

### Full database backup

Back up the entire database with the following command:

   ```{.bash data-prompt="$"}
   $ xtrabackup --user=backup --password='password' --backup --target-dir=$HOME/dbbackup_PS8 -S $HOME/PS130320_8_0_19_10_debug/socket.sock --datadir=$HOME/PS130320_8_0_19_10_debug/data
   ```

### Prepare the backup

Prepare the backup with the `--export` option:

   ```{.bash data-prompt="$"}
   $ xtrabackup --prepare --export --target-dir=$HOME/dbbackup_PS8
   ```

### Restore a table

The following procedure walks you through backing up and restoring a single table.

1. Discard the table's tablespace:

    ```{.bash data-prompt="mysql>"}
    mysql> ALTER TABLE mytable DISCARD TABLESPACE;
    ```

2. Copy the table files from the backup directory to the Percona Server data directory:

    ```{.bash data-prompt="$"}
    $ cp $HOME/dbbackup_PS8/test/mytable.* $HOME/PS130320_8_0_19_10_debug/data/test/
    ```

3. Import the tablespace:

    ```{.bash data-prompt="mysql>"}
    $ ALTER TABLE mytable IMPORT TABLESPACE;
    ```

### For MyISAM tables

The following procedure walks you through backing up and restoring a single MyISAM table.

1. Drop the MyISAM table:

    ```{.bash data-prompt="mysql>"}
    $ DROP TABLE myisamtable;
    ```

2. Restore the MyISAM table using the `IMPORT TABLE` statement.

### Restore a schema or database

Back up a database schema with this command:

   ```{.bash data-prompt="$"}
   $ xtrabackup --user=backup --password='password' --backup --databases=test --target-dir=$HOME/test -S $HOME/test/socket.sock --datadir=$HOME/test/data
   ```

### Prepare and restore

The following procedure walks you through steps to prepare and restore a single table.

1. Prepare the backup with the `--export` option:

    ```{.bash data-prompt="$"}
    $ xtrabackup --prepare --export --target-dir=$HOME/test
    ```

2. Remove the tablespace for all InnoDB tables in the database:

    ```{.bash data-prompt="mysql>"}
    mysql> ALTER TABLE mytable DISCARD TABLESPACE;
    ```

3. Copy all table files from the backup directory to the MySQL data directory:

    ```{.bash data-prompt="$"}
    $ cp $HOME/test/* $HOME/PS130320_8_0_19_10_debug/data/test/
    ```

4. Restore the tables

    ```{.bash data-prompt="mysql>"}
    mysql> ALTER TABLE mytable IMPORT TABLESPACE;
    ```

This method does not require stopping the database server. However, it would be best to restore each table individually, which you can automate with a script.

## Use a partial backup

Prerequisites:

* Partial XtraBackup requires restoring tables individually, unlike a full backup.
* Ensure the versions of mysqldump and XtraBackup are compatible with your MySQL 8 server.
* Consider using a scripting solution to automate the backup process.

### Capturing schema with mysqldump

While XtraBackup offers partial backups for specific directories, it doesn't capture the schema. To create a complete backup solution for database servers, you can combine mysqldump for the schema and XtraBackup for the data.

1. Prepare for Backup

    * **Stop writes (optional):** Consider briefly stopping writes to the database using `mysqladmin FLUSH TABLES WITH READ LOCK` to ensure data consistency during the backup process.  Remember to unlock tables with `mysqladmin UNLOCK TABLES` afterwards.

    * **Choose directories:** Decide on separate directories for the schema dump and partial XtraBackup.

2. Capture Schema with mysqldump

    * Open a terminal and connect to your MySQL server.
    * Use the following command to dump the schema for your desired schema_name, replacing it with the actual name:

    ```{.bash data-prompt="$"}
    $ mysqldump -u username -p schema_name > schema_backup.sql
    ```

    * Enter your MySQL username and password (using -p prompts you for password) when prompted.

3. Perform Partial XtraBackup

    * Use the `xtrabackup --partial` flag to specify the directory containing the specific tables you want to back up. 
    * Here's the command structure:

    ```{.bash data-prompt="$"}
    $ xtrabackup --partial [--include <directory>] --backup outdir
    ```

    * Replace `<directory>` with the path containing the table files (usually inside the data directory) for the specific schema you want to back up. 
    * Replace `outdir` with the directory where you want to store the partial XtraBackup.

4. (Optional) Resume writes

    If you stopped writes earlier, run `mysqladmin UNLOCK TABLES` to unlock the tables and resume normal operations.

#### Restore the backup

In a restore, you'll need both the schema dump and the partial XtraBackup.

1. Restore the schema first using:

    ```{.bash data-prompt="$"}
    $ mysql -u username -p schema_name < schema_backup.sql
    ```

2. Then, use `xtrabackup --prepare --apply-logs` on the partial XtraBackup directory to prepare the data for restoring individual tables.

3. Finally, use `xtrabackup --restore` to restore specific tables as needed. Refer to the XtraBackup documentation for detailed restore instructions specific to your needs.


