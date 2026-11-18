# xtrabackup exit codes

The *xtrabackup* binary exits with the traditional success value of 0 after a backup when no error occurs. If an error occurs during the backup, the exit value is 1.

An exception applies to Percona XtraBackup versions earlier than 9.7.2-3. These versions exit with `2` on a Vector Search redo log record. Percona Server for MySQL 9.7.4-4 writes this record type. For details, see [Backup fails on a Percona Server for MySQL 9.7.4-4 database that uses Vector Search](faq.md#backup-fails-on-a-percona-server-for-mysql-974-4-database-that-uses-vector-search).

In certain cases, the exit value can be something other than 0 or 1, due to the command-line option code included from the *MySQL* libraries. An unknown command-line option, for example, will cause an exit code of 255.
