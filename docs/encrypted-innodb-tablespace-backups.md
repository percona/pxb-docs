<!--- We should probably remove the info about `keyring_file` plugin-->

# Encrypted InnoDB tablespace backups

InnoDB supports [data encryption for InnoDB tables] stored in file-per-table tablespaces. This feature provides an at-rest
encryption for physical tablespace data files.

For an authenticated user or application to access an  encrypted 
tablespace, InnoDB uses the master encryption key to decrypt 
the tablespace key. The master encryption key is stored in a keyring. 
xtrabackup supports two keyring plugins: `keyring_file`, and 
`keyring_vault`. These plugins are installed into the `plugin` directory.

Percona XtraBackup supports the Amazon Key Management
Service (AWS KMS). AWS KMS is cloud-based encryption and key management
service. The keys and functionality can be used for other AWS services
or your applications that use AWS. No configuration is required to back
up a server with AWS KMS-enabled encryption. 

<!--- We should probably remove the info about `keyring_file` plugin
## Use `keyring_file` plugin

In order to back up and prepare a database containing encrypted InnoDB  
tablespaces, specify the path to a keyring file as the value of the
`--keyring-file-data` option.

```{.bash data-prompt="$"}
$ xtrabackup --backup --target-dir=/data/backup/ --user=root \
--keyring-file-data=/var/lib/mysql-keyring/keyring
```

After xtrabackup takes the backup, the following
message confirms the action:

??? example "Confirmation message"

    ```{.text .no-copy}
    xtrabackup: Transaction log of lsn (5696709) to (5696718) was copied.
    160401 10:25:51 completed OK!
    ```

!!! warning
   
    xtrabackup does not copy the keyring file into the backup directory. To prepare the backup, you must copy the keyring file manually.

### Prepare the backup with the `keyring_file` plugin

To prepare the backup specify the keyring-file-data.

```{.bash data-prompt="$"}
$ xtrabackup --prepare --target-dir=/data/backup \
--keyring-file-data=/var/lib/mysql-keyring/keyring
```

After xtrabackup takes the backup, the following message confirms
the action:

??? example "Confirmation message"

    ```{.text .no-copy}
    InnoDB: Shutdown completed; log sequence number 5697064
    160401 10:34:28 completed OK!
    ```

The backup is now prepared and can be restored with the `--copy-back`
option. In case the keyring has been rotated, you must restore the
keyring used when the backup was taken and prepared.

## Use `keyring_vault` plugin

Keyring vault plugin settings are described in [Use the keyring component or keyring plugin](https://docs.percona.com/percona-server/{{vers}}/using-keyring-plugin.html).

### Create a backup with the `keyring_vault` plugin

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

### Prepare the backup with the `keyring_vault` plugin

To prepare the backup, xtrabackup must access the keyring.
xtrabackup does not communicate with the MySQL server or read the
default `my.cnf` configuration file. Specify the keyring settings in the
command line:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --target-dir=/data/backup \
--keyring-vault-config=/etc/vault.cnf
```

Review [Use the keyring component or keyring plugin](https://docs.percona.com/percona-server/{{vers}}/using-keyring-plugin.html) for a description of keyring vault plugin settings.

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
-->

## Use the `keyring_file` component

A component is not loaded with the `--early_plugin_load` option. The 
server uses a manifest to load the component and the component has its 
own configuration file. See the [MySQL documentation on the component 
installation] for more information.

An example of a manifest and a configuration file follows:

An example of `./bin/mysqld.my`:

```json
{
   "components": "file://component_keyring_file"
}
```

An example of `/lib/plugin/component_keyring_file.cnf`:

```json
{
   "path": "/var/lib/mysql-keyring/keyring_file", "read_only": false
}
```

For more information, see [Keyring Component Installation] and [Using the keyring_file File-Based Keyring Plugin].

With the appropriate privilege, you can `SELECT` on
the [performance_schema.keyring_component_status table] to view the attributes and status of the installed keyring component 
when in use.

The component has no special requirements for backing up a database that
contains encrypted InnoDB tablespaces.

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

!!! warning
   
    xtrabackup does not copy the keyring file into the backup directory. To prepare the backup, you must copy the keyring file manually.


### Prepare the backup with the `keyring_file` component

xtrabackup reads the keyring_file component configuration
from `xtrabackup_component_keyring_file.cnf`. You must specify the
keyring_file data path if the `keyring-file-data` is not located in the
attribute `PATH` from the xtrabackup_component_keyring_file.cnf.

The following is an example of adding the location for the
keyring-file-data:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --target-dir=/data/backup \
--keyring-file-data=/var/lib/mysql-keyring/keyring
```

xtrabackup attempts to read `xtrabackup_component_keyring_file.cnf`. You can assign another keyring file component configuration by passing the `--component-keyring-file-config` option.

After xtrabackup completes preparing the backup, the following message confirms
the action:

??? example "Confirmation message"

    ```{.text .no-copy}
    InnoDB: Shutdown completed; log sequence number 5697064
    160401 10:34:28 completed OK!
    ```

The backup is prepared. To restore the backup use the `--copy-back` option.
If the keyring has been rotated, you must restore the specific keyring used
to take and prepare the backup.

## Incremental encrypted InnoDB tablespace backups with `keyring_file`

The process of taking incremental backups with InnoDB tablespace encryption
is similar to taking the Incremental Backups with unencrypted tablespace. The `keyring-file` component should not used in production or for regulatory compliance.

## Create an incremental backup

To make an incremental backup, begin with a full backup. The xtrabackup
binary
writes a file called `xtrabackup_checkpoints` into the backup’s target
directory. This file contains a line showing the `to_lsn`, which is the
database’s LSN at the end of the backup. First you need to create a full
backup with the following command:

```{.bash data-prompt="$"}
$ xtrabackup --backup --target-dir=/data/backups/base \
--keyring-file-data=/var/lib/mysql-keyring/keyring
```

In order to prepare the backup, you must make a copy of the keyring file yourself. xtrabackup does not copy the keyring file into the backup directory.  Restoring the backup after the keyring has been changed causes errors like `ERROR 3185 (HY000): Can't find master key from keyring, please check keyring plugin is loaded.` when the restore process tries accessing an encrypted table.

If you look at the `xtrabackup_checkpoints` file, you should see
the output similar to the following:

??? example "Expected output"

    ```{.text .no-copy}
    backup_type = full-backuped
    from_lsn = 0
    to_lsn = 7666625
    last_lsn = 7666634
    compact = 0
    recover_binlog_info = 1
    ```

Now that you have a full backup, you can make an incremental backup based
on it. Use a command such as the following:

```{.bash data-prompt="$"}
$ xtrabackup --backup --target-dir=/data/backups/inc1 \
--incremental-basedir=/data/backups/base \
--keyring-file-data=/var/lib/mysql-keyring/keyring
```

To prepare the backup, you must copy the keyring file manually. xtrabackup does not copy the keyring file into the backup directory. 

If the
keyring has not been rotated you can use the same as the one you’ve
backed-up with the base backup. If the keyring has been rotated, or you have 
upgraded the plugin to a component, you must back up the keyring file. 
Otherwise, you cannot prepare the backup.

The `/data/backups/inc1/` directory should now contain delta files, such
as `ibdata1.delta` and `test/table1.ibd.delta`. These represent the
changes since the `LSN 7666625`. If you examine the
`xtrabackup_checkpoints` file in this directory, you should see 
the output similar to the following:

??? example "Expected output"

    ```{.text .no-copy}
    backup_type = incremental
    from_lsn = 7666625
    to_lsn = 8873920
    last_lsn = 8873929
    compact = 0
    recover_binlog_info = 1
    ```

Use this directory as the base for yet another incremental backup:

```{.bash data-prompt="$"}
$ xtrabackup --backup --target-dir=/data/backups/inc2 \
--incremental-basedir=/data/backups/inc1 \
--keyring-file-data=/var/lib/mysql-keyring/keyring
```

### Prepare incremental backups

The `--prepare` step for incremental backups is not the same as for
normal backups. In normal backups, two types of operations are performed to
make
the database consistent: committed transactions are replayed from the log
file
against the data files, and uncommitted transactions are rolled back. You
must
skip the rollback of uncommitted transactions when preparing a backup,
because
transactions that were uncommitted at the time of your backup may be in
progress, and it’s likely that they will be committed in the next
incremental
backup. You should use the `--apply-log-only` option to prevent the
rollback phase.

If you do not use the `--apply-log-only` option to prevent the rollback phase, then your incremental backups are useless. After transactions have been rolled back, further incremental backups cannot be applied.

Beginning with the full backup you created, you can prepare it and then
apply the incremental differences to it. Recall that you have the following backups:

```{.text .no-copy}
/data/backups/base
/data/backups/inc1
/data/backups/inc2
```

To prepare the base backup, you need to run `--prepare` as usual, but
prevent the rollback phase:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --apply-log-only --target-dir=/data/backups/base \
--keyring-file-data=/var/lib/mysql-keyring/keyring
```

??? example "Expected output"

    ```{.text .no-copy}
    InnoDB: Shutdown completed; log sequence number 7666643
    InnoDB: Number of pools: 1
    160401 12:31:11 completed OK!
    ```

To apply the first incremental backup to the full backup, you should use
the following command:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --apply-log-only --target-dir=/data/backups/base \
--incremental-dir=/data/backups/inc1 \
--keyring-file-data=/var/lib/mysql-keyring/keyring
```

The backup should be prepared with the keyring file and type that was used when backup was being taken. This means that if the keyring has been rotated, or you have upgraded from a plugin to a component between the base and incremental backup that you must use the keyring that was in use when the first incremental backup has been taken.

Preparing the second incremental backup is a similar process: apply the
deltas
to the (modified) base backup, and you will roll its data forward in 
time to the point of the second incremental backup:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --target-dir=/data/backups/base \
--incremental-dir=/data/backups/inc2 \
--keyring-file-data=/var/lib/mysql-keyring/keyring
```
Use `--apply-log-only` when merging all incremental backups except the last one. That’s why the previous line does not contain the `--apply-log-only` option. Even if the `--apply-log-only` was used on the last step, backup would still be consistent but in that case  server would perform the rollback phase.

The backup is now prepared and can be restored with `--copy-back` option.
In case the keyring has been rotated you’ll need to restore the keyring which was used to take and prepare the backup.

## Use the Key Management Interoperability Protocol (KMIP)

Percona XtraBackup 8.0.27-19 adds support for the Key Management
Interoperability Protocol (KMIP) which enables the communication between
the key management system and encrypted database server.

Percona XtraBackup has no special requirements for backing up a database
that contains encrypted InnoDB tablespaces.

Percona XtraBackup performs the following actions:

1. Connects to the MySQL server

2. Pulls the configuration

3. Connects to the KMIP server

4. Fetches the necessary keys from the KMIP server

5. Stores the KMIP server configuration settings in  the `xtrabackup_component_keyring_kmip.cnf` file in the backup directory

When preparing the backup, Percona XtraBackup connects to the KMIP server
with the settings from the `xtrabackup_component_keyring_kmip.cnf` file.

## Restore a backup when the keyring is not available

While the described restore method works, this method requires access to
the same keyring that the server is using. It may not be possible if the backup is
prepared on a different server or at a much later time, when keys in the keyring are
purged, or, in the case of a malfunction, when the keyring vault server is not available at all.

The `--transition-key=<passphrase>` option should be used to make it possible for xtrabackup to process the backup without access to the keyring vault server. In this case, xtrabackup derives the AES encryption key from the specified passphrase and will use it to encrypt tablespace keys of tablespaces that are being backed up.

### Create a backup with a passphrase

The following example illustrates how the backup can be created in this
case:

```{.bash data-prompt="$"}
$ xtrabackup --backup --user=root -p --target-dir=/data/backup \
--transition-key=MySecretKey
```

If `--transition-key` is specified without a value, xtrabackup will ask for it.

xtrabackup scrapes `--transition-key` so that its value is not visible in the `ps` command output.

### Prepare a backup with a passphrase

The same passphrase should be specified for the prepare command:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --target-dir=/data/backup \
--transition-key=MySecretKey
```

There are no `--keyring-vault...`,\`\`–keyring-file…\`\`,
or `--component-keyring-file-config` options here,
because xtrabackup does not talk to the keyring in this case.

### Restore a backup with a generated key

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

xtrabackup will generate a new master key, store it in the target keyring
vault server and re-encrypt the tablespace keys using this key.

### Make a backup with a stored transition key

Finally, there is an option to store a transition key in the keyring. In this case, xtrabackup will need to access the same keyring file or vault server during prepare and copy-back but does not depend on whether the server keys have been purged.

In this scenario, the three stages of the backup process look as follows.

* Back up

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

[data encryption for InnoDB tables]: https://dev.mysql.com/doc/refman/{{vers}}/en/innodb-data-encryption.html
[MySQL documentation on the component installation]: https://dev.mysql.com/doc/refman/{{vers}}/en/keyring-component-installation.html
[Keyring Component Installation]: https://dev.mysql.com/doc/refman/{{vers}}/en/keyring-component-installation.html
[Using the keyring_file File-Based Keyring Plugin]: https://dev.mysql.com/doc/refman/{{vers}}/en/keyring-file-plugin.html
[performance_schema.keyring_component_status table]: https://dev.mysql.com/doc/refman/{{vers}}/en/performance-schema-keyring-component-status-table.html