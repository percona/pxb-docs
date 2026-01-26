# Restore full, incremental, and compressed backups

!!! warning
   
    Backup needs to be prepared before it can be restored.

The restore backup procedure is the same for full, incremental, and compressed backups.

Ensure you have one of the following before proceeding:

* Root access

* `sudo` access — administrator privileges are required to restore files, change ownership, and manage the database service.

For convenience, *xtrabackup* binary has the `--copy-back` option to copy the backup to the datadir of the server:

```bash
xtrabackup --copy-back --target-dir=/data/backups/
```

If you don’t want to save your backup, you can use the `--move-back` option which will move the backed up data to the datadir.

If you don’t want to use `--copy-back` and `--move-back` options, you can also use **rsync** or **cp** to restore the files.

!!! note
   
    The datadir must be empty before restoring the backup. Also, it’s important to note that MySQL server needs to be shut down before restore is performed. You cannot restore to a datadir of a running mysqld instance (except when importing a partial backup).

An example of the **rsync** command to restore the backup:

```bash
rsync -avrP /data/backup/ /var/lib/mysql/
```

You should check that the restored files have the correct ownership and permissions.

As files’ attributes are preserved, in most cases you must change the files’ ownership to `mysql` before starting the database server, as the files are owned by the user who created the backup:

```bash
chown -R mysql:mysql /var/lib/mysql
```

## Prepare grastate.dat for Galera cluster (Optional)

When restoring a backup of a Percona XtraDB Cluster, be sure the `grastate.dat` file is present and correctly populated before you start the node.
The example demonstrates how to restore a backup on a single node and then bootstrap a new Percona XtraDB Cluster. Once the first node is up, additional nodes can join later via IST (Incremental State Transfer) or SST (State Snapshot Transfer).

This `grastate.dat` file contains the following information:

* `UUID` - identifies the specific Galera cluster the node last belonged to.

* `seqno` - indicates the global transaction number of the last committed write-set on that node.

* `safe_to_bootstrap` flag - indicates whether the node was the last to shut down gracefully. A value of `1` means the node was the last to shut down gracefully and it is safe to use this node to bootstrap a new cluster. A value of `0` means the node was not the last to shut down gracefully and it should not be used to start the cluster.

After preparing and restoring the backup, do the following steps:

1. Extract the Galera state information from the backup metadata file located in the restored datadir (for example, `/var/lib/mysql`). The extracted information is represented in the `uuid:seqno` format.

    ```bash
    cat /var/lib/mysql/xtrabackup_galera_info
    ```

    ??? example "Expected output"

        ```text
        3f9d1c8e-4a12-11ee-bc3c-8c8590c4abcd:145672
        ```

2. Create or update the `grastate.dat` file in the datadir using the extracted `UUID` and `seqno`. In this example, the node is used to bootstrap a new cluster, so `safe_to_bootstrap` is set to `1`.

    !!! note
    
        Set `safe_to_bootstrap` to `1` only on the node that will be used to bootstrap a new cluster. All other nodes must have `safe_to_bootstrap` set to `0`.


    **Bootstrap node (`safe_to_bootstrap: 1`):**

    ```bash
    cat > /var/lib/mysql/grastate.dat <<EOF
    # GALERA saved state
    version: 2.1
    uuid: 3f9d1c8e-4a12-11ee-bc3c-8c8590c4abcd
    seqno: 145672
    safe_to_bootstrap: 1
    EOF
    ```

    **All other nodes (`safe_to_bootstrap: 0`):**
    
    ```bash
    cat > /var/lib/mysql/grastate.dat <<EOF
    # GALERA saved state
    version: 2.1
    uuid: 3f9d1c8e-4a12-11ee-bc3c-8c8590c4abcd
    seqno: 145672
    safe_to_bootstrap: 0
    EOF
    ```

3. Ensure the file has the correct ownership:

    ```bash
    chown mysql:mysql /var/lib/mysql/grastate.dat
    ```

If `grastate.dat` is missing or contains incorrect values, the node may fail to start or attempt an unsafe cluster bootstrap.

Data is now restored, and you can start the server.
