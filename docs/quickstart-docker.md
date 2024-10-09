# Start a Docker container and take a backup

Percona XtraBackup works in combination with a MySQL-compatible database, Percona Server for MySQL, in our scenario. To use Percona XtraBackup, run it in a separate Docker container and then connect the Percona XtraBackup container to the Percona Server for MySQL container. As soon as you [start Percona Server for MySQL in a Docker container](https://docs.percona.com/percona-server/8.4/quickstart-docker.html) and [create a database and table in Percona Server for MySQL](https://docs.percona.com/percona-server/8.4/quickstart-docker.html#create-a-database), you are ready to backup your databes with Percona XtraBackup.

The following steps create a Docker volume, start Percona XtraBackup in a Docker continer, take and prepare a backup of Percona Server for MySQL database.
{.power-number}

## Create a Docker volume

The benefits of using a Docker volume are the following:

* You can keep your data safe and accessible across different containers. For example, if you want to upgrade your database image to a newer version, you can stop the old container and start a new one with the same volume attached without losing any data. 

* You can quickly backup and restore your data using the `docker cp` command or mount the volume to another container.

```{.bash data-prompt="$"}
$ docker volume create backupvol
```
    
??? example "Expected output"

    ```{.text .no-copy}
     backupvol
    ```

## Start Percona XtraBackup 8.4 in a container, take and prepare a backup

The `docker run` command creates and runs a new container from an image. The command modifies the container's behavior with options.

In our example, the command has the following options:

| Option | Description |
|---|---|
| `--name`  |  Provides a name to the container. If you do not use this option, Docker adds a random name.  |
| `--volumes-from` | Refers to Percona Server for MySQL and indicates that you intend to use the same data as the `psmysql` container.|
| `it` | Interacts with the container and be a pseudo-terminal. |
| `--user root` | Sets the user to root inside the Percona XtraBackup container. This option is required to access the MySQL data directory and run the xtrabackup command. |
|`backup_84` |Indicates the directory inside the container where the backup files are stored. |
| `-v` | Mounts a volume from the host machine to volumes in another container that is being run. In our example, the `-v` option mounts a volume from the `psmysql` container to the `backupvol` volume on the host machine.|
| `backupvol` | Indicates the persistent storage for the database. |
| `psmysql`    | Indicates the Percona Server for MySQL container.  |
|`--password`   | Prompts the user to enter the password for the root user. For convenience you can add the password for the root user to this option, for example, `--password=secret`. Then the password will be passed automaticaly when running the command. Note that if you specify the password with `--password=secret`, the password is visible in `docker ps`, `docker ps -a` (docker history) and regular ps command.          |
| `8.4` | Use this tag to specify a specific version. Avoid using the `latest` tag. <br> In our example, we use the `8.4` tag. In Docker, a tag is a label assigned to an image and is used to maintain different versions of an image.|

If you do not add a tag, Docker uses `latest` as the default tag and downloads the newest image from [percona/percona-xtrabackup on the Docker Hub](https://hub.docker.com/r/percona/percona-xtrabackup). This image can be in a different series or version from what you expect since the latest image changes over time. If you are using Percona XtraBackup version prior to 8.4, use tags to ensure that you use [compatible versions](server-backup-version-comparison.md) of Percona Server for MySQL and Percona XtraBackup. 

The CPU architecture or platform for Percona Server for MySQL and Percona XtraBackup should be the same. If you want to use a different platform, you can add the following command:

| Platform                 | Description                                                 |
|--------------------------|-------------------------------------------------------------|
| --platform linux/amd64    | To run an AMD64 platform on an ARM64 computer.              |
| --platform linux/arm64    | To run an ARM64 platform on an AMD64 computer.              |

You can run the Docker ARM64 version of Percona XtraBackup. Use the `8.4-aarch64` tag instead of `8.4`.

### Connect the Percona XtraBackup container to the Percona Server container

We recommend using the `–-user root` option in the Docker command.
Run a Docker container example

```{.bash data-prompt="$"}
$ docker run --name pxb --volumes-from psmysql -v backupvol:/backup_84 -it --user root percona/percona-xtrabackup:8.4 /bin/bash -c "xtrabackup --backup --datadir=/var/lib/mysql/ --target-dir=/backup_84 --user=root --password; xtrabackup --prepare --target-dir=/backup_84"
```

You are prompted to enter the password. In our example, the password is `secret`.

```{.text .no-copy}
2024-10-07T13:55:47.640100-00:00 0 [Note] [MY-011825] [Xtrabackup] recognized server arguments: --datadir=/var/lib/mysql/
2024-10-07T13:55:47.641887-00:00 0 [Note] [MY-011825] [Xtrabackup] recognized client arguments: --backup=1 --target-dir=/backup_84 --user=root --password
Enter password:
```
    
In this example of expected output, we provide the first and last section of the backup log and use ellipses instead of the entire backup log.

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

The command runs a Docker container `pxb` from the `percona/percona-xtrabackup:8.4` image and mounts two volumes: one from another container named `psmysql`, which contains Percona Server data directory, and another named `backupvol`, which is where the backup files are stored. The command also sets the user to root and prompts the user to enter the password. 

The command then executes two steps: 
    
* Runs `xtrabackup` with the `--backup` option to copy the data files from `/var/lib/mysql/` to `/backup_8034`
    
* Runs `xtrabackup` with the `--prepare` option to apply the log files and make the backup consistent and ready for restore

You can check the Xtrabackup logs with the `docker container logs <container-name>` command.

For example:

```{.bash data-prompt="$"}
$ docker container logs pxb
```

## Next steps

[Restore the backup :material-arrow-right:](quickstart-restore-backup.md){.md-button}

