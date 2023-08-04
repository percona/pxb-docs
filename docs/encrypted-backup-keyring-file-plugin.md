# Encrypted backup with the keyring_file plugin

In order to back up and prepare a database containing encrypted InnoDB  
tablespaces, specify the path to a keyring file as the value of the
`--keyring-file-data` option.


## Back up

```{.bash data-prompt="$"}
$ xtrabackup --backup --target-dir=/data/backup/ --user=root \
--keyring-file-data=/var/lib/mysql-keyring/keyring
```

The following message confirms the action:

??? example "Confirmation message"

    ```{.text .no-copy}
    xtrabackup: Transaction log of lsn (5696709) to (5696718) was copied.
    160401 10:25:51 completed OK!
    ```

## Prepare the backup

!!! warning

    The xtrabackup binary does not copy the keyring file into the backup directory. To prepare the backup, copy the keyring file manually.

To prepare the backup specify the keyring-file-data, use `--keyring_file_data`. 

```{.bash data-prompt="$"}
$ xtrabackup --prepare --target-dir=/data/backup \
--keyring-file-data=/var/lib/mysql-keyring/keyring
```

The following message confirms the action:

??? example "Confirmation message"

```{.text .no-copy}
InnoDB: Shutdown completed; log sequence number 5697064
160401 10:34:28 completed OK!
```

The `--component-keyring-config` option generates an error if used with the plugin.  The [encrypted backups with the keyring file component](encrypted-backup-keyring-file-component.md) uses this option.

## Copy-back

The backup is now prepared and can be restored with the `--copy-back`
option. If the keyring has rotated, restore the keyring used when the backup was taken and prepared.