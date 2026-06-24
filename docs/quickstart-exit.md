# Clean up quickstart resources

This tutorial describes how to remove the Docker containers, images, and volumes created during the quickstart.

## Resources to remove

The following table lists all resources created during the quickstart tutorials:

| Resource | Type | Created in |
|----------|------|------------|
| `psmysql` | Container | [Percona Server quickstart :octicons-link-external-16:](https://docs.percona.com/percona-server/{{vers}}/quickstart-docker.html) |
| `ps-restore-target` | Container | [Restore the backup](quickstart-restore-back.md) |
| `pxb` | Container | [Take a backup with Docker](quickstart-docker.md) |
| `backupvol` | Volume | [Take a backup with Docker](quickstart-docker.md) |
| `restore_data` | Volume | [Restore the backup](quickstart-restore-back.md) |

## Step 1: Exit the MySQL client

If the MySQL client session remains open, exit the session before removing containers.
{.power-number}

1. Exit the MySQL command client:

    ```sql
    exit
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Bye
        ```

    Alternative commands: `\q` or `quit`

## Step 2: Remove Docker containers

Remove the containers created during the quickstart. The `-f` option forces removal of running containers.
{.power-number}

1. Remove the restore target container:

    ```shell
    docker container rm ps-restore-target -f
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        ps-restore-target
        ```

2. Remove the Percona Server container:

    ```shell
    docker container rm psmysql -f
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        psmysql
        ```

3. Remove the Percona XtraBackup container:

    ```shell
    docker container rm pxb -f
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        pxb
        ```

## Step 3: Remove Docker images (optional)

Remove the Docker images to free disk space. Skip this step to retain images for future use.
{.power-number}

1. Remove the Percona Server image:

    ```shell
    docker image rmi percona/percona-server:8.4
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Untagged: percona/percona-server:8.4
        Untagged: percona/percona-server@sha256:...
        Deleted: sha256:...
        ```

2. Remove the Percona XtraBackup image:

    ```shell
    docker image rmi percona/percona-xtrabackup:8.4
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Untagged: percona/percona-xtrabackup:8.4
        Untagged: percona/percona-xtrabackup@sha256:...
        Deleted: sha256:...
        ```

## Step 4: Remove Docker volumes

Remove the volumes that stored database and backup data.

!!! warning "Permanent data loss"

    Removing volumes permanently deletes all stored data. Verify the data is no longer needed before proceeding.

{.power-number}

1. Remove the backup volume:

    ```shell
    docker volume rm backupvol
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        backupvol
        ```

2. Remove the restore target volume:

    ```shell
    docker volume rm restore_data
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        restore_data
        ```

## Verify resource removal

Confirm all quickstart resources have been removed with the following commands:

```shell
docker ps -a --filter "name=psmysql" --filter "name=ps-restore-target" --filter "name=pxb"
docker volume ls --filter "name=backupvol" --filter "name=restore_data"
```

??? example "Expected output"

    ```{.text .no-copy}
    CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

    DRIVER    VOLUME NAME
    ```

Empty results confirm resource removal completed.

## Summary

This tutorial covered the removal of the following quickstart resources:

* Three Docker containers: `psmysql`, `ps-restore-target`, `pxb`

* Two Docker images: `percona/percona-server:8.4`, `percona/percona-xtrabackup:8.4`

* Two Docker volumes: `backupvol`, `restore_data`

For information about running Percona XtraBackup in production environments, see [Installation](installation.md).

## Next step

[Explore next steps](quickstart-next-steps.md){.md-button}
