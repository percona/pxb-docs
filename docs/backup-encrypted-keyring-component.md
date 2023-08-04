# Back up an InnoDB tablespace encrypted with the keyring component

Percona XtraBackup has has no special requirements for backing up a database with InnoDB tablespaces encrypted by a keyring component.

```{.bash data-prompt="$"}
$ xtrabackup --backup --target-dir=/data/backup --user=root
```

After *xtrabackup* completes the action, the following message confirms
the action:

??? example "Confirmation message"

    ```{.text .no-copy}
    xtrabackup: Transaction log of lsn (5696709) to (5696718) was copied.
    160401 10:25:51 completed OK!
    ```

## Prepare the backup with the keyring component

The xtrabackup reads the `component_keyring_file.cnf` to find the path to the `component_keyring_file`. The component configuration requires a `path` attribute that provides the absolute path and name of the file used to store the keys. If needed, you can assign another configuration file by passing the `--component-keyring-file-config` option. 

The example passes the location for the `component_keyring_file.cnf`:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --target-dir=/data/backup \
--component-keyring-config=/usr/lib64/mysql/plugin/component_keyring_file.cnf
```

The message confirms the success of the operation:

??? example "Confirmation message"

    ```{.text .no-copy}
    InnoDB: Shutdown completed; log sequence number 5697064
    160401 10:34:28 completed OK!
    ```

## Restore an InnoDB tablespace encrypted with the keyring component

To restore the backup use the `--copy-back` option.

If the keyring has been rotated, you must restore the specific keyring used
to take and prepare the backup.
