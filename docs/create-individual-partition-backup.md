# Create an individual partitions backup

Percona XtraBackup lets you back up
individual partitions because partitions are regular tables with specially formatted names. The only requirement for this feature is to enable the `innodb_file_per_table` option
on the server.

There is one caveat about using this kind of backup: you can not copy back
the prepared backup. Restoring partial backups should be done by importing the
tables.

There are three ways of specifying which part of the whole data will be backed
up: regular expressions (`--tables`), enumerating the
tables in a file (`--tables-file`) or providing a list of
databases (`--databases`).

The regular expression provided to this option will be matched against the fully
qualified database name and table name, in the form of
`database-name.table-name`.

If the partition 0 is not backed up, Percona XtraBackup cannot generate a .cfg file. MySQL 8.0 stores the table metadata in partition 0.

For example, this operation takes a back-up of the partition `p4` from 
the table `name` located in the database `imdb`:

```{.bash data-prompt="$"}
$ xtrabackup --tables=^imdb[.]name#p#p4 --backup
```

If partition 0 is not backed up, the following errors may occur:

??? example "The error message"

    ```{.text .no-copy}
    xtrabackup: export option not specified
    xtrabackup: error: cannot find dictionary record of table imdb/name#p#p4
    ```

Note that this option is passed to `xtrabackup --tables` and is matched
against each table of each database, the directories of each database will be
created even if they are empty.

## Next step

[Prepare an individual partitions backup :material-arrow-right:](prepare-individual-partitions-backup.md){.md-button}
