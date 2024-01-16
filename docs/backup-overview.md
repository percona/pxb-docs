# Backup process overview

Percona Xtrabackup is a tool that allows you to create backups of MySQL or MariaDB databases. It works by copying the data files and the binary log files of the server, while ensuring that the data is consistent and not corrupted by ongoing transactions. Percona Xtrabackup can also prepare the backup files for restoration, apply incremental backups, and stream the backup files to another server or storage device.

## Backup types

You can take and prepare the following types of backups:

* [Full backup](create-full-backup.md) - a backup of all the contents of the database

* [Incremental backup](create-incremental-backup.md) - a backup of only the files that have changed since the last full backup

* [Compressed backup](create-compressed-backup.md) - a backup of all the contents of the database with applying a compression algorithm that reduces the size of the data to be stored

* [Partial backup](create-partial-backup.md) - a backup of only the files that have changed in a specific folder or a set of folders, rather than the entire database

* [Individual partitions backup](create-individual-partition-backup.md) - a backup of an individual partition

## Backup restoration

* [Restore full, incremental, compressed backups](restore-a-backup.md)

* [Restore a partial backup](restore-partial-backup.md)

* [Restore an individual partitions backup](restore-individual-partitions.md)

* [Restore individual tables](restore-individual-tables.md)



