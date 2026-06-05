# Quickstart overview

Percona XtraBackup performs online, non-blocking physical backups for Percona Server for MySQL and MySQL databases. This quickstart guide uses Docker to demonstrate backup and restore operations.

For alternative installation methods, see [Installation](installation.md).

## Why use Docker for this quickstart

Docker containers isolate applications from the host system. Running Percona XtraBackup in a container provides the following benefits:

* No installation required on the host system

* Consistent environment across different operating systems

* Complete removal leaves no residual files

For production deployments, see [Installation](installation.md) for package-based installation options.

## Supported configurations

Verify your environment meets the following requirements before starting.

### Supported servers

Percona XtraBackup {{vers}} supports the following MySQL-compatible servers:

* MySQL Server

* Percona Server for MySQL

* Percona XtraDB Cluster

### Supported storage engines

Percona XtraBackup {{vers}} supports the following storage engines:

* InnoDB

* MyISAM

* MyRocks

* XtraDB

### Version requirements

Percona XtraBackup {{vers}} requires databases created with the {{vers}} series or later. Databases created with earlier MySQL, Percona Server for MySQL, or Percona XtraDB Cluster versions are not supported.

For detailed version compatibility information, see [Server and backup version comparison](server-backup-version-comparison.md).

## Prerequisites

Both learning paths require [Docker :octicons-link-external-16:](https://docs.docker.com/engine/install/) installed on your system. Each tutorial includes specific setup instructions for Percona Server for MySQL.

## Choose your learning path

This quickstart offers two paths based on your experience level and goals:

| Path | Best for | Time | Topics covered |
|------|----------|------|----------------|
| [Basic quickstart](quickstart-docker.md) | First-time users learning core concepts | 15-20 min | Single backup, restore, validation |
| [Docker Compose tutorial](docker-compose-tutorial.md) | Production-oriented users | 30-40 min | Backup profiles, validation testing, disaster recovery |

### Basic quickstart

The [basic quickstart](quickstart-docker.md) teaches core Percona XtraBackup operations using individual Docker commands:

* Create a backup volume

* Take and prepare a full backup

* Restore a backup to a new container

* Validate restored data

### Docker Compose tutorial

The [Docker Compose tutorial](docker-compose-tutorial.md) demonstrates a production-ready backup workflow with separate services for backup, validation, and restore:

* Configure Docker Compose with backup profiles

* Validate backups before relying on them for recovery

* Simulate a disaster scenario

* Execute a complete restore operation

* Understand file permission requirements

## Terminology

This quickstart uses the following terms:

| Term | Definition |
|------|------------|
| Container | The Docker container running Percona XtraBackup or Percona Server |
| Instance | The MySQL database server process running inside a container |
| Volume | Docker persistent storage that survives container restarts |
| Prepared backup | A backup with transaction logs applied, ready for restoration |

For additional terminology, see [Glossary](glossary.md).
