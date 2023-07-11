# Create a partial backup

*xtrabackup* supports taking partial backups when the
`innodb_file_per_table` option is enabled. There are three ways to create
partial backups:

1. matching the tables names with a regular expression

2. providing a list of table names in a file

3. providing a list of databases

!!! warning

    Do not copy back the prepared backup.

    Restoring partial backups should be done by importing the tables,
    not by using the –copy-back option. It is not
    recommended to run incremental backups after running a partial
    backup.

    Although there are some scenarios where restoring can be done by
    copying back the files, this may lead to database
    inconsistencies in many cases and it is not a recommended way to
    do it.

For the purposes of this manual page, we will assume that there is a database
named `test` which contains tables named `t1` and `t2`.

!!! warning

    If any of the matched or listed tables is deleted during the backup,
    *xtrabackup* will fail.

There are multiple ways of specifying which part of the whole data is backed up:

* Use the `--tables` option to list the table names

* Use the `--tables-file` option to list the tables in a file

* Use the `--databases` option to list the databases

* Use the `--databases-file` option to list the databases

## The `–-tables` option

The first method involves the xtrabackup –tables option. The option’s
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

## The `-–tables-file` option

The `--tables-file` option specifies a file that can contain multiple table
names, one table name per line in the file. Only the tables named in the file
will be backed up. Names are matched exactly, case-sensitive, with no pattern or
regular expression matching. The table names must be fully-qualified in
`databasename.tablename` format.

```{.bash data-prompt="$"}
$ echo "mydatabase.mytable" > /tmp/tables.txt
$ xtrabackup --backup --tables-file=/tmp/tables.txt
```

## The `--databases` and `-–databases-file` options

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

## The `--databases-file` option

The –databases-file option specifies a file that can contain multiple
databases and tables in the `databasename[.tablename]` format, one element name per line in the file. Names are matched exactly, case-sensitive, with no pattern or regular expression matching.

!!! note
   
    Tables processed during the –prepare step may also be added to the backup
    even if they are not explicitly listed by the parameter if they were created
    after the backup started.

The next step is to [prepare](prepare-partial-backup.md) the backup in order to restore it. 
