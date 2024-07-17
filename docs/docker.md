# Run Percona XtraBackup 8.0 in a Docker container

Docker containers are built from Docker images, which are snapshots of the configuration needed to run an applications, such as the code, and libraries. With Docker, you can build, deploy, run, update, and manage containers, which isolate applications from the host system. A Docker container lets you work with Percona XtraBackup without installing the product on a local drive. You may run Percona Server for MySQL in one container and Percona XtraBackup in another.

For this document, container refers to the Docker container and instance refers to the database server in the container.

Percona XtraBackup has an official Docker image hosted on [Docker Hub](https://hub.docker.com/r/percona/percona-xtrabackup/). If you want the latest version, use the `latest` tag. You can reference a specific version using the [Docker tag filter for the 8.0 versions](https://registry.hub.docker.com/r/percona/percona-xtrabackup/tags?page=1&name=8.0).

Make sure that you are using the latest version of Docker. The `APT` and `YUM` versions may be outdated and cause errors. Use the [installation instructions](https://docs.docker.com/engine/install/) to install Docker on your system.

## 1. Run Percona Server for MySQL container

Percona XtraBackup works in combination with a MySQL-compatible database, Percona Server for MySQL, in our example. To take a backup of Percona Server for MySQL, run Percona Server for MySQL in a Docker container and create a database with data. Read the instructions on how to [Run Percona Server for MySQL in a Docker Container](https://docs.percona.com/percona-server/8.0/docker.html).

As soon as Percona Server for MySQL runs and the database contains data, you are ready to connect the Percona XtraBackup container to the Percona Server for MySQL container and take a backup.

## 2. Create Percona XtraBackup Docker container and connect to Percona Server for MySQL container

You can create a Docker container based on Percona XtraBackup image with
either `docker create` or the `docker run` command. `docker create`
creates a Docker container and makes it available for starting later.

Docker downloads the Percona XtraBackup 8.0 image from the Docker Hub. If it
is not the first time you use the selected image, Docker uses the image
available locally.

!!! important
   
    When running Percona XtraBackup from a container and connecting to a 
    MySQLserver container, we recommend using the --user=root option in the 
    Docker command.

```{.bash data-prompt="$"}
$ sudo docker create --name percona-xtrabackup --volumes-from percona-server-mysql:8.0 \
percona/percona-xtrabackup:8.0  \
xtrabackup --backup --datadir=/var/lib/mysql/ --target-dir=/backup \
--user=root --password=root
```

With parameter name you give a meaningful name to your new Docker container
so that you could easily locate it among your other containers.

The `volumes-from` flag refers to Percona Server for MySQL and indicates
that you intend to use the same data as the Percona Server for MySQL container.

### Percona XtraBackup ARM64

Starting with Percona XtraBackup 8.0.35-31, you can run the Docker ARM64 version of Percona XtraBackup. You can find the version and architecture on [Docker Hub Percona/Percona-Server Tags](https://registry.hub.docker.com/r/percona/percona-xtrabackup/tags?page=1&name=8.0). The Docker images for ARM64 version contain `aarch64` in the tag name, for example, `8.0.35-aarch64`.

We recommend that the architectures match. If the server is ARM64, you should also use Percona XtraBackup in ARM64.

### Start the Percona XtraBackup container

Start the Percona XtraBackup container with exactly the same parameters that were used when the container was created:

```{.bash data-prompt="$"}
$ sudo docker start -ai percona-xtrabackup
```

This command starts the `percona-xtrabackup` container, attaches to its
input/output streams, and opens an interactive shell.

### Docker run command

The `docker run` command is a shortcut command that creates a Docker container and
then immediately runs it.

```{.bash data-prompt="$"}
$ sudo docker run --name percona-xtrabackup --volumes-from percona-server-mysql:8.0 \
percona/percona-xtrabackup:8.0
xtrabackup --backup --datadir=/var/lib/mysql --target-dir=/backup --user=root --password=root
```

## For more information

Review the [Docker Docs](https://docs.docker.com/)
