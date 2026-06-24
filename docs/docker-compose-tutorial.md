# Docker Compose backup and restore tutorial

This tutorial demonstrates a production-ready approach to backing up, validating, and restoring Percona Server for MySQL using Percona XtraBackup in a Docker Compose environment.

## Overview

In a containerized environment, restoring a physical backup requires a strict sequence because you cannot overwrite data files while the database engine is running. Furthermore, physical files recovered by the `root` user cause permissions errors when the database tries to boot as the `mysql` user.

This tutorial teaches you to:

* Set up a complete Docker Compose environment with Percona Server and Percona XtraBackup
* Take and prepare a full backup
* Validate that the backup is functional before using it
* Simulate a disaster scenario
* Execute a complete restore operation
* Understand the critical role of file permissions in containerized restores

## Prerequisites

* [Docker :octicons-link-external-16:](https://docs.docker.com/engine/install/) installed on your system
* [Docker Compose :octicons-link-external-16:](https://docs.docker.com/compose/install/) installed (included with Docker Desktop)
* Basic familiarity with Docker concepts

## Architecture

This tutorial uses Docker Compose profiles to separate backup operations into distinct tasks:

| Profile | Service | Purpose |
|---------|---------|---------|
| (default) | `psmysql` | Primary Percona Server for MySQL instance |
| `backup` | `pxb-backup` | Takes and prepares backups |
| `validate` | `pxb-validate` | Launches an isolated database from backup files |
| `restore` | `pxb-restore` | Restores backup files to the primary database |

Using profiles ensures that backup, validation, and restore operations only run when explicitly invoked.

## Step 1: Set up the project structure

Create a project directory with the following structure:
{.power-number}

1. Create the project directory and navigate to it:

    ```shell
    mkdir pxb-tutorial && cd pxb-tutorial
    ```

    If the command executes successfully, the expected output is empty. You are now in the `pxb-tutorial` directory.

2. Create the secrets directory:

    ```shell
    mkdir secrets
    ```

    If the command executes successfully, the expected output is empty.

3. Create the password file:

    ```shell
    echo "YourSecurePassword123" > secrets/db_root_pwd.txt
    ```

    If the command executes successfully, the expected output is empty.

    !!! warning
    
        In production, use a strong, randomly generated password and secure the secrets directory with appropriate file permissions.

4. Verify the project structure:

    ```shell
    ls -la
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        total 0
        drwxr-xr-x  3 user  staff   96 Jun  4 10:00 .
        drwxr-xr-x  5 user  staff  160 Jun  4 10:00 ..
        drwxr-xr-x  3 user  staff   96 Jun  4 10:00 secrets
        ```

## Step 2: Create the Docker Compose file

Create a file named `docker-compose.yml` in your project directory. Select the configuration for your system architecture:

=== "AMD64 (Intel/AMD)"

    ```yaml
    services:
      # Main Database Engine
      psmysql:
        image: percona/percona-server:8.4
        container_name: psmysql
        environment:
          MYSQL_ROOT_PASSWORD_FILE: /run/secrets/db_root_pwd
        volumes:
          - mysql_data:/var/lib/mysql
        ports:
          - "3306:3306"
        secrets:
          - db_root_pwd

      # BACKUP & PREPARE TASK
      pxb-backup:
        image: percona/percona-xtrabackup:8.4
        container_name: pxb_backup
        user: root
        depends_on:
          - psmysql
        volumes:
          - mysql_data:/var/lib/mysql:ro
          - backupvol:/backup_84
        secrets:
          - db_root_pwd
        command: >
          /bin/bash -c "
          export MYSQL_PWD=$$(cat /run/secrets/db_root_pwd);
          xtrabackup --backup --datadir=/var/lib/mysql/ --target-dir=/backup_84 --user=root;
          xtrabackup --prepare --target-dir=/backup_84
          "
        profiles:
          - backup

      # RESTORE TASK (Destructive - Requires psmysql to be stopped)
      pxb-restore:
        image: percona/percona-xtrabackup:8.4
        container_name: pxb_restore
        user: root
        volumes:
          - mysql_data:/var/lib/mysql
          - backupvol:/backup_84
        command: >
          /bin/bash -c "
          echo '==> Clearing current database directory...';
          rm -rf /var/lib/mysql/* &&
          echo '==> Restoring physical data files from backupvol...';
          xtrabackup --copy-back --target-dir=/backup_84 --datadir=/var/lib/mysql/ &&
          echo '==> Fixing file permissions for Percona Server...';
          chown -R mysql:mysql /var/lib/mysql
          "
        profiles:
          - restore

      # VALIDATION TASK (Launches an isolated, temporary DB from the backup)
      pxb-validate:
        image: percona/percona-server:8.4
        container_name: pxb_validate
        environment:
          MYSQL_ROOT_PASSWORD_FILE: /run/secrets/db_root_pwd
        volumes:
          - backupvol:/var/lib/mysql
        ports:
          - "3307:3306"
        secrets:
          - db_root_pwd
        user: root
        entrypoint: >
          /bin/bash -c "
          chown -R mysql:mysql /var/lib/mysql &&
          exec gosu mysql mysqld
          "
        profiles:
          - validate

    volumes:
      mysql_data:
      backupvol:

    secrets:
      db_root_pwd:
        file: ./secrets/db_root_pwd.txt
    ```

=== "ARM64 (Apple Silicon Macs)"

    ```yaml
    services:
      # Main Database Engine
      psmysql:
        image: percona/percona-server:8.4-aarch64
        container_name: psmysql
        environment:
          MYSQL_ROOT_PASSWORD_FILE: /run/secrets/db_root_pwd
        volumes:
          - mysql_data:/var/lib/mysql
        ports:
          - "3306:3306"
        secrets:
          - db_root_pwd

      # BACKUP & PREPARE TASK
      pxb-backup:
        image: percona/percona-xtrabackup:8.4-aarch64
        container_name: pxb_backup
        user: root
        depends_on:
          - psmysql
        volumes:
          - mysql_data:/var/lib/mysql:ro
          - backupvol:/backup_84
        secrets:
          - db_root_pwd
        command: >
          /bin/bash -c "
          export MYSQL_PWD=$$(cat /run/secrets/db_root_pwd);
          xtrabackup --backup --datadir=/var/lib/mysql/ --target-dir=/backup_84 --user=root;
          xtrabackup --prepare --target-dir=/backup_84
          "
        profiles:
          - backup

      # RESTORE TASK (Destructive - Requires psmysql to be stopped)
      pxb-restore:
        image: percona/percona-xtrabackup:8.4-aarch64
        container_name: pxb_restore
        user: root
        volumes:
          - mysql_data:/var/lib/mysql
          - backupvol:/backup_84
        command: >
          /bin/bash -c "
          echo '==> Clearing current database directory...';
          rm -rf /var/lib/mysql/* &&
          echo '==> Restoring physical data files from backupvol...';
          xtrabackup --copy-back --target-dir=/backup_84 --datadir=/var/lib/mysql/ &&
          echo '==> Fixing file permissions for Percona Server...';
          chown -R mysql:mysql /var/lib/mysql
          "
        profiles:
          - restore

      # VALIDATION TASK (Launches an isolated, temporary DB from the backup)
      pxb-validate:
        image: percona/percona-server:8.4-aarch64
        container_name: pxb_validate
        environment:
          MYSQL_ROOT_PASSWORD_FILE: /run/secrets/db_root_pwd
        volumes:
          - backupvol:/var/lib/mysql
        ports:
          - "3307:3306"
        secrets:
          - db_root_pwd
        user: root
        entrypoint: >
          /bin/bash -c "
          chown -R mysql:mysql /var/lib/mysql &&
          exec gosu mysql mysqld
          "
        profiles:
          - validate

    volumes:
      mysql_data:
      backupvol:

    secrets:
      db_root_pwd:
        file: ./secrets/db_root_pwd.txt
    ```

!!! note "About the `$$` syntax"

    The `$$` in the YAML file escapes the `$` character for Docker Compose. Docker Compose interprets `$` as a variable, so `$$` produces a literal `$` in the command.

### Key configuration details

| Configuration | Explanation |
|---------------|-------------|
| `user: root` | Required for `pxb-backup` and `pxb-restore` to access MySQL data files and modify permissions |
| `mysql_data:/var/lib/mysql:ro` | The `:ro` flag mounts the volume as read-only for the backup service, ensuring data integrity |
| `chown -R mysql:mysql` | Resets file ownership after restore; MySQL refuses to start if files are owned by `root` |
| `profiles` | Services only start when their profile is explicitly activated |
| `gosu mysql mysqld` | Drops from `root` to `mysql` user before starting the database |

## Step 3: Start the primary database and add test data

Start the primary Percona Server instance and create some test data.
{.power-number}

1. Start the primary database:

    ```shell
    docker compose up -d psmysql
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        [+] Running 3/3
         ✔ Network pxb-tutorial_default  Created
         ✔ Volume "pxb-tutorial_mysql_data"  Created
         ✔ Container psmysql  Started
        ```

2. Wait for the database to initialize (about 30 seconds), then connect to it:

    ```shell
    docker exec -it psmysql mysql -uroot -p
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Enter password:
        Welcome to the MySQL monitor.  Commands end with ; or \g.
        Your MySQL connection id is 8
        Server version: 8.4.2-2 Percona Server (GPL), Release 2, Revision b575402d

        Copyright (c) 2009-2024 Percona LLC and/or its affiliates
        Copyright (c) 2000, 2024, Oracle and/or its affiliates.

        Oracle is a registered trademark of Oracle Corporation and/or its
        affiliates. Other names may be trademarks of their respective
        owners.

        Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

        mysql>
        ```

    Enter the password from your secrets file (`YourSecurePassword123`) when prompted.

3. Create a test database and table:

    ```sql
    CREATE DATABASE mydb;
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Query OK, 1 row affected (0.01 sec)
        ```

    ```sql
    USE mydb;
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Database changed
        ```

    ```sql
    CREATE TABLE employees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        country VARCHAR(50)
    );
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Query OK, 0 rows affected (0.03 sec)
        ```

    ```sql
    INSERT INTO employees (name, email, country) VALUES
        ('Erasmus Richardson', 'erasmus@example.com', 'England'),
        ('Jenna French', 'jenna@example.com', 'Canada'),
        ('Alfred Dejesus', 'alfred@example.com', 'Austria');
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Query OK, 3 rows affected (0.01 sec)
        Records: 3  Duplicates: 0  Warnings: 0
        ```

4. Verify the data was inserted:

    ```sql
    SELECT * FROM employees;
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        +----+--------------------+---------------------+---------+
        | id | name               | email               | country |
        +----+--------------------+---------------------+---------+
        |  1 | Erasmus Richardson | erasmus@example.com | England |
        |  2 | Jenna French       | jenna@example.com   | Canada  |
        |  3 | Alfred Dejesus     | alfred@example.com  | Austria |
        +----+--------------------+---------------------+---------+
        3 rows in set (0.00 sec)
        ```

5. Exit the MySQL client:

    ```sql
    exit
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Bye
        ```

## Step 4: Take and prepare a backup

Run the backup service to create a full backup and prepare it for restoration.
{.power-number}

1. Run the backup task:

    ```shell
    docker compose run --rm pxb-backup
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        xtrabackup version 8.4.0-2 based on MySQL server 8.4.2 Linux (x86_64)
        ...
        [Note] [MY-011825] [Xtrabackup] Executing LOCK TABLES FOR BACKUP
        ...
        [Note] [MY-011825] [Xtrabackup] completed OK!

        [Note] [MY-011825] [Xtrabackup] recognized server arguments: --innodb_checksum_algorithm=crc32
        ...
        [Note] [MY-011825] [Xtrabackup] completed OK!
        ```

    The backup service performs two operations:
    
    * `xtrabackup --backup`: Creates a physical copy of the database files
    * `xtrabackup --prepare`: Applies transaction logs to make the backup consistent

## Step 5: Validate the backup

Before relying on a backup for disaster recovery, verify that it is functional. The validation service launches an independent, temporary Percona Server instance that boots directly from the backup files.

!!! note "Why validate?"

    A backup that has not been tested for recovery provides no guarantee of data protection. Validation proves that backup files are functional before you need them in an emergency.

Do the following to validate the backup:
{.power-number}

1. Start the validation container:

    ```shell
    docker compose up -d pxb-validate
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        [+] Running 1/1
         ✔ Container pxb_validate  Started
        ```

2. Check the container logs to ensure it initializes properly:

    ```shell
    docker compose logs pxb-validate
    ```

    Look for `ready for connections` in the output.

    ??? example "Expected output"

        ```{.text .no-copy}
        pxb_validate  | [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.4.2-2) starting as process 7
        ...
        pxb_validate  | [System] [MY-011323] [Server] X Plugin ready for connections.
        pxb_validate  | [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections.
        ```

3. Connect to the validation instance on port `3307` and verify your data:

    ```shell
    docker exec -it pxb_validate mysql -uroot -p -e "SELECT * FROM mydb.employees;"
    ```

    Enter the password (`YourSecurePassword123`) when prompted.

    ??? example "Expected output"

        ```{.text .no-copy}
        Enter password:
        +----+--------------------+---------------------+---------+
        | id | name               | email               | country |
        +----+--------------------+---------------------+---------+
        |  1 | Erasmus Richardson | erasmus@example.com | England |
        |  2 | Jenna French       | jenna@example.com   | Canada  |
        |  3 | Alfred Dejesus     | alfred@example.com  | Austria |
        +----+--------------------+---------------------+---------+
        ```

4. Stop the validation container when finished:

    ```shell
    docker compose stop pxb-validate
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        [+] Stopping 1/1
         ✔ Container pxb_validate  Stopped
        ```

## Step 6: Simulate a disaster

To practice restoration, simulate total data loss by stopping the primary database and wiping its data volume.

!!! warning

    This step intentionally destroys all data in the primary database. In a real environment, you would only do this if data corruption or loss has already occurred.

Do the following to simulate a disaster:
{.power-number}

1. Stop the primary database container:

    ```shell
    docker compose stop psmysql
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        [+] Stopping 1/1
         ✔ Container psmysql  Stopped
        ```

2. Wipe the production data directory (simulating drive failure or data corruption):

    ```shell
    docker compose run --rm --user root psmysql bash -c "rm -rf /var/lib/mysql/*"
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        [+] Creating 1/0
         ✔ Container pxb-tutorial-psmysql-run-xxxxx  Created
        [+] Running 1/0
         ✔ Container pxb-tutorial-psmysql-run-xxxxx  Started
        ```

        The command output shows a temporary container being created and run. After execution, no additional output appears because the `rm` command produces no output on success.

3. Verify the database cannot start (optional):

    If you attempt to start the database now, it will fail because its data files are missing:

    ```shell
    docker compose start psmysql
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        [+] Running 1/1
         ✔ Container psmysql  Started
        ```

    ```shell
    docker compose logs psmysql
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        psmysql  | [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.4.2-2) starting as process 1
        psmysql  | [System] [MY-013576] [InnoDB] InnoDB initialization has started.
        psmysql  | [ERROR] [MY-012224] [InnoDB] Tablespace open failed for '"./ibdata1"'
        psmysql  | [ERROR] [MY-012930] [InnoDB] Plugin initialization aborted with error: Generic error.
        psmysql  | [ERROR] [MY-010334] [Server] Failed to initialize DD Storage Engine
        psmysql  | [ERROR] [MY-010020] [Server] Data Dictionary initialization failed.
        psmysql  | [ERROR] [MY-010119] [Server] Aborting
        psmysql  | [System] [MY-010910] [Server] /usr/sbin/mysqld: Shutdown complete (mysqld 8.4.2-2)
        ```

    The logs show that MySQL cannot find its system tablespace (`ibdata1`) and fails to start.

## Step 7: Execute the restore

Run the restore service to copy the backup files back to the primary database volume and fix file permissions.
{.power-number}

1. Stop the primary database if the container is running:

    ```shell
    docker compose stop psmysql
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        [+] Stopping 1/1
         ✔ Container psmysql  Stopped
        ```

2. Run the restore task:

    ```shell
    docker compose run --rm pxb-restore
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        ==> Clearing current database directory...
        ==> Restoring physical data files from backupvol...
        xtrabackup version 8.4.0-2 based on MySQL server 8.4.2 Linux (x86_64)
        ...
        [Note] [MY-011825] [Xtrabackup] completed OK!
        ==> Fixing file permissions for Percona Server...
        ```

    The restore service performs three operations:
    
    * Clears any residual files from the data directory
    * Runs `xtrabackup --copy-back` to restore backup files
    * Runs `chown -R mysql:mysql` to fix file ownership

## Step 8: Verify the restoration

Start the primary database and confirm that your data has been recovered.
{.power-number}

1. Start the primary database:

    ```shell
    docker compose start psmysql
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        [+] Running 1/1
         ✔ Container psmysql  Started
        ```

2. Check the logs to ensure it starts successfully:

    ```shell
    docker compose logs psmysql
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        psmysql  | [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.4.2-2) starting as process 1
        psmysql  | [System] [MY-013576] [InnoDB] InnoDB initialization has started.
        psmysql  | [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
        psmysql  | [System] [MY-011323] [Server] X Plugin ready for connections. Bind-address: '::' port: 33060
        psmysql  | [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.4.2-2'  socket: '/var/lib/mysql/mysql.sock'  port: 3306  Percona Server (GPL), Release 2, Revision b575402d.
        ```

    Look for `ready for connections` in the output to confirm the server started successfully.

3. Connect and verify your data is restored:

    ```shell
    docker exec -it psmysql mysql -uroot -p -e "SELECT * FROM mydb.employees;"
    ```

    Enter the password (`YourSecurePassword123`) when prompted.

    ??? example "Expected output"

        ```{.text .no-copy}
        Enter password:
        +----+--------------------+---------------------+---------+
        | id | name               | email               | country |
        +----+--------------------+---------------------+---------+
        |  1 | Erasmus Richardson | erasmus@example.com | England |
        |  2 | Jenna French       | jenna@example.com   | Canada  |
        |  3 | Alfred Dejesus     | alfred@example.com  | Austria |
        +----+--------------------+---------------------+---------+
        ```

Your database has been fully restored from the backup.

## Understanding file permissions

One of the most common issues when restoring backups in Docker environments is file permission errors. The following table explains why the `chown` command is critical:

| Stage | File Owner | Explanation |
|-------|------------|-------------|
| After backup | `mysql` | Backup preserves original ownership |
| After `--copy-back` | `root` | Files are copied by root user in the restore container |
| After `chown` | `mysql` | Ownership restored; MySQL can start |

If you skip the `chown -R mysql:mysql /var/lib/mysql` step, MySQL fails to start with permission errors similar to:

```{.text .no-copy}
[ERROR] [MY-010187] [Server] Could not open file '/var/lib/mysql/ibdata1' for reading: Permission denied
```

## Clean up

To remove all containers, volumes, and resources created by this tutorial:
{.power-number}

1. Remove Docker containers and volumes:

    ```shell
    docker compose down -v
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        [+] Running 5/5
         ✔ Container pxb_validate  Removed
         ✔ Container psmysql       Removed
         ✔ Volume pxb-tutorial_mysql_data  Removed
         ✔ Volume pxb-tutorial_backupvol   Removed
         ✔ Network pxb-tutorial_default    Removed
        ```

2. Remove the secrets directory:

    ```shell
    rm -rf secrets/
    ```

    If the command executes successfully, the expected output is empty.

3. Optionally, remove the project directory:

    ```shell
    cd .. && rm -rf pxb-tutorial/
    ```

    If the command executes successfully, the expected output is empty.

## Key takeaways

* **Separation of concerns**: Using Docker Compose profiles separates backup, validation, and restore into distinct operations, making each step explicit and auditable.

* **Validation before restore**: Always validate backups by booting a temporary database instance from the backup files before relying on them for disaster recovery.

* **The permission gotcha**: Physical backups restored by the `root` user must have ownership changed to `mysql:mysql` before the database can start. This is a common source of restore failures.

* **Prepared backups**: Backups must be prepared with `xtrabackup --prepare` before they can be restored or used for validation.

## Next steps

* Learn about [incremental backups](create-incremental-backup.md) to reduce backup time and storage
* Explore [streaming backups](take-streaming-backup.md) for direct-to-cloud storage
* Review [backup encryption](encrypt-backups.md) for securing backup data
