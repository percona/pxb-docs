# Overview

Percona XtraBackup is a 100% open source backup solution for all versions of Percona Server for MySQL and MySQL® that performs online non-blocking, tightly compressed, highly secure full backups on transactional systems.

To start with Percona XtraBackup quickly, we recommend using Docker and this Quickstart guide focuses on this installation method. You can explore alternative installation options in the [Install](installation.md) section.

### Why to start Percona XtraBackup in a Docker container

Docker containers are built from Docker images, which are snapshots of the configuration needed to run an applications, such as the code, and libraries. With Docker, you can build, deploy, run, update, and manage containers, which isolate applications from the host system. A Docker container lets you work with Percona XtraBackup without installing the product on a local drive.

## Purpose of the Quickstart

This section provides you with the basic steps to quiclky start Percona XtraBackup in a Docker continer, take a backup, prepare a backup and restore a backup of Percona Server for MySQL database.

You are welcome to change the names of any items in commands. If you do, the results may vary from those we provide in this Quickstart guide.

In this section, container refers to the Docker container and instance refers to the database server in the container.

## Prerequisites

* [Install Docker](https://docs.docker.com/engine/install/) on your system.

To take a backup of Percona Server for MySQL, run Percona Server for MySQL in a Docker container and create a database, and a table.

* [Start Percona Server in a Docker container](https://docs.percona.com/percona-server/8.0/quickstart-docker.html)
* [Create a database and table in Percona Server](https://docs.percona.com/percona-server/8.0/quickstart-docker.html#create-a-database)

### Limitations

Percona XtraBackup 8.0 does not support making backups of databases created in versions before the 8.0 series of MySQL, Percona Server for MySQL, or Percona XtraDB Cluster or versions greater than 8.0, such as the 8.1 Innovation release. 

### Supported servers

Percona XtraBackup 8.0 can back up data stored on MySQL servers, Percona Server for MySQL, and Percona XtraDB Cluster.

### Supported storage engines

Percona XtraBackup 8.0 can back up data from InnoDB, XtraDB, MyISAM, and MyRocks tables.

## Steps to perform

In this Quickstart, you will learn how to:
{.power-number}

1. [Start a Docker container and take a backup](quickstart-docker.md)
2. [Restore a backup](quickstart-restore-backup.md)
3. [Clean up](quickstart-exit.md)
4. [Choose your next steps](quickstart-next-steps.md)

## Next steps

[Start a Docker container and take a backup :material-arrow-right:](quickstart-docker.md){.md-button}

