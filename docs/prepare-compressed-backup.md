# Prepare the backup

Before you can prepare the backup you’ll need to uncompress all the files.
*Percona XtraBackup* has implemented `--decompress` option
that can be used to decompress the backup.

```{.bash data-prompt="$"}
$ xtrabackup --decompress --target-dir=/data/compressed/
```

!!! note
   
    `--parallel` can be used with `--decompress` option to decompress multiple files simultaneously. 

*Percona XtraBackup* does not automatically remove the compressed files. In order to clean up the backup directory you should use `--remove-original` option. Even if they’re not removed these files will not be copied/moved over to the datadir if `--copy-back` or `--move-back` are used.

When the files are uncompressed you can prepare the backup with the `--prepare` option:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --target-dir=/data/compressed/
```

??? example "Confirmation message"

    ```{.text .no-copy}
    InnoDB: Starting shutdown...
    InnoDB: Shutdown completed; log sequence number 9293846
    170223 13:39:31 completed OK!
    ```

Now the files in `/data/compressed/` are ready to be used by the server.

The next step is  to [restore](restore-a-backup.md) the backup. 

