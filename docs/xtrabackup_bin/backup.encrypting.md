# Encrypt backups

*Percona XtraBackup* supports encrypting and decrypting local and streaming
backups with *xbstream* option adding another layer of protection. The
encryption is implemented using the `libgcrypt` library from GnuPG.

## Create encrypted backups

To make an encrypted backup the following options need to be specified (options
`--encrypt-key` and `--encrypt-key-file` are mutually exclusive,
i.e. just one of them needs to be provided):


* `--encrypt`


* `--encrypt-key`


* `--encrypt-key-file`

Both the `--encrypt-key` option and
`--encrypt-key-file` option can be used to specify the
encryption key. An encryption key can be generated with a command like
`openssl rand -base64 24`

```text
U2FsdGVkX19VPN7VM+lwNI0fePhjgnhgqmDBqbF3Bvs=
```

This value then can be used as the encryption key

### The `--encrypt-key` option

Example of the *xtrabackup* command using the `--encrypt-key` should
look like this:

```{.bash data-prompt="$"}
$  xtrabackup --backup --encrypt=AES256 --encrypt-key="U2FsdGVkX19VPN7VM+lwNI0fePhjgnhgqmDBqbF3Bvs=" --target-dir=/data/backup
```

### The `--encrypt-key-file` option

Use the `--encrypt-key-file` option as follows:

```{.bash data-prompt="$"}
$ xtrabackup --backup --encrypt=AES256 --encrypt-key-file=/data/backups/keyfile --target-dir=/data/backup
```

!!! note
   
    Depending on the text editor that you use to make the `KEYFILE`,
    the editor can automatically insert the CRLF (end of line)
    character. This will cause the key size to grow and thus making it
    invalid. The suggested way to create the file is by using the
    command line: `echo -n “U2FsdGVkX19VPN7VM+lwNI0fePhjgnhgqmDBqbF3Bvs=” > /data/backups/keyfile`.

## Optimize the encryption process

Two new options are available for encrypted backups that can be used to speed up
the encryption process. These are `--encrypt-threads` and
`--encrypt-chunk-size`. By using the `--encrypt-threads` option
multiple threads can be specified to be used for encryption in parallel. Option
`--encrypt-chunk-size` can be used to specify the size (in bytes) of the
working encryption buffer for each encryption thread (default is 64K).

## Decrypt encrypted backups

Backups can be decrypted with The xbcrypt binary. The following one-liner can be
used to encrypt the whole folder:

```{.bash data-prompt="$"}
$ for i in `find . -iname "*\.xbcrypt"`; do xbcrypt -d --encrypt-key-file=/root/secret_key --encrypt-algo=AES256 < $i > $(dirname $i)/$(basename $i .xbcrypt) && rm $i; done
```

*Percona XtraBackup* `--decrypt` option has been implemented that can be
used to decrypt the backups:

```{.bash data-prompt="$"}
$ xtrabackup --decrypt=AES256 --encrypt-key="U2FsdGVkX19VPN7VM+lwNI0fePhjgnhgqmDBqbF3Bvs=" --target-dir=/data/backup/
```

*Percona XtraBackup* doesn’t automatically remove the encrypted files. In order
to clean up the backup directory users should remove the `\*.xbcrypt` files.

!!! note
   
    `--parallel` can be used with `--decrypt` option to decrypt multiple files simultaneously.

When the files are decrypted, the backup can be prepared.

## Prepare encrypted backups

After the backups have been decrypted, they can be prepared in the same way as
the standard full backups with the `--prepare` option:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --target-dir=/data/backup/
```

## Restore encrypted backups

*xtrabackup* offers the `--copy-back` option to restore a backup to the
server’s datadir:

```{.bash data-prompt="$"}
$ xtrabackup --copy-back --target-dir=/data/backup/
```

It will copy all the data-related files back to the server’s datadir,
determined by the server’s `my.cnf` configuration file. You should check
the last line of the output for a success message:

??? example "Expected output"

    ```{.text .no-copy}
    150318 11:08:13  xtrabackup: completed OK!
    ```
