# Run in a Docker container

Docker allows you to run Percona XtraBackup and Percona Server for MySQL in separate containers, keeping your host system clean and organized. Each container is fully equipped with everything needed to run the application, creating an isolated environment for Percona XtraBackup without requiring direct installation. By managing your database server and backups in separate containers, you can maintain a tidy separation of services, enhancing your workflow and efficiency.

When we say "container" here, we mean the Docker container itself.
The "instance" refers specifically to the database server running inside that container.

Percona maintains an official Docker image on [Docker
Hub](https://hub.docker.com/r/percona/percona-xtrabackup/), making it easy to get started. You have two options for the image version:

* Use the `latest` tag to get the most recent release

* Pick a specific version through the Docker tag filter

A critical first step: ensure you have the current version of Docker installed. The package manager versions (APT, YUM) often lag behind and can cause issues. Instead, follow Docker's official installation guide to get the most recent release.

--8<--- "get-help-snip.md"

## Install the Docker Engine

You need Docker to run Percona XtraBackup in a container. The instructions are subject to change, so always refer to the [Docker documentation](https://docs.docker.com/get-docker/) for the most up-to-date information.

=== "Debian/Ubuntu"

    1. Remove any existing Docker version to prevent conflicts:
        
        ```bash
        $ sudo apt-get remove docker docker-engine docker.io containerd runc
        ```
        
    2. Update package lists:
        
        ```bash
        $ sudo apt-get update
        ```
        
    3. Install prerequisites to allow the use of repositories over HTTPS:
        
        ```bash
        $ sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release
        ```
        
    4. Add Docker's official GPG key:
        
        ```bash  
        $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
        ```
        
    5. Set up the Docker repository:
        
        ```bash
        $ echo \
          "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
          $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        ```
        
    6. Install the Docker Engine:
        
        ```bash
        $ sudo apt-get update
        $ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        ```
        
    7. Verify the installation:
        
        ```bash  
        $ sudo docker --version
        ```

=== "Red Hat Enterprise Linux (RHEL) 7 or below"

    1. Remove any existing Docker version to prevent conflicts:
        
        ```bash
        $ sudo yum remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine
        ```
    
    2. Install the required packages:
        
        ```bash
        $ sudo yum install -y yum-utils
        ```
    
    3. Set up the Docker repository:
        
        ```bash
        $ sudo yum-config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
        ```
    
    4. Install the Docker Engine:
        
        ```bash
        $ sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        ```
    
    5. Start the Docker service:
        
        ```bash
        $ sudo systemctl start docker
        ```
    
    6. Verify the installation:
        
        ```bash  
        $ sudo docker --version
        ```

=== "Red Hat Enterprise Linux (RHEL) 8+"

    1. Remove any existing Docker version to prevent conflicts:
        
        ```bash
        $ sudo dnf remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine
        ```
    
    2. Install the required packages:
        
        ```bash
        $ sudo dnf install dnf-plugins-core
        ```
    
    3. Set up the Docker repository:
        
        ```bash
        $ sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
        ```
    
    4. Install the Docker Engine:
        
        ```bash
        $ sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        ```
    
    5. Start the Docker service:
        
        ```bash
        $ sudo systemctl enable --now docker
        ```
    
    6. Verify the installation:
        
        ```bash  
        $ sudo docker --version
        ```

## Docker images

Docker images are pre-packaged software that contains everything needed to run an application. They include the application code, runtime, libraries, environment variables, and configuration files. You can download images from Docker Hub, a public repository of Docker images.

1. Go to Docker Hub at https://hub.docker.com
2. Type "percona xtrabackup" in the search bar
3. Look for the official Percona repository (`percona/percona-xtrabackup`)

The repository name shows as `percona/percona-xtrabackup` where:

| Name                | Description                      |
|---------------------|--------------------------------|
| percona            | Organization name              |
| percona-xtrabackup | Specific image name            |

### Image tags

Each Docker image has tags that tell you its version. For Percona XtraBackup, you'll see tags like:
```bash
percona/percona-xtrabackup:8.0
percona/percona-xtrabackup:8.0.35
percona/percona-xtrabackup:latest
```

- `8.0` tracks the latest 8.0 release
- `8.0.35` points to that specific version
- `latest` always gets you the newest version

### Pull images

To download an image, use `docker pull`. Here's how:

```bash
# Pull the latest version
docker pull percona/percona-xtrabackup:latest

# Pull a specific version
docker pull percona/percona-xtrabackup:8.0.35
```

### What's in a Percona XtraBackup image

A Percona XtraBackup image contains:
- The XtraBackup backup tool
- Required system libraries
- Configuration files
- Runtime dependencies

Think of it as a pre-packed toolkit with everything XtraBackup needs to run.

### Check images

See what images you've downloaded:
```bash
# List all images
docker images

# Look for specific Percona images
docker images | grep percona
```

### Use an image

Run a basic test to make sure your image works:
```bash
docker run --rm percona/percona-xtrabackup:latest xtrabackup --version
```

This command shows the XtraBackup version and confirms your setup works.



## 1. Run Percona Server for MySQL container

Percona XtraBackup works in combination with a MySQL-compatible database, Percona Server for MySQL, in our example. To take a backup of Percona Server for MySQL, run Percona Server for MySQL in a Docker container and create a database with data. Read the instructions on how to [Run Percona Server for MySQL in a Docker Container](https://docs.percona.com/percona-server/8.0/docker.html).

As soon as Percona Server for MySQL runs and the database contains data, you are ready to connect the Percona XtraBackup container to the Percona Server for MySQL container and take a backup.

## 2. Create a container and connect to Percona Server for MySQL container

You have two options to create a Docker container from a Percona XtraBackup image:

* `docker create`: Makes a container ready to start later

* `docker run`: Creates and starts the container immediately

When you first create a container, Docker downloads the Percona XtraBackup 8.0 image from Docker Hub. For future containers, Docker uses your local copy.

### Important security note

When connecting your XtraBackup container to a MySQL server container, always use the `--user=root` option in your Docker command. This ensures proper backup permissions.

### Container creation

Here's how to create a basic backup container:

```bash
# Create a container for backing up MySQL data
docker create \
    --name percona-xtrabackup \
    --volumes-from percona-server-mysql:8.0 \
    percona/percona-xtrabackup:8.0 \
    xtrabackup --backup \
    --datadir=/var/lib/mysql/ \
    --target-dir=/backup \
    --user=root \
    --password=root
```

This command does the following:

* `--name percona-xtrabackup`: Names your container for easy reference

* `--volumes-from percona-server-mysql:8.0`: Connects to your MySQL container's data

* `percona/percona-xtrabackup:8.0`: Uses the Percona XtraBackup 8.0 image

* The remaining options configure the backup:

  * `--backup`: Tells XtraBackup to perform a backup
  
  * `--datadir`: Points to MySQL's data directory
  
  * `--target-dir`: Sets where the backup will be stored
  
  * `--user` and `--password`: MySQL connection credentials

### Next steps

After creating your container, you can:

* Start the container with `docker start percona-xtrabackup`

* Check its status with `docker ps -a`

* View logs with `docker logs percona-xtrabackup`

### Common issues

If you see permission errors:

* Double-check your MySQL user credentials

* Verify the `--volumes-from` connection

* Ensure your target directory is writable

### Remove the container

Need to make changes? You can remove the container and create a new one:

```bash
docker rm percona-xtrabackup
# Then run the create command again with your changes
```

### Percona XtraBackup ARM64

Starting with Percona XtraBackup 8.0.35-31, you can run the Docker ARM64 version of Percona XtraBackup. You can find the version and architecture on [Docker Hub Percona/Percona-Server Tags](https://registry.hub.docker.com/r/percona/percona-xtrabackup/tags?page=1&name=8.0). The Docker images for ARM64 version contain `aarch64` in the tag name, for example, `8.0.35-aarch64`.

We recommend that the architectures match. If the server is ARM64, you should also use Percona XtraBackup in ARM64.

### Start the Percona XtraBackup container

Start the Percona XtraBackup container with exactly the same parameters that were used when the container was created. The following command starts the percona-xtrabackup Docker container, attaches to its output, and keeps STDIN open for interactive input. This is useful if you want to monitor the container's logs and interact with it directly.

```{.bash data-prompt="$"}
$ sudo docker start -ai percona-xtrabackup
```

The command sudo docker start -ai percona-xtrabackup does the following:

* `sudo`: Runs the command with superuser (administrator) privileges.

* `docker`: Refers to the Docker command-line interface.

* `start`: Starts a stopped Docker container.

* `-a`: Attaches to the container's output, so you can see the logs and interact with the container in real time.

* `-i`: Keeps the container's STDIN open, allowing you to provide input to the container.

* `percona-xtrabackup`: Specifies the name of the Docker container you want to start.

### Take a backup

This command creates and starts a new Docker container named `percona-xtrabackup`, mounts the volumes from the existing `percona-server-mysql:8.0` container, and performs a backup of the MySQL data using `xtrabackup`. The backup is stored in the `/backup` directory inside the new container..

```{.bash data-prompt="$"}
$ sudo docker run --name percona-xtrabackup --volumes-from percona-server-mysql:8.0 \
percona/percona-xtrabackup:8.0
xtrabackup --backup --datadir=/var/lib/mysql --target-dir=/backup --user=root --password=root
```

* `sudo`: Runs the command with superuser (administrator) privileges.

* `docker run`: Creates and starts a new Docker container.

* `--name percona-xtrabackup`: Names the new container percona-xtrabackup.

* `--volumes-from percona-server-mysql:8.0`: Mounts volumes from the existing container percona-server-mysql:8.0 into the new container. This allows the new container to access the data and directories of the existing container.

* `percona/percona-xtrabackup:8.0`: Specifies the Docker image to use for creating the container. In this case, it's the percona/percona-xtrabackup:8.0 image.

* `xtrabackup --backup --datadir=/var/lib/mysql --target-dir=/backup --user=root --password=root`: Executes the xtrabackup command within the container to perform a backup. The options provided to the xtrabackup command are:

  * `--backup`: Tells xtrabackup to perform a backup.

  * `--datadir=/var/lib/mysql`: Specifies the data directory of the MySQL server.

  * `--target-dir=/backup`: Specifies the directory where the backup will be stored.

  * `--user=root`: Uses the root user to perform the backup.

  * `--password=root`: Uses the root password for authentication.



## Restore a backup

To restore a backup in Docker, you need to create a new container from the Percona XtraBackup image and use the `xtrabackup` command to restore the backup data to the MySQL data directory. The following steps outline the process of restoring a backup in Docker:

1. Create a Docker volume for the restored data.

    ```bash
    docker volume create restorevol
    ```

2. Run a new Percona Server for MySQL container to restore the backup data:

    ```bash
    docker run -d -p 3307:3306 --name psmysql2 -e MYSQL_ROOT_PASSWORD=secret -v restorevol:/var/lib/mysql percona/percona-server:8.0.34
    ```

3. Stop the new Percona Server for MySQL container:

    ```bash
    docker stop psmysql2
    ```

4. Remove all files in the new volume to prepare for restoration:
  
    ```bash
    docker run --rm --volumes-from psmysql2 -it --user root percona/percona-xtrabackup:8.0.34 /bin/bash -c "rm -rf /var/lib/mysql/*"
    ```
  
5. Restore the backup data to the new volume:

    ```bash
    docker run --rm --volumes-from psmysql2 -it --user root -v restorevol:/backup percona/percona-xtrabackup:8.0.34 xtrabackup --copy-back --target-dir=/backup
    ```
  
6. Change the ownership of the restored data:

    ```bash
    docker run --rm --volumes-from psmysql2 -it --user root percona/percona-xtrabackup:8.0.34 chown -R mysql:mysql /var/lib/mysql
    ```

7. Start the new Percona Server for MySQL container:

    ```bash
    docker start psmysql2
    ```

### Troubleshoot issues with creating the container or during the backup

If you encounter issues when creating the container or during the backup process, consider the following troubleshooting steps:

* Check Docker daemon: Ensure the Docker daemon runs and is properly configured.

* Verify Docker image

    * Confirm you use the correct Docker image.

    * Check available images with the `docker images` command.

* Inspect container logs

    * View logs using the `docker logs <container_name>` command.

    * Identify any errors or warnings.

* Check volume permissions

    * Ensure the volumes have the correct permissions.

    * Verify that the container can access the volumes.

* Review configuration files: Double-check the configuration files for syntax errors or misconfigurations.

* Resource allocation

    * Ensure the host system has sufficient resources (CPU, memory, disk space).

    * Monitor resource usage during the backup process.

* Network issues

    * Verify there are no network connectivity issues between the Docker containers.

    * Check firewall settings and network configurations.

* Compatibility: Ensure the versions of Percona Server and Percona XtraBackup are compatible.

* Error messages

    * Look for specific error messages in the logs.

    * Search for solutions online or in the Percona documentation.




## For more information

Review the [Docker Docs](https://docs.docker.com/)
