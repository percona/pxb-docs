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

* Use the `--databases` option to list the databases or specific tables

* Use the `--databases-file` option to list the databases or specific tables in a file

!!! note "Conflict between --tables and --databases"

    The `--tables` and `--databases` options use different filtering mechanisms and can conflict when used together.

    * `--tables` uses regular expressions and implies a partial backup.
    * `--databases` uses exact matching and implies a full backup of the listed databases.

    If you use both, you may get unexpected results (for example, a database listed in `--databases` might be fully backed up even if you only wanted specific tables from it via `--tables`). To combine specific tables from one database with full backups of other databases, use `--tables-file` instead of `--tables`.

## Filtering Behavior with Examples

To understand how filtering works, consider the following environment:

*   Database `testdb`: Contains tables `table1`, `table2`, and `table3`.
*   System Databases: `mysql`, `performance_schema`, `sys`.

**Goal**: Back up `testdb.table1`, `testdb.table2`, and all system databases (`mysql`, `performance_schema`, `sys`).

### Why mixing --tables and --databases fails

When determining whether to back up a table, xtrabackup follows this logic:

1.  **Database Check**: xtrabackup first checks if the database is included or excluded.
    *   If you use `--databases`, any database *not* in the list is skipped immediately.
    *   If a database is in the `--databases` list, it is marked to have **all its tables included** (unless `--tables-file` is also used).

2.  **Table Check**: If the database is not skipped:
    *   If the database was selected via `--databases`, **all** tables in it are copied, ignoring any `--tables` regex.
    *   If the database was not explicitly selected via `--databases` (or selected via `--tables-file`), it then checks the table name against the list.

This behavior explains why mixing `--tables` (regex) and `--databases` (list) often fails in the scenario above:

*   **Case 1**: `xtrabackup --backup --tables="testdb.table1" --databases="mysql"`
    *   `testdb` is NOT in `--databases`, so the database is skipped entirely. The result is that no tables from the `testdb` database are included.
*   **Case 2**: `xtrabackup --backup --tables="testdb.table1" --databases="mysql,testdb"`
    *   `testdb` IS in `--databases`. XtraBackup includes **all** tables in `testdb` (`table1`, `table2`, AND `table3`), ignoring the `--tables` regex.

### Solution: Combining specific tables and whole databases

If you want to back up specific tables from one database (e.g., `testdb.table1`, `testdb.table2`) while also backing up other databases (e.g., `mysql`, `performance_schema`, `sys`), use `--tables-file` or simply list the tables in `--databases` (or `--databases-file`).

#### Method 1: Using `--tables-file` (Recommended)

1.  Create a file listing the specific tables you want to back up. When using this method, you do **not** need to list the database of the specific tables in the `--databases` list; `--tables-file` automatically registers it.

    ```text
    testdb.table1
    testdb.table2
    ```

2.  Run xtrabackup using both `--tables-file` and `--databases`.

    ```bash
    xtrabackup --backup --tables-file=tables.txt --databases="mysql,performance_schema,sys" --target-dir=/data/backups/
    ```

In this configuration, `--tables-file` ensures the specific tables from `testdb` are backed up, while `--databases` ensures the system databases are backed up in full.

!!! note "Avoid Duplication"
    If you use `--tables-file` to back up specific tables from a database (e.g., `testdb`), do **not** also list that database (`testdb`) in the `--databases` option. Doing so will override the partial selection and back up the **entire** database.

#### Method 2: Using `--databases` for everything

You can also list the specific tables directly in the `--databases` option. This works because `--databases` supports `database.table` format.

This correctly instructs XtraBackup to take full backups of `mysql`, `performance_schema`, and `sys`, but only partial backups of `testdb`.

```bash
xtrabackup --backup --databases="mysql,performance_schema,sys,testdb.table1,testdb.table2" --target-dir=/data/backups/
```

!!! warning "Do Not Use Wildcards"
    Do not add `.*` to database names (e.g., `testdb.*`). This is not supported and will result in missing tables. Use the database name alone (`testdb`) for full backups.

## The `–-tables` option

The first method involves the xtrabackup `--tables` option. This option accepts either:
* A comma-separated list of fully qualified table names in the format `database.table` (for example, `db1.t1,db1.t2,db2.t3`)
* A POSIX regular expression surrounded by single quotes that is matched against the fully-qualified database name and table name using the `databasename.tablename` format

To back up only tables in the `test` database, use the following
command:

```bash
xtrabackup --backup --datadir=/var/lib/mysql --target-dir=/data/backups/ \
--tables="^test[.].*"
```

To back up only the `test.t1` table, use the following command:

```bash
xtrabackup --backup --datadir=/var/lib/mysql --target-dir=/data/backups/ \
--tables="^test[.]t1"
```

## The `-–tables-file` option

The `--tables-file` option specifies a file that can contain multiple table
names, one table name per line in the file. Only the tables named in the file
will be backed up. Names are matched exactly, case-sensitive, with no pattern or
regular expression matching. The table names must be fully-qualified in
`databasename.tablename` format.

```bash
echo "mydatabase.mytable" > /tmp/tables.txt
xtrabackup --backup --tables-file=/tmp/tables.txt
```

## The `--databases` and `-–databases-file` options

The `--databases` option accepts a comma-separated list of database names or table names. 

*   To back up an entire database, specify just the database name (e.g., `databasename`).
*   To back up specific tables, specify them in `database.table` format (e.g., `databasename.mytable`).

!!! note "No Wildcards or Regex"

    The `--databases` option does **not** support wildcards (like `*`) or regular expressions.

    *   Do **not** use `<database>.*`. This will look for a literal table named `*`, which will fail to back up your tables.
    *   To include all tables, simply use the database name: `databasename`.

This option is robust because it correctly registers the specific tables for partial backups, avoiding the conflicts that happen when mixing `--databases` (for full DBs) and `--tables` (for partials).

In addition to your selected databases, make sure to specify the `mysql`, `sys`, and `performance_schema` databases. These databases are required when restoring the databases using xtrabackup `--copy-back`.

!!! note
   
    Tables processed during the –prepare step may also be added to the backup
    even if they are not explicitly listed by the parameter if they were created
    after the backup started.

```bash
xtrabackup --backup --databases='mysql,sys,performance_schema,test' --target-dir=/data/backups/
```

## The `--databases-file` option

The –databases-file option specifies a file that can contain multiple
databases and tables in the `databasename[.tablename]` format, one element name per line in the file. Names are matched exactly, case-sensitive, with no pattern or regular expression matching.

*   To back up an entire database, specify just the database name (e.g., `databasename`).
*   To back up a specific table, specify `databasename.mytable`.
*   **Do not use** `.*` or regex (e.g., `databasename.*`). These are treated as literal names.

!!! note
   
    Tables processed during the –prepare step may also be added to the backup
    even if they are not explicitly listed by the parameter if they were created
    after the backup started.

The next step is to [prepare](prepare-partial-backup.md) the backup in order to restore it. 
