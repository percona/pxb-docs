> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-xtrabackup/8.4/llms.txt).

# Restore the backup

This tutorial describes how to restore a Percona XtraBackup backup to a new database container. The tutorial also covers validating the restored data.

## Learning objectives

This tutorial covers the following tasks:

- Create a restore target container
- Use `xtrabackup --copy-back` to restore physical backup files
- Fix file permissions required for MySQL to start
- Validate restored data accessibility

## Prerequisites

Complete the following quickstart steps before starting this tutorial:

- [Start Percona Server in a Docker container](https://docs.percona.com/percona-server/8.4/quickstart-docker.html) - Creates the `psmysql` container with the `mydb` database
- [Take a backup](https://docs.percona.com/percona-xtrabackup/8.4/quickstart-docker.html) - Creates the `backupvol` volume containing your prepared backup

### Understanding host terminal vs container

This tutorial requires running commands in two different places:

| Location      | Description                                                  | Prompt example |
| ------------- | ------------------------------------------------------------ | -------------- |
| Host terminal | Your computer’s command line where you run `docker` commands | `$` or `%`     |
| MySQL client  | Inside a container, connected to the database                | `mysql>`       |

Commands starting with `docker` always run on your host terminal. SQL commands like `SELECT` run inside the MySQL client.

### Verify the backup volume

Before proceeding, verify the backup volume exists.

If you are still in the MySQL client from the previous tutorial, exit to return to your host terminal:

```
exit
```

Expected output

```
Bye
```

Run the following command on your host terminal to verify the backup volume:

```
docker volume ls
```

Expected output

```
DRIVER    VOLUME NAME
local     backupvol
```

Confirm `backupvol` appears in the list. If the volume does not exist, complete the [Take a backup](https://docs.percona.com/percona-xtrabackup/8.4/quickstart-docker.html) tutorial first.

## Restore process overview

Restoring a physical backup requires copying the backup files to a MySQL data directory. In Docker environments, the restore process requires the following steps:

1. Create a target container - A Percona Server container receives the restored data
1. Stop the target database - MySQL cannot run while the restore process overwrites data files
1. Clear the data directory - The target directory must be empty before restoration
1. Copy the backup files - The `xtrabackup --copy-back` command transfers the files
1. Fix file permissions - Restored files have `root` ownership, but MySQL runs as the `mysql` user

For more information about the restore process, see [Restore full, incremental, and compressed backups](https://docs.percona.com/percona-xtrabackup/8.4/restore-a-backup.html).

## Step 1: Create a restore target container

Create a second Percona Server container named `ps-restore-target` as the restore destination. This configuration simulates restoring to a different server, a common disaster recovery scenario.

1. Create a Docker volume for the restore target:

   ```
   docker volume create restore_data
   ```

   Expected output

   ```
   restore_data
   ```

   This volume stores the restored database files.

1. Start a Percona Server container:

   **AMD64 (Intel/AMD)**

   ```
   docker run -d -p 3307:3306 --name ps-restore-target -e MYSQL_ROOT_PASSWORD=secret -v restore_data:/var/lib/mysql percona/percona-server:8.4
   ```

   **ARM64 (Apple Silicon Macs)**

   ```
   docker run -d -p 3307:3306 --name ps-restore-target -e MYSQL_ROOT_PASSWORD=secret -v restore_data:/var/lib/mysql percona/percona-server:8.4-aarch64
   ```

   Expected output

   ```
   4501d5524461b4483d414bd218d49ed4f47599add7d7fb81e157951a7a52f3d1
   ```

   The following table describes each option:

   | Option                           | Purpose                                                                      |
   | -------------------------------- | ---------------------------------------------------------------------------- |
   | `-d`                             | Runs the container in background mode                                        |
   | `-p 3307:3306`                   | Maps to port 3307 to avoid conflicts with the original database on port 3306 |
   | `--name ps-restore-target`       | Assigns a descriptive container name                                         |
   | `-e MYSQL_ROOT_PASSWORD=secret`  | Sets the root password, which MySQL requires for initialization              |
   | `-v restore_data:/var/lib/mysql` | Mounts the volume for data storage                                           |

1. Wait 30 seconds for container initialization, then verify the container status:

   ```
   docker ps --filter name=ps-restore-target
   ```

   Expected output

   ```
   CONTAINER ID   IMAGE                       COMMAND                  CREATED          STATUS          PORTS                               NAMES
   4501d552446    percona/percona-server:8.4  "/docker-entrypoint.…"   30 seconds ago   Up 29 seconds   33060/tcp, 0.0.0.0:3307->3306/tcp   ps-restore-target
   ```

## Step 2: Prepare the target for restore

Stop the database and clear the data directory before restoring. The `xtrabackup --copy-back` command requires an empty target directory.

1. Stop the restore target container:

   ```
   docker stop ps-restore-target
   ```

   Expected output

   ```
   ps-restore-target
   ```

   Database must be stopped

   MySQL locks data files while running. Overwriting locked files causes corruption or errors.

1. Clear the data directory:

   The `--rm` option creates a temporary container. Docker removes this container automatically after the command completes.

   **AMD64 (Intel/AMD)**

   ```
   docker run --volumes-from ps-restore-target -v backupvol:/backup_84 -it --rm --user root percona/percona-xtrabackup:8.4 /bin/bash -c "rm -rf /var/lib/mysql/*"
   ```

   **ARM64 (Apple Silicon Macs)**

   ```
   docker run --volumes-from ps-restore-target -v backupvol:/backup_84 -it --rm --user root percona/percona-xtrabackup:8.4-aarch64 /bin/bash -c "rm -rf /var/lib/mysql/*"
   ```

   If the command succeeds, the output is empty.

   This command performs the following actions:

   - Mounts the `restore_data` volume through `--volumes-from ps-restore-target`
   - Runs as `root` to obtain file deletion permissions
   - Removes all files from `/var/lib/mysql/`

## Step 3: Restore the backup files

Copy the backup files from `backupvol` to the restore target data directory.

1. Run the restore command:

   **AMD64 (Intel/AMD)**

   ```
   docker run --volumes-from ps-restore-target -v backupvol:/backup_84 -it --rm --user root percona/percona-xtrabackup:8.4 /bin/bash -c "xtrabackup --copy-back --datadir=/var/lib/mysql/ --target-dir=/backup_84"
   ```

   **ARM64 (Apple Silicon Macs)**

   ```
   docker run --volumes-from ps-restore-target -v backupvol:/backup_84 -it --rm --user root percona/percona-xtrabackup:8.4-aarch64 /bin/bash -c "xtrabackup --copy-back --datadir=/var/lib/mysql/ --target-dir=/backup_84"
   ```

   Expected output

   ```
   2024-10-07T14:08:59.127166-00:00 0 [Note] [MY-011825] [Xtrabackup] recognized server arguments: --datadir=/var/lib/mysql/
   2024-10-07T14:08:59.128951-00:00 0 [Note] [MY-011825] [Xtrabackup] recognized client arguments: --copy-back=1 --target-dir=/backup_84
   xtrabackup version 8.4.0-7 based on MySQL server 8.4.0 Linux (x86_64) (revision id: 4093cfd8)
   2024-10-07T14:08:59.129407-00:00 0 [Note] [MY-011825] [Xtrabackup] cd to /backup_84/

   ...

   2024-10-07T14:08:59.129407-00:00 0 [Note] [MY-011825] [Xtrabackup] Done: Copying ./ibtmp1 to /var/lib/mysql/ibtmp1 
   2024-10-07T14:08:59.129407-00:00 0 [Note] [MY-011825] [Xtrabackup] completed OK!
   ```

   The following table describes each xtrabackup option:

   | Option         | Purpose                                                                            |
   | -------------- | ---------------------------------------------------------------------------------- |
   | `--copy-back`  | Copies backup files to the data directory; use `--move-back` to move files instead |
   | `--datadir`    | Specifies the destination directory for restored files                             |
   | `--target-dir` | Specifies the source directory containing the prepared backup                      |

   For a complete list of options, see [xtrabackup option reference](https://docs.percona.com/percona-xtrabackup/8.4/xtrabackup-option-reference.html).

## Step 4: Fix file permissions

The restored files have `root` ownership because the restore command ran as root. MySQL runs as the `mysql` user and cannot read files owned by root.

1. Change ownership of the restored files:

   **AMD64 (Intel/AMD)**

   ```
   docker run --volumes-from ps-restore-target -v backupvol:/backup_84 -it --rm --user root percona/percona-xtrabackup:8.4 /bin/bash -c "chown -R mysql:mysql /var/lib/mysql/"
   ```

   **ARM64 (Apple Silicon Macs)**

   ```
   docker run --volumes-from ps-restore-target -v backupvol:/backup_84 -it --rm --user root percona/percona-xtrabackup:8.4-aarch64 /bin/bash -c "chown -R mysql:mysql /var/lib/mysql/"
   ```

   If the command succeeds, the output is empty.

   Required step

   Skipping the `chown` command causes MySQL to fail with permission errors:

   ```
   [ERROR] [MY-010187] [Server] Could not open file '/var/lib/mysql/ibdata1' for reading: Permission denied
   ```

   For more information about file permissions, see [Permissions](https://docs.percona.com/percona-xtrabackup/8.4/permissions.html).

1. Start the restore target container:

   ```
   docker start ps-restore-target
   ```

   Expected output

   ```
   ps-restore-target
   ```

1. Check the container logs to verify MySQL started:

   ```
   docker logs ps-restore-target 2>&1 | tail -5
   ```

   Expected output

   ```
   2024-10-07T14:10:15.123456Z 0 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
   2024-10-07T14:10:15.234567Z 0 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
   2024-10-07T14:10:15.345678Z 0 [System] [MY-011323] [Server] X Plugin ready for connections.
   2024-10-07T14:10:15.345678Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.4.0-1'  socket: '/var/lib/mysql/mysql.sock'  port: 3306  Percona Server (GPL), Release 1, Revision 238b3c02.
   ```

   The message `ready for connections` confirms the server started.

## Step 5: Validate the restored data

Connect to the restored database and verify data integrity.

1. Connect to the restored database:

   ```
   docker exec -it ps-restore-target mysql -uroot -p
   ```

   Expected output

   ```
   Enter password:
   Welcome to the MySQL monitor.  Commands end with ; or \g.
   Your MySQL connection id is 10
   Server version: 8.4.0-1 Percona Server (GPL), Release 1, Revision 238b3c02

   Copyright (c) 2009-2024 Percona LLC and/or its affiliates
   Copyright (c) 2000, 2024, Oracle and/or its affiliates.

   Oracle is a registered trademark of Oracle Corporation and/or its
   affiliates. Other names may be trademarks of their respective
   owners.

   Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

   mysql>
   ```

   Enter the password `secret` when prompted.

1. Verify the `mydb` database exists:

   ```
   SHOW DATABASES;
   ```

   Expected output

   ```
   +--------------------+
   | Database           |
   +--------------------+
   | information_schema |
   | mydb               |
   | mysql              |
   | performance_schema |
   | sys                |
   +--------------------+
   5 rows in set (0.03 sec)
   ```

1. Query the `employees` table data:

   ```
   SELECT * FROM mydb.employees;
   ```

   Expected output

   ```
   +----+--------------------+-----------------------------------+-------------+
   | id | name               | email                             | country     |
   +----+--------------------+-----------------------------------+-------------+
   |  1 | Erasmus Richardson | posuere.cubilia.curae@outlook.net | England     |
   |  2 | Jenna French       | rhoncus.donec@hotmail.couk        | Canada      |
   |  3 | Alfred Dejesus     | interdum@aol.org                  | Austria     |
   |  4 | Hamilton Puckett   | dapibus.quam@outlook.com          | Canada      |
   |  5 | Michal Brzezinski  | magna@icloud.pl                   | Poland      |
   |  6 | Zofia Lis          | zofial00@hotmail.pl               | Poland      |
   |  7 | Aisha Yakubu       | ayakubu80@outlook.com             | Nigeria     |
   |  8 | Miguel Cardenas    | euismod@yahoo.com                 | Peru        |
   |  9 | Luke Jansen        | nibh@hotmail.edu                  | Netherlands |
   | 10 | Roger Pettersen    | nunc@protonmail.no                | Norway      |
   +----+--------------------+-----------------------------------+-------------+
   10 rows in set (0.00 sec)
   ```

   The data restoration completed.

1. Exit the MySQL client:

   ```
   exit
   ```

   Expected output

   ```
   Bye
   ```

## Summary

This tutorial covered the following completed tasks:

- Created a restore target container named `ps-restore-target`
- Prepared the target by stopping MySQL and clearing the data directory
- Restored backup files using `xtrabackup --copy-back`
- Fixed file permissions with `chown -R mysql:mysql`
- Validated data recovery

## Next steps

[Clean up](https://docs.percona.com/percona-xtrabackup/8.4/quickstart-exit.html)
