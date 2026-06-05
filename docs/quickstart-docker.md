# Take a backup with Docker

This tutorial describes how to create a backup volume, run Percona XtraBackup in a Docker container, and take a prepared backup of a Percona Server for MySQL database.

## Learning objectives

This tutorial covers the following tasks:

* Create a Docker volume to store backup files

* Connect Percona XtraBackup to a running Percona Server container

* Take a full backup using `xtrabackup --backup`

* Prepare the backup using `xtrabackup --prepare`

## Prerequisites

Complete the following steps before starting this tutorial:

* [Install Docker :octicons-link-external-16:](https://docs.docker.com/engine/install/) on your system

* [Start Percona Server in a Docker container :octicons-link-external-16:](https://docs.percona.com/percona-server/{{vers}}/quickstart-docker.html) - Creates the `psmysql` container with the `mydb` database and `employees` table

## Architecture overview

Percona XtraBackup runs in a separate Docker container and connects to the Percona Server for MySQL container. This connection allows the backup tool to access the database files for backup and restore operations.

For more information about how Percona XtraBackup works, see [How Percona XtraBackup works](how-xtrabackup-works.md).

## Step 1: Create a backup volume

Docker volumes provide persistent storage that remains accessible across container restarts and updates. Creating a dedicated backup volume offers the following benefits:

* Data persists independently of container lifecycle

* Multiple containers can access the same backup data

* Backup files remain available for restore operations

Create the backup volume with the following command:

```shell
docker volume create backupvol
```
    
??? example "Expected output"

    ```{.text .no-copy}
    backupvol
    ```

## Step 2: Take and prepare the backup

The backup process requires connecting the Percona XtraBackup container to the Percona Server container. The `--user root` option grants the necessary permissions to access the MySQL data directory.

### Understand the command options

The following table describes each option used in the backup command:

| Option | Description |
|--------|-------------|
| `--name pxb` | Assigns the name `pxb` to the container |
| `--volumes-from psmysql` | Mounts volumes from the `psmysql` container to access database files |
| `-v backupvol:/backup_84` | Mounts the `backupvol` volume at `/backup_84` inside the container |
| `-it` | Allocates a pseudo-terminal for interactive password entry |
| `--user root` | Runs the container as root to access the MySQL data directory |
| `--password` | Prompts for the MySQL root password |

### Run the backup command

Select the command for your system architecture:

=== "AMD64 (Intel/AMD)"

    ```shell
    docker run --name pxb --volumes-from psmysql -v backupvol:/backup_84 -it --user root percona/percona-xtrabackup:8.4 /bin/bash -c "xtrabackup --backup --datadir=/var/lib/mysql/ --target-dir=/backup_84 --user=root --password; xtrabackup --prepare --target-dir=/backup_84"
    ```

=== "ARM64 (Apple Silicon Macs)"

    ```shell
    docker run --name pxb --volumes-from psmysql -v backupvol:/backup_84 -it --user root percona/percona-xtrabackup:8.4-aarch64 /bin/bash -c "xtrabackup --backup --datadir=/var/lib/mysql/ --target-dir=/backup_84 --user=root --password; xtrabackup --prepare --target-dir=/backup_84"
    ```

Enter the password `secret` when prompted:

```{.text .no-copy}
2024-10-07T13:55:47.640100-00:00 0 [Note] [MY-011825] [Xtrabackup] recognized server arguments: --datadir=/var/lib/mysql/
2024-10-07T13:55:47.641887-00:00 0 [Note] [MY-011825] [Xtrabackup] recognized client arguments: --backup=1 --target-dir=/backup_84 --user=root --password
Enter password:
```

??? example "Expected output"

    ```{.text .no-copy}
    xtrabackup version 8.4.0-1 based on MySQL server 8.4.0 Linux (x86_64) (revision id: 3792f907)
    2024-10-07T13:55:51.255518-00:00 0 [Note] [MY-011825] [Xtrabackup] perl binary not found. Skipping the version check
    2024-10-07T13:55:51.256080-00:00 0 [Note] [MY-011825] [Xtrabackup] Connecting to MySQL server host: localhost, user: root, password: set, port: not set, socket: not set
    2024-10-07T13:55:51.270222-00:00 0 [Note] [MY-011825] [Xtrabackup] Using server version 8.4.0-1
    2024-10-07T13:55:51.272839-00:00 0 [Note] [MY-011825] [Xtrabackup] Executing LOCK TABLES FOR BACKUP
        
    ...

    2024-10-07T13:55:55.550829-00:00 0 [Note] [MY-011825] [Xtrabackup] completed OK!
    ```

The command executes two xtrabackup operations:

* `xtrabackup --backup` - Copies data files from `/var/lib/mysql/` to `/backup_84`

* `xtrabackup --prepare` - Applies transaction logs to make the backup consistent

For more information about the backup and prepare process, see [Create a full backup](create-full-backup.md) and [Prepare a full backup](prepare-full-backup.md).

!!! warning "Password visibility"

    Specifying the password directly with `--password=secret` exposes the password in `docker ps`, `docker history`, and system process listings. Use the interactive prompt for production environments.

## Step 3: Verify the backup

Check the backup container logs to confirm the backup completed:

```shell
docker container logs pxb
```

??? example "Expected output"

    ```{.text .no-copy}
    ...
    2024-10-07T13:55:55.550829-00:00 0 [Note] [MY-011825] [Xtrabackup] completed OK!
    ```

The message `completed OK!` confirms the backup and prepare operations finished.

## Summary

This tutorial covered the following completed tasks:

* Created the `backupvol` Docker volume for backup storage

* Connected the Percona XtraBackup container to the `psmysql` database container

* Executed `xtrabackup --backup` to copy database files

* Executed `xtrabackup --prepare` to make the backup consistent

The backup stored in `backupvol` is ready for restoration.

## Next steps

[Restore the backup](quickstart-restore-back.md){.md-button}
