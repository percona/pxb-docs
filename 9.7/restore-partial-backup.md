> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-xtrabackup/9.7/llms.txt).

# Restore a partial backup

**Warning – Do Not Use –copy-back for Partial Restores**

Never copy back a prepared backup when you only need a subset of the data. Restoring partial backups should be done by importing the required tables (e.g., via logical dumps, mysqldump, or XtraBackup’s `--export`/`IMPORT TABLESPACE` workflow). Using the `--copy-back` (or `--move-back`) option in this scenario can leave the server in an inconsistent state because the InnoDB redo logs expect a complete data set.

Do not start incremental backups from a partial backup. Incremental backups rely on a full, consistent base; beginning a new incremental chain from an incomplete backup will produce unusable backup sets.

## Restore individual tables

Restore partial backups by restoring individual tables in the partial backup to the server. Use XtraBackup’s `--export` option during prepare, then import the tables using `IMPORT TABLESPACE`. For more information, see [Restore individual tables](https://docs.percona.com/percona-xtrabackup/9.7/restore-individual-tables.html).

## Related topics

- [Create a partial backup](https://docs.percona.com/percona-xtrabackup/9.7/create-partial-backup.html)
- [Prepare a partial backup](https://docs.percona.com/percona-xtrabackup/9.7/prepare-partial-backup.html)
