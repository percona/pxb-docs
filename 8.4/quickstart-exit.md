> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-xtrabackup/8.4/llms.txt).

# Clean up quickstart resources

This tutorial describes how to remove the Docker containers, images, and volumes created during the quickstart.

## Resources to remove

The following table lists all resources created during the quickstart tutorials:

| Resource            | Type      | Created in                                                                                          |
| ------------------- | --------- | --------------------------------------------------------------------------------------------------- |
| `psmysql`           | Container | [Percona Server quickstart](https://docs.percona.com/percona-server/8.4/quickstart-docker.html)     |
| `ps-restore-target` | Container | [Restore the backup](https://docs.percona.com/percona-xtrabackup/8.4/quickstart-restore-back.html)  |
| `pxb`               | Container | [Take a backup with Docker](https://docs.percona.com/percona-xtrabackup/8.4/quickstart-docker.html) |
| `backupvol`         | Volume    | [Take a backup with Docker](https://docs.percona.com/percona-xtrabackup/8.4/quickstart-docker.html) |
| `restore_data`      | Volume    | [Restore the backup](https://docs.percona.com/percona-xtrabackup/8.4/quickstart-restore-back.html)  |

## Step 1: Exit the MySQL client

If the MySQL client session remains open, exit the session before removing containers.

1. Exit the MySQL command client:

   ```
   exit
   ```

   Expected output

   ```
   Bye
   ```

   Alternative commands: `\q` or `quit`

## Step 2: Remove Docker containers

Remove the containers created during the quickstart. The `-f` option forces removal of running containers.

1. Remove the restore target container:

   ```
   docker container rm ps-restore-target -f
   ```

   Expected output

   ```
   ps-restore-target
   ```

1. Remove the Percona Server container:

   ```
   docker container rm psmysql -f
   ```

   Expected output

   ```
   psmysql
   ```

1. Remove the Percona XtraBackup container:

   ```
   docker container rm pxb -f
   ```

   Expected output

   ```
   pxb
   ```

## Step 3: Remove Docker images (optional)

Remove the Docker images to free disk space. Skip this step to retain images for future use.

1. Remove the Percona Server image:

   ```
   docker image rmi percona/percona-server:8.4
   ```

   Expected output

   ```
   Untagged: percona/percona-server:8.4
   Untagged: percona/percona-server@sha256:...
   Deleted: sha256:...
   ```

1. Remove the Percona XtraBackup image:

   ```
   docker image rmi percona/percona-xtrabackup:8.4
   ```

   Expected output

   ```
   Untagged: percona/percona-xtrabackup:8.4
   Untagged: percona/percona-xtrabackup@sha256:...
   Deleted: sha256:...
   ```

## Step 4: Remove Docker volumes

Permanent data loss

Removing volumes permanently deletes all stored data. Verify the data is no longer needed before proceeding.

Remove the volumes that stored database and backup data.

1. Remove the backup volume:

   ```
   docker volume rm backupvol
   ```

   Expected output

   ```
   backupvol
   ```

1. Remove the restore target volume:

   ```
   docker volume rm restore_data
   ```

   Expected output

   ```
   restore_data
   ```

## Verify resource removal

Confirm all quickstart resources have been removed with the following commands:

```
docker ps -a --filter "name=psmysql" --filter "name=ps-restore-target" --filter "name=pxb"
docker volume ls --filter "name=backupvol" --filter "name=restore_data"
```

Expected output

```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

DRIVER    VOLUME NAME
```

Empty results confirm resource removal completed.

## Summary

This tutorial covered the removal of the following quickstart resources:

- Three Docker containers: `psmysql`, `ps-restore-target`, `pxb`
- Two Docker images: `percona/percona-server:8.4`, `percona/percona-xtrabackup:8.4`
- Two Docker volumes: `backupvol`, `restore_data`

For information about running Percona XtraBackup in production environments, see [Installation](https://docs.percona.com/percona-xtrabackup/8.4/installation.html).

## Next step

[Explore next steps](https://docs.percona.com/percona-xtrabackup/8.4/quickstart-next-steps.html)
