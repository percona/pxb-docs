> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-xtrabackup/9.7/llms.txt).

# Backup process overview

Percona Xtrabackup is a tool that allows you to create backups of MySQL or MariaDB databases. It works by copying the data files and the binary log files of the server, while ensuring that the data is consistent and not corrupted by ongoing transactions. Percona Xtrabackup can also prepare the backup files for restoration, apply incremental backups, and stream the backup files to another server or storage device.

## Backup types

You can take and prepare the following types of backups:

- [Full backup](https://docs.percona.com/percona-xtrabackup/9.7/create-full-backup.html) - a backup of all the contents of the database
- [Incremental backup](https://docs.percona.com/percona-xtrabackup/9.7/create-incremental-backup.html) - a backup of only the files that have changed since the last full backup
- [Compressed backup](https://docs.percona.com/percona-xtrabackup/9.7/create-compressed-backup.html) - a backup of all the contents of the database with applying a compression algorithm that reduces the size of the data to be stored
- [Partial backup](https://docs.percona.com/percona-xtrabackup/9.7/create-partial-backup.html) - a backup of only the files that have changed in a specific folder or a set of folders, rather than the entire database
- [Individual partitions backup](https://docs.percona.com/percona-xtrabackup/9.7/create-individual-partition-backup.html) - a backup of an individual partition

## Backup restoration

- [Restore full, incremental, compressed backups](https://docs.percona.com/percona-xtrabackup/9.7/restore-a-backup.html)
- [Restore a partial backup](https://docs.percona.com/percona-xtrabackup/9.7/restore-partial-backup.html)
- [Restore an individual partitions backup](https://docs.percona.com/percona-xtrabackup/9.7/restore-individual-partitions.html)
- [Restore individual tables](https://docs.percona.com/percona-xtrabackup/9.7/restore-individual-tables.html)
