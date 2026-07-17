# Quickstart Overview

Percona XtraBackup is a 100% open source backup solution for all versions of Percona Server for MySQL and MySQL® that performs online non-blocking, tightly compressed, highly secure full backups on transactional systems.

To quickly start with Percona XtraBackup, we recommend using Docker. This Quickstart guide focuses on this installation method. You can explore alternative installation options in the [Install](installation.md) section.

### Docker containers

Docker containers are built from Docker images, which are configuration snapshots needed to run applications. With Docker, you can build, deploy, run, update, and manage containers, which isolate applications from the host system. A Docker container lets you work with Percona XtraBackup without installing the product on a local drive.

Using Docker has benefits:

* Easily set up and use
* Doesn't change anything on your computer
* Simply remove it when you're done

## Quickstart Purpose

This section provides you with the basic steps to start Percona XtraBackup in a Docker container, take a backup, prepare a backup and restore a backup of Percona Server for MySQL database.

We use specific names in our examples, but feel free to change them if you want. Just remember that if you do, your results might be different from our guide.

When we talk about a "container," we mean the Docker container where Percona XtraBackup is running. When we say "instance," we're talking about the MySQL database server inside that container.

This guide will help you get started quickly, but there's a lot more to learn about database backups as you go along.

## Prerequisites

* [Install Docker :octicons-link-external-16:](https://docs.docker.com/engine/install/) on your system.

To take a backup of Percona Server for MySQL, run Percona Server for MySQL in a Docker container and create a database, and a table.

* [Start Percona Server in a Docker container :octicons-link-external-16:](https://docs.percona.com/percona-server/{{ps}}/quickstart-docker.html)
* [Create a database and table in Percona Server :octicons-link-external-16:](https://docs.percona.com/percona-server/{{ps}}/quickstart-docker.html#create-a-database)

### Limitations

Percona XtraBackup {{vers}} does not support making backups of databases created in versions before the {{vers}} series of MySQL, Percona Server for MySQL, or Percona XtraDB Cluster.

### Support servers and storage engines

Percona XtraBackup {{vers}} supports backing up data from various MySQL-compatible servers and storage engines.

Supported Servers:

* MySQL Server
* Percona Server for MySQL
* Percona XtraDB Cluster

Supported Storage Engines:

* InnoDB
* XtraDB
* MyISAM
* MyRocks

## Steps to perform

In this Quickstart, you will learn how to:
{.power-number}

1. [Start a Docker container and take a backup](quickstart-docker.md)
2. [Restore a backup](quickstart-restore-back.md)
3. [Clean up](quickstart-exit.md)
4. [Choose your next steps](quickstart-next-steps.md)
