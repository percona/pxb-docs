# Next steps

This page provides recommendations for continuing your Percona XtraBackup learning after completing the quickstart.

## Continue learning Percona XtraBackup

The following resources expand on the concepts covered in the quickstart:

| Topic | Description |
|-------|-------------|
| [Create incremental backups](create-incremental-backup.md) | Back up only changed data to reduce backup time and storage |
| [Create compressed backups](create-compressed-backup.md) | Reduce backup size with compression |
| [Encrypt backups](encrypt-backups.md) | Protect backup data with encryption |
| [Stream backups to cloud storage](xbcloud-binary-overview.md) | Send backups directly to S3, GCS, or Azure |

## Docker Compose tutorial

For a production-ready approach to backup validation and disaster recovery, follow the [Docker Compose backup and restore tutorial](docker-compose-tutorial.md). This tutorial covers the following topics:

* Configure Docker Compose with backup profiles

* Validate backups before relying on them for recovery

* Simulate and recover from a disaster scenario

* Understand file permission requirements for containerized restores

## Production installation

The quickstart uses Docker for demonstration purposes. For production environments, install Percona XtraBackup directly on the database server.

See [Installation](installation.md) for package-based installation options.

## Related Percona products

The following Percona products work with Percona XtraBackup:

| Product | Purpose | Documentation |
|---------|---------|---------------|
| Percona Server for MySQL | MySQL-compatible database with performance enhancements | [Installation :octicons-link-external-16:](https://docs.percona.com/percona-server/{{vers}}/installation.html) |
| Percona XtraDB Cluster | High-availability MySQL clustering with Galera | [Installation :octicons-link-external-16:](https://docs.percona.com/percona-xtradb-cluster/{{vers}}/install-index.html) |
| Percona Monitoring and Management | Database monitoring and performance analysis | [Quickstart :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/3/quickstart/quickstart.html) |
| Percona Toolkit | Command-line tools for MySQL administration | [Documentation :octicons-link-external-16:](https://docs.percona.com/percona-toolkit/) |
