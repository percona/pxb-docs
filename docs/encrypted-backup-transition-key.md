# Encrypted tablespace backup with transition-key

While the described restore method works, this method requires access to
the same keyring that the server is using. It may not be possible if the backup is
prepared on a different server or at a much later time, when keys in the keyring are
purged, or, in the case of a malfunction, when the keyring vault server is not available at all.

The `--transition-key=<passphrase>` option should be used to make it possible for *xtrabackup* to process the backup without access to the keyring vault server. In this case, *xtrabackup* derives the AES encryption key from the specified passphrase and will use it to encrypt tablespace keys of tablespaces that are being backed up.

## Create a backup with a passphrase

    The following example illustrates how the backup can be created in this
    case:

    ```{.bash data-prompt="$"}
    $ xtrabackup --backup --user=root -p --target-dir=/data/backup \
    --transition-key=MySecretKey
    ```

    If `--transition-key` is specified without a value, xtrabackup asks for it.

    xtrabackup scrapes `--transition-key` so that its value is not visible in the `ps` command output.

  ## Prepare a backup with a passphrase

    The same passphrase should be specified for the prepare command:

    ```{.bash data-prompt="$"}
    $ xtrabackup --prepare --target-dir=/data/backup \
    --transition-key=MySecretKey
    ```

    There are no `--keyring-vault...`,\`\`–keyring-file…\`\`,
    or `--component-keyring-file-config` options here,
    because *xtrabackup* does not talk to the keyring in this case.

  ## Restore a backup with a generated key

    When restoring a backup you will need to generate a new master key. Here is the example for `keyring_file` plugin or component:

    ```{.bash data-prompt="$"}
    $ xtrabackup --copy-back --target-dir=/data/backup --datadir=/data/mysql \
    --transition-key=MySecretKey --generate-new-master-key \
    --keyring-file-data=/var/lib/mysql-keyring/keyring
    ```

    In case of `keyring_vault`, it will look like this:

    ```{.bash data-prompt="$"}
    $ xtrabackup --copy-back --target-dir=/data/backup --datadir=/data/mysql \
    --transition-key=MySecretKey --generate-new-master-key \
    --keyring-vault-config=/etc/vault.cnf
    ```

    *xtrabackup* will generate a new master key, store it in the target keyring
    vault server and re-encrypt the tablespace keys using this key.

 ## Make a backup with a stored transition key

    Finally, there is an option to store a transition key in the keyring. In this case, *xtrabackup* will need to access the same keyring file or vault server during prepare and copy-back but does not depend on whether the server keys have been purged.

    In this scenario, the three stages of the backup process look as follows.

    * Backup

    ```{.bash data-prompt="$"}
    $ xtrabackup --backup --user=root -p --target-dir=/data/backup \
    --generate-transition-key
    ```

    * Prepare

    - `keyring_file` variant:

    ```{.bash data-prompt="$"}
    $ xtrabackup --prepare --target-dir=/data/backup \
    --keyring-file-data=/var/lib/mysql-keyring/keyring
    ```

    - `keyring_vault` variant:

    ```{.bash data-prompt="$"}
    $ xtrabackup --prepare --target-dir=/data/backup \
    --keyring-vault-config=/etc/vault.cnf
    ```

    * Copy-back

    - `keyring_file` variant:

    ```{.bash data-prompt="$"}
    $ xtrabackup --copy-back --target-dir=/data/backup --datadir=/data/mysql \
    --generate-new-master-key --keyring-file-data=/var/lib/mysql-keyring/keyring
    ```

    - `keyring_vault` variant:

    ```{.bash data-prompt="$"}
    $ xtrabackup --copy-back --target-dir=/data/backup --datadir=/data/mysql \
    --generate-new-master-key --keyring-vault-config=/etc/vault.cnf
    ```
    