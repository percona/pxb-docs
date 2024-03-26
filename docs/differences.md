
# Differences between a logical backup and Percona XtraBackup

You'll notice several key differences when transitioning from a logical database to Percona XtraBackup.

| Type                  | Logical backup                                        | Physical backup                                          |
|-----------------------|-------------------------------------------------------|----------------------------------------------------------|
| Definition            | Contains logical data (tables, schemas, procedures).  | Copies entire database directories and files.            |
| Method                | Exported as binary files using EXPORT/IMPORT tools.   | Copies raw data files directly from the database.        |
| Data contents         | Includes data structure (schema, tables, procedures). | Contains complete data (structure, tables, transactions) |
| Instance Independence | Can be restored on any other machine or environment.  | Tied to the specific database instance and environment.  |
| OS-level restoration  | Not suitable for OS-level restoration                 | Suitable for full disaster recovery scenarios.           |
| Granularity           | Granular recovery of specific components.             | Restores the entire database.                            |
| Performance           | Slower due to SQL parsing and execution               | Faster due to direct file copying                        |
| Use cases             | Data migration platform-independent copies            | Full database restoration, disaster recovery             |
| Security              | Less secure                                           | More secure                                              |


XtraBackup is designed to perform hot backups of MySQL, MariaDB, and Percona Server databases without interrupting database services. XtraBackup performs physical backups by copying the data files, ensuring minimal impact on server performance. XtraBackup includes advanced features such as backup compression and encryption, providing efficient and secure data protection. The tool also offers a streaming backup option, which is useful for backing up large databases or transferring backups to another server. XtraBackup integrates with Percona's additional tools like Percona Toolkit and Percona Monitoring and Management (PMM), offering a comprehensive database performance monitoring, management, and optimization solution. These features are not typically found in logical database backup solutions.

Another difference is the support for incremental backups with XtraBackup. You can back up only the data that has changed since the last full backup, significantly reducing the time and storage requirements compared to a full logical backup.

A logical backup contains copies of information about a database, such as tables, schemas, and procedures. Commonly, these backups are exported as binary files using EXPORT/IMPORT tools. Logical backups focus on the data structure and SQL statements, and you can back up a selected set of data or exclude specific data during the export, saving time and storage. They contain only structural information about the database, not instance-specific details. Logical backups are slower than physical backups because of the SQL parsing and execution. A logical backup does not preserve the file system-level security settings, user accounts, privileges, or authentication settings. During restoration, you must manually reconfigure these settings.

You can restore a logical backup on any other machine and in different environments. Logical backups provide granular recovery capabilities to restore specific components, such as individual tables or schemas. The recovery process can be more difficult because it involves recreating the entire data structure.
Use logical backups when restoring or moving a database copy to another environment.
They are an option for platform-independent data migration.

Unlike physical backups, logical backups are less secure because the data is unencrypted. Anyone with access to the backup could read sensitive information. 





