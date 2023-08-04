# Use `keyring_vault` plugin

The keyring vault plugin settings are
described in [using the keyring plugin](https://www.percona.com/doc/percona-server/LATEST/security/using-keyring-plugin.html#using-keyring-plugin).

## Create a backup with the `keyring_vault` plugin

The following command creates a backup in the `/data/backup` directory:

```{.bash data-prompt="$"}
$ xtrabackup --backup --target-dir=/data/backup --user=root
```

After xtrabackup completes the action, the following message confirms
the action:

??? example "Confirmation message"

    ```{.text .no-copy}
    xtrabackup: Transaction log of lsn (5696709) to (5696718) was copied.
    160401 10:25:51 completed OK!
    ```

## Prepare the backup with the `keyring_vault` plugin

To prepare the backup, xtrabackup must access the keyring.
xtrabackup does not communicate with the MySQL server or read the
default `my.cnf` configuration file. Specify the keyring settings in the
command line:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --target-dir=/data/backup \
--keyring-vault-config=/etc/vault.cnf
```

After xtrabackup completes the action, the following message confirms
the action:

??? example "Confirmation message"

    ```{.text .no-copy}
    InnoDB: Shutdown completed; log sequence number 5697064
    160401 10:34:28 completed OK!
    ```

The backup is now prepared and can be restored with the `--copy-back`
option:

```{.bash data-prompt="$"}
$ xtrabackup --copy-back --target-dir=/data/backup --datadir=/data/mysql
```