# Differences between a logical backup and Percona XtraBackup

You'll notice several key differences when transitioning from a logical database backup to Percona XtraBackup. A logical backup contains the database contents as SQL or similar logical data (tables, schemas, procedures); see the [Glossary](glossary.md#logical-backup). A physical backup copies the database’s raw data files from disk; see the [Glossary](glossary.md#physical-backup). The following table summarizes how they differ.

| Type | Logical backup | Physical backup |
|------|----------------|-----------------|
| Definition | Contains logical data (tables, schemas, procedures). | Copies entire database directories and files. |
| Method | Exported as binary files using EXPORT/IMPORT tools. | Copies raw data files directly from the database. |
| Data contents | Includes data structure (schema, tables, procedures). | Contains complete data (structure, tables, transactions). |
| Instance Independence | Can be restored on any other machine or environment. | Tied to the specific database instance and environment. |
| OS-level restoration | Not suitable for OS-level restoration. | Suitable for full disaster recovery scenarios. |
| Granularity | Granular recovery of specific components (for example, one table or schema). | Typically full restore; XtraBackup also supports [partial backup](create-partial-backup.md) and [restore individual tables](restore-individual-tables.md). |
| Performance | For full backup/restore, slower (SQL parsing and execution); partial restore of one table can be faster. | For full backup/restore, faster (direct file copying); bottleneck is often disk or network I/O. |
| Use cases | Data migration, platform-independent copies, version or engine change. | Full database restoration, disaster recovery. |
| Security | Unencrypted dumps are human-readable; security depends on encryption and access control. | Binary files are less directly readable when unencrypted; security depends on encryption and access control for both. |

Physical backups are suitable for OS-level restoration (copying back the database files and directory structure) and full disaster recovery (recovering systems and data after a major failure). Percona XtraBackup is designed to perform hot backups (backups taken while the database is running and in use) of MySQL, Percona Server for MySQL, and other MySQL-compatible databases without interrupting database services. XtraBackup performs physical backups by copying the data files; impact on server performance is often relatively low compared to blocking backup methods, but it depends on I/O load and workload. XtraBackup includes backup compression and encryption, and a [streaming backup](take-streaming-backup.md) option for large databases or transferring backups to another server. Many logical backup tools (for example, a plain `mysqldump` run) do not build in compression, encryption, or streaming; you can add them via external pipelines, while XtraBackup provides these in one tool. XtraBackup also integrates with [Percona Toolkit](https://docs.percona.com/percona-toolkit/) and [Percona Monitoring and Management (PMM)](https://docs.percona.com/pmm/) for monitoring and management.

Another difference is the support for [incremental backups](create-incremental-backup.md) with XtraBackup. You can back up only the data that has changed since the last full backup, significantly reducing the time and storage requirements compared to a full logical backup.

## Logical backups in more detail

A logical backup contains copies of information about a database, such as tables, schemas (the structure of the database: tables, columns, indexes), and procedures (reusable SQL code stored in the database). Commonly, these backups are exported as binary or text files using export/import tools (for example, `mysqldump`).

Logical backups focus on the data structure and SQL statements. You can back up a selected set of data or exclude specific data during the export, saving time and storage. They contain only structural information about the database, not instance-specific details (that is, details tied to one running copy of the database server).

For full backup and full restore, logical backups are usually slower than physical backups because of SQL parsing and execution; for restoring a single table, a logical dump of that table can be faster than preparing and extracting from a physical backup. A logical backup does not preserve the file system-level security settings, user accounts, privileges, or authentication settings. During restoration, you must manually reconfigure these settings.

You can restore a logical backup on any other machine and in different environments. Logical backups provide granular recovery (restoring only selected parts, such as individual tables or schemas) instead of the whole database. The recovery process can be more involved because it may require recreating the data structure.

Use logical backups when restoring or moving a database copy to another environment; they are well suited to platform-independent data migration (restoring on different operating systems or hardware). When the goal is to change MySQL version, storage engine, or move to another database product, logical backup or logical export is often the only practical option—physical backups are tied to the same engine and often the same minor version.

When unencrypted, logical backup files (for example, SQL from `mysqldump`) are human-readable, so anyone with access can read sensitive data. Both logical and physical backups need access control and encryption for strong security.

## Physical backups and Percona XtraBackup in more detail

Percona XtraBackup is a physical backup tool. It copies the database’s data files and log files from disk while the server is running (hot backup), then uses a prepare step to apply redo and undo so the copy is consistent. Because it works at the file level, full backup and full restore are usually faster than with logical backups, and the result is suitable for same-version, same-engine restore and for disaster recovery.

XtraBackup supports [full](create-full-backup.md), [incremental](create-incremental-backup.md), and [compressed](create-compressed-backup.md) backups, plus [encryption](encrypt-backups.md) and [streaming](take-streaming-backup.md) to remote storage. You can also take [partial backups](create-partial-backup.md) or back up [individual partitions](create-individual-partition-backup.md), and [restore individual tables](restore-individual-tables.md) when needed. Backup impact on the server is usually moderate; it depends on I/O load and is often lower than with blocking methods such as `FLUSH TABLES WITH READ LOCK`.

Use physical backups with XtraBackup when you need fast, non-blocking backups and restores on the same MySQL-compatible server (same or compatible version and engine). For migrating to a different version, engine, or database product, use logical backup or export instead.

!!! admonition "See also"

    [How Percona XtraBackup works](how-xtrabackup-works.md)

    [Backup process overview](backup-overview.md)

    [Backup strategy and backup policy](backup-strategy.md)

    [Create a full backup](create-full-backup.md)

    [Restore a backup](restore-a-backup.md)

    [Glossary](glossary.md) (logical backup, physical backup)
