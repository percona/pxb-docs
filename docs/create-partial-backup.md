# Create a partial backup

xtrabackup supports taking partial backups when the
`innodb_file_per_table` option is enabled.

!!! warning

    Do not copy back the prepared backup.

    Restoring partial backups should be done by importing the tables.
    We do not by using the `–copy-back` option. This operation may lead to database
    inconsistencies.
    
    We do not recommend running incremental backups after taking a partial
    backup.

The xtrabackup binary fails if you delete any of the matched or listed tables during the backup.

There are multiple ways of specifying which part of the whole data is backed up:

* Use the `--tables` option to list the table names

* Use the `--tables-file` option to list the tables in a file

* Use the `--databases` option to list the databases

* Use the `--databases-file` option to list the databases

The following examples assume a database named `test` that contains tables named `t1` and `t2`.

=== "`–-tables` option"

    The first method involves the xtrabackup `–tables` option. The option’s
    value is a regular expression that is matched against the fully-qualified database name and table name using the `databasename.tablename` format.
    
    To back up only tables in the `test` database, use the following
    command:
    
    ```{.bash data-prompt="$"}
    $ xtrabackup --backup --datadir=/var/lib/mysql --target-dir=/data/backups/ \
    --tables="^test[.].*"
    ```
    
    To back up only the `test.t1` table, use the following command:
    
    ```{.bash data-prompt="$"}
    $ xtrabackup --backup --datadir=/var/lib/mysql --target-dir=/data/backups/ \
    --tables="^test[.]t1"
    ```

=== "`-–tables-file` option"

    The `--tables-file` option specifies a file that can contain multiple table
    names, one table name per line in the file. Only the tables named in the file
    will be backed up. Names are matched exactly, case-sensitive, with no pattern or
    regular expression matching. The table names must be fully-qualified in
    `databasename.tablename` format.
    
    ```{.bash data-prompt="$"}
    $ echo "mydatabase.mytable" > /tmp/tables.txt
    $ xtrabackup --backup --tables-file=/tmp/tables.txt
    ```

=== "`--databases` option"

    The \` –databases\` option accepts a space-separated list of the databases
    and tables to backup in the `databasename[.tablename]` format. In addition to
    this list, make sure to specify the `mysql`, `sys`, and
    
    `performance_schema` databases. These databases are required when restoring
    the databases using xtrabackup –copy-back.
    
    !!! note
       
        Tables processed during the –prepare step may also be added to the backup
        even if they are not explicitly listed by the parameter if they were created
        after the backup started.
    
    ```{.bash data-prompt="$"}
    $ xtrabackup --databases='mysql sys performance_schema test ...'
    ```

=== "`--databases-file` option"

    The –databases-file option specifies a file that can contain multiple
    databases and tables in the `databasename[.tablename]` format, one element name per line in the file. Names are matched exactly, case-sensitive, with no pattern or regular expression matching.
    
    !!! note
       
        Tables processed during the –prepare step may also be added to the backup
        even if they are not explicitly listed by the parameter if they were created
        after the backup started.

## Next step

[Prepare the backup :material-arrow-right:](prepare-partial-backup.md){.md-button}