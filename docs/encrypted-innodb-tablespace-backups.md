# Encrypted InnoDB tablespace backups

Percona XtraBackup supports two distinct types of encryption:

* [InnoDB tablespace encryption](#innodb-tablespace-encryption): The MySQL server handles encryption using keyring components. InnoDB tablespace encryption provides at-rest encryption for physical tablespace data files at the database level.

* [Backup-level encryption](#backup-level-encryption): XtraBackup applies an additional encryption layer during the backup process, independent of InnoDB encryption. Backup-level encryption protects backup files themselves.

These encryption types are independent. You can use them separately or together for enhanced security.

## InnoDB tablespace encryption

InnoDB supports [data encryption for InnoDB tables] in file-per-table tablespaces. When accessing an encrypted tablespace, InnoDB uses the master encryption key to decrypt the tablespace key. InnoDB stores the master encryption key in a keyring.

Percona XtraBackup supports the following keyring components:

* [keyring_vault](#keyring_vault-configuration)
* [keyring_file](#keyring_file-configuration)
* [Key Management Interoperability Protocol (KMIP)]
* [Amazon Key Management Service (AWS KMS)]

Percona XtraBackup {{vers}} and later versions support only component versions of the security features.


## Workflow phases

The backup and restore process for encrypted InnoDB tablespaces has three distinct phases, each with different keyring-config requirements:

| Phase | Description | Required | keyring-options |
|-------|-------------|---------|----------------|
| Backup | Run `xtrabackup --backup …` | No | The backup does not use any keyring options. |
| Prepare | Run `xtrabackup --prepare …` | Yes | You must supply the keyring configuration file matching the keyring component that the MySQL server uses for encryption. |
| Restore | Run `xtrabackup` [`--copy-back`](xtrabackup-option-reference.md#copy-back) … or `xtrabackup` [`--move-back`](xtrabackup-option-reference.md#move-back) … (followed by `--prepare` if using [`--move-back`](xtrabackup-option-reference.md#move-back)) | Yes | You must provide the same keyring-config file. |

!!! note

    If you rotated the keyring using `ALTER INSTANCE ROTATE INNODB MASTER KEY`, you must use the keyring that was active when you created the backup to prepare and restore the backup.

### Configuration file name requirements

The configuration file name must match exactly the expected name for each keyring component. If the file name does not match exactly, XtraBackup ignores the configuration file.

| Component | Expected config-file name |
|-----------|---------------------------|
| Vault | `component_keyring_vault.cnf` |
| KMS | `component_keyring_kms.cnf` |
| KMIP | `component_keyring_kmip.cnf` |
| File | `component_keyring_file.cnf` |

### Keyring component configuration files

Each keyring component requires a configuration file with a specific structure. The following examples show the format for each component type.

#### keyring_vault configuration

The `component_keyring_vault.cnf` file uses JSON format:

```json
{
  "vault_url": "${VAULT_URL}",
  "secret_mount_point": "${VAULT_MOUNT_POINT}",
  "secret_mount_point_version": "${VAULT_CONFIG_VERSION}",
  "token": "${VAULT_TOKEN}",
  "vault_ca": "${VAULT_CA}"
}
```

For information on configuring the keyring vault component on the MySQL server, see [Use the keyring vault component].

#### keyring_file configuration

The `component_keyring_file.cnf` file uses JSON format:

```json
{
  "path": "/var/lib/mysql-keyring/keyring",
  "read_only": false
}
```

!!! warning

    XtraBackup does not copy the keyring file into the backup directory. Copy the keyring file manually before preparing.

#### keyring_kmip configuration

The `component_keyring_kmip.cnf` file uses JSON format:

```json
{
  "server_addr": "kmip.example.com",
  "server_port": 5696,
  "client_ca": "/path/to/client/ca.pem",
  "client_key": "/path/to/client/key.pem",
  "server_ca": "/path/to/server/ca.pem"
}
```

#### keyring_kms configuration

The `component_keyring_kms.cnf` file uses JSON format:

```json
{
  "path": "/var/lib/mysql-keyring/keyring",
  "read_only": false,
  "region": "us-east-1",
  "auth_key": "your-auth-key",
  "secret_access_key": "your-secret-access-key",
  "kms_key": "your-kms-key-id"
}
```

### Backup and restore with keyring components

XtraBackup uses the component's configuration file during prepare and restore operations. The MySQL server must use one of the supported keyring components for encryption.

#### Phase 1: Backup

No keyring configuration is needed:

```bash
xtrabackup --backup --target-dir=/data/backup --user=root
```

#### Phase 2: Prepare

To prepare the backup, you must provide access to the keyring. The xtrabackup binary does not communicate with the MySQL server or read the default `my.cnf` configuration file. Specify the keyring configuration file.

!!! warning "File-name restriction"

    The configuration file name must match exactly the expected name for your keyring component. See [Configuration file name requirements](#configuration-file-name-requirements) for the exact file names required. If the file name does not match exactly, XtraBackup ignores the configuration file.

```bash
xtrabackup --prepare --target-dir=/data/backup
```

Specify the path to your component's configuration file (for example, `/etc/component_keyring_vault.cnf` or `/var/lib/mysql-keyring/component_keyring_file.cnf`).

#### Phase 3: Restore

After you prepare the backup, restore the backup using [`--copy-back`](xtrabackup-option-reference.md#copy-back) or [`--move-back`](xtrabackup-option-reference.md#move-back). If you use [`--move-back`](xtrabackup-option-reference.md#move-back), run `--prepare` again after moving the files. In both cases, provide the same keyring configuration file.

```bash
xtrabackup --copy-back --target-dir=/data/backup --datadir=/data/mysql
```

Or using `--move-back`:

```bash
xtrabackup --move-back --target-dir=/data/backup --datadir=/data/mysql
xtrabackup --prepare --target-dir=/data/mysql
```

### Incremental encrypted InnoDB tablespace backups

The process of taking incremental backups with InnoDB tablespace encryption is similar to [taking incremental backups with unencrypted tablespace](create-incremental-backup.md). The same three-phase workflow applies, with keyring-config requirements in phases 2 and 3.

#### Phase 1: Backup

Begin with a full backup. The xtrabackup binary writes `xtrabackup_checkpoints` into the backup's target directory, which contains the `to_lsn` (the LSN of the database at the end of the backup).

Create a full backup (no keyring config needed):

```bash
xtrabackup --backup --target-dir=/data/backups/base
```

Make an incremental backup based on the full backup:

```bash
xtrabackup --backup --target-dir=/data/backups/inc1 \
--incremental-basedir=/data/backups/base
```

The [`--incremental-basedir`](xtrabackup-option-reference.md#incremental-basedir) option specifies the base backup directory.

Use this directory as the base for yet another incremental backup:

```bash
xtrabackup --backup --target-dir=/data/backups/inc2 \
--incremental-basedir=/data/backups/inc1
```

#### Phase 2: Prepare

The `--prepare` step for incremental backups requires the keyring configuration. Use [`--apply-log-only`](xtrabackup-option-reference.md#apply-log-only) for all incremental backups except the last one to prevent rolling back transactions that might be committed in subsequent incremental backups.

Beginning with the full backup, prepare the full backup and then apply the incremental differences. Prepare the base backup with [`--apply-log-only`](xtrabackup-option-reference.md#apply-log-only). Use the appropriate configuration file name for your keyring component (see [Configuration file name requirements](#configuration-file-name-requirements)):

```bash
xtrabackup --prepare --apply-log-only --target-dir=/data/backups/base
```

Apply the first incremental backup to the full backup using [`--incremental-dir`](xtrabackup-option-reference.md#incremental-dir):

```bash
xtrabackup --prepare --apply-log-only --target-dir=/data/backups/base \
--incremental-dir=/data/backups/inc1
```

!!! note
   
    If you have many InnoDB Data (IBD) files, speed up the prepare phase for incremental backups  by using the `--parallel` option. This option lets you process multiple delta files simultaneously. When using `--parallel` in the prepare phase, always specify a numeric value. The recommended minimum value is 4 (for example, `--parallel=4`).
    
    An example of the backup command using the `--parallel` option:
    
    ```shell
    xtrabackup --prepare --apply-log-only --target-dir=/data/backups/base \
    --incremental-dir=/data/backups/inc1 --parallel=4
    ```

Prepare the backup using the same keyring file and type that were used when the backup was created. If the keyring has changed or you upgraded from a plugin to a component between the base and incremental backup, use the keyring from when the first incremental backup was made. If the original keyring is missing or has changed, recover or replace it before restoring. If you cannot recover the keyring, restore from a backup that matches the most recent available keyring.

Preparing the second incremental backup is a similar process: apply the deltas
to the (modified) base backup, and you will roll the base backup's data forward in 
time to the point of the second incremental backup:

```shell
xtrabackup --prepare --target-dir=/data/backups/base \
--incremental-dir=/data/backups/inc2
```

You can also use the `--parallel` option here to speed up the process:

```shell
xtrabackup --prepare --target-dir=/data/backups/base \
--incremental-dir=/data/backups/inc2 --parallel=4
```

!!! note

    Use [`--apply-log-only`](xtrabackup-option-reference.md#apply-log-only) when merging all incremental backups except for the last one. This is why the previous command does not include the `--apply-log-only` option. If `--apply-log-only` is used on the last step, backup remains consistent but the server performs the rollback phase.

#### Phase 3: Restore

After you prepare the incremental backups, restore them using [`--copy-back`](xtrabackup-option-reference.md#copy-back) or [`--move-back`](xtrabackup-option-reference.md#move-back). If you use [`--move-back`](xtrabackup-option-reference.md#move-back), run `--prepare` again after moving the files. In both cases, provide the same keyring configuration file:

```bash
xtrabackup --copy-back --target-dir=/data/backups/base --datadir=/data/mysql
```

Or using `--move-back`:

```bash
xtrabackup --move-back --target-dir=/data/backups/base --datadir=/data/mysql
xtrabackup --prepare --target-dir=/data/mysql
```

### Restore a backup when the keyring is not available

The keyring component method requires access to the same keyring that the server uses. This may not be possible if you prepare the backup on a different server, when keys in the keyring are purged, or when the keyring vault server is unavailable.

Use the [`--transition-key=<passphrase>`](xtrabackup-option-reference.md#transition-key) option to process the backup without access to the keyring server. The binary derives the AES (Advanced Encryption Standard) encryption key from the specified passphrase and uses the AES encryption key to encrypt tablespace keys.

#### Create a backup with a passphrase

```bash
xtrabackup --backup --user=root -p --target-dir=/data/backup \
--transition-key=MySecretKey
```

If you specify [`--transition-key`](xtrabackup-option-reference.md#transition-key) without a value, xtrabackup asks for the passphrase. xtrabackup hides the passphrase value so that the value is not visible in the `ps` command output.

#### Prepare a backup with a passphrase

Specify the same passphrase for the prepare command:

```bash
xtrabackup --prepare --target-dir=/data/backup \
--transition-key=MySecretKey
```

You do not need keyring options here, because xtrabackup does not access the keyring in this case.

#### Restore a backup with a generated key

When you restore a backup, generate a new master key using [`--generate-new-master-key`](xtrabackup-option-reference.md#generate-new-master-key). The configuration file name must match one of the exact configuration file names listed in [Configuration file name requirements](#configuration-file-name-requirements):

```bash
xtrabackup --copy-back --target-dir=/data/backup --datadir=/data/mysql \
--transition-key=MySecretKey --generate-new-master-key
```

Specify the path to your component's configuration file. XtraBackup generates a new master key, stores the new master key in the target keyring, and re-encrypts the tablespace keys using the new master key.

#### Make a backup with a stored transition key

You can store a transition key in the keyring. In this case, xtrabackup must access the same keyring during prepare and copy-back steps, but xtrabackup does not depend on whether the server keys have been purged. The configuration file name must match one of the exact configuration file names listed in [Configuration file name requirements](#configuration-file-name-requirements):

* Back up using [`--generate-transition-key`](xtrabackup-option-reference.md#generate-transition-key):

  ```bash
  xtrabackup --backup --user=root -p --target-dir=/data/backup \
  --generate-transition-key
  ```

* Prepare:

  ```bash
  xtrabackup --prepare --target-dir=/data/backup
  ```

* Copy-back:

  ```bash
  xtrabackup --copy-back --target-dir=/data/backup --datadir=/data/mysql \
  --generate-new-master-key
  ```

Specify the path to your component's configuration file.

## Backup-level encryption

Backup-level encryption is an additional protection layer that XtraBackup applies during the backup process. Backup-level encryption is independent of InnoDB tablespace encryption and protects the backup files themselves. XtraBackup implements the encryption using the `libgcrypt` library from GnuPG. You can use backup-level encryption on any backup, regardless of whether the source database uses InnoDB tablespace encryption.

### Create encrypted backups

To create an encrypted backup, use the [`--encrypt`](xtrabackup-option-reference.md#encrypt) option along with either [`--encrypt-key`](xtrabackup-option-reference.md#encrypt-key) or [`--encrypt-key-file`](xtrabackup-option-reference.md#encrypt-key-file) to specify the encryption key. The `--encrypt-key` and `--encrypt-key-file` options are mutually exclusive. Use one or the other, but do not both. If you specify both options, XtraBackup returns an error and exits.

The `--encrypt` option specifies the encryption algorithm: `AES128`, `AES192`, or `AES256`. To generate an encryption key, use a command such as `openssl rand -base64 24`.

#### Using --encrypt-key

```bash
xtrabackup --backup --encrypt=AES256 --encrypt-key="{randomly-generated-alphanumeric-string}" --target-dir=/data/backup
```

!!! note

    The `--encrypt-key` option exposes the key in process listings. Do not use this option on systems with uncontrolled access.

#### Using --encrypt-key-file

The recommended method uses `--encrypt-key-file` to read the key from a file:

```bash
echo -n "{randomly-generated-alphanumeric-string}" > /data/backups/keyfile
xtrabackup --backup --encrypt=AES256 --encrypt-key-file=/data/backups/keyfile --target-dir=/data/backup
```

!!! warning

    When creating the key file, ensure your text editor does not insert a CRLF (end of line) character. This invalidates the key because the size is wrong. Use `echo -n` to create the file without a trailing newline.

### Optimize the encryption process

Additional encrypted backup options can speed up the encryption process: [`--encrypt-threads`](xtrabackup-option-reference.md#encrypt-threads) (enables parallel encryption with multiple threads) and [`--encrypt-chunk-size`](xtrabackup-option-reference.md#encrypt-chunk-size) (specifies the size, in bytes, of the working encryption buffer for each encryption thread; the default value is 64K).

### Decrypt encrypted backups

To decrypt an encrypted backup, use the [`--decrypt`](xtrabackup-option-reference.md#decrypt) option. The decryption algorithm must match the algorithm that you used during encryption. You can use the [`--parallel`](xtrabackup-option-reference.md#parallel) option with `--decrypt` to decrypt multiple files simultaneously.

```bash
xtrabackup --decrypt=AES256 --encrypt-key-file=/data/backups/keyfile --target-dir=/data/backup
```

Alternatively, you can use the `xbcrypt` binary directly:

```bash
for i in `find . -iname "*\.xbcrypt"`; do xbcrypt -d --encrypt-key-file=/root/secret_key --encrypt-algo=AES256 < $i > $(dirname $i)/$(basename $i .xbcrypt) && rm $i; done
```

!!! note

    Percona XtraBackup does not automatically remove the encrypted files after decryption. Remove the `*.xbcrypt` files manually, or use the [`--remove-original`](xtrabackup-option-reference.md#remove-original) option.

### Prepare encrypted backups

After decrypting the backup, prepare the backup with the `--prepare` option:

```bash
xtrabackup --prepare --target-dir=/data/backup
```

[data encryption for InnoDB tables]: https://dev.mysql.com/doc/refman/{{vers}}/en/innodb-data-encryption.html
[Amazon Key Management Service (AWS KMS)]: https://docs.percona.com/percona-server/8.4/using-amz-kms.html
[Key Management Interoperability Protocol (KMIP)]: https://docs.percona.com/percona-server/8.4/using-kmip.html?h=kmip
[Use the keyring vault component]: https://docs.percona.com/percona-server/8.4/use-keyring-vault-component.html
