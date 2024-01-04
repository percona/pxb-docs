# Encrypt backups
Percona XtraBackup supports encrypting and decrypting local and streaming backups with the upstream option, adding another protection layer. The
encryption is implemented using the `libgcrypt` library from GnuPG.

## Create encrypted backups

The following options create encrypted backups. The
`--encrypt-key` and `--encrypt-key-file` options specify the encryption key and are mutually exclusive. You should select one or the other.

* `--encrypt`

* `--encrypt-key`

* `--encrypt-key-file`

For an encryption key, use a command, such as `openssl rand -base64 24`, to generate a random alphanumeric string.

### The `--encrypt-key` option

An example of the *xtrabackup* command using the `--encrypt-key`:

```{.bash data-prompt="$"}
$  xtrabackup --backup --encrypt=AES256 --encrypt-key="{randomly-generated-alphanumeric-string}" --target-dir=/data/backup
```

### The `--encrypt-key-file` option

The recommended method uses the command line: `echo -n “{randomly-generated-alphanumeric-string}” > /data/backups/keyfile` to create the file.

Remember that your text editor can automatically insert a CRLF (end of line) character in the `KEYFILE` when using the-- `encrypt-key-file` option. This inserted character invalidates the key because the size is wrong. 

An example of using the `--encrypt-key-file` option:

```{.bash data-prompt="$"}
$ xtrabackup --backup --encrypt=AES256 --encrypt-key-file=/data/backups/keyfile --target-dir=/data/backup
```

## Optimize the encryption process

Additional encrypted backup options, `--encrypt-threads` and
`--encrypt-chunk-size`, can speed up the encryption process. 

Use the `--encrypt-threads` option to enable parallel encryption with multiple threads. 

The `--encrypt-chunk-size` option specifies the size, in bytes, of the working encryption buffer for each encryption thread. The default size is 64K.

## Decrypt encrypted backups

You can decrypt backups with the `xbcrypt` binary. The following example encrypts a backup.

You can use the `--parallel` option and the `--decrypt` option to decrypt multiple files simultaneously.

```{.bash data-prompt="$"}
$ for i in `find . -iname "*\.xbcrypt"`; do xbcrypt -d --encrypt-key-file=/root/secret_key --encrypt-algo=AES256 < $i > $(dirname $i)/$(basename $i .xbcrypt) && rm $i; done
```

The following example shows a decryption process.

```{.bash data-prompt="$"}
$ xtrabackup --decrypt=AES256 --encrypt-key="{randomly-generated-alphanumeric-string}" --target-dir=/data/backup/
```

Percona XtraBackup doesn’t automatically remove the encrypted files. You must remove the `\*.xbcrypt` files manually.

## Prepare encrypted backups

After decrypting the backups, prepare the backups with the `--prepare` option:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --target-dir=/data/backup/
```

## Restore encrypted backups

*xtrabackup* offers the `--copy-back` option to restore a backup to the server’s datadir:

```{.bash data-prompt="$"}
$ xtrabackup --copy-back --target-dir=/data/backup/
```

The option copies all the data-related files to the server’s datadir. The server’s `my.cnf` configuration file determines the location. 

You should check the last line of the output for a success message:

??? example "Expected output"

    ```{.text .no-copy}
    150318 11:08:13  xtrabackup: completed OK!
    ```