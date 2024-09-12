# Decompress and prepare a backup

Before you can prepare the backup you need to decompress all the files.

## Decompress a backup

* To decompress backups made using `LZ4` or `ZSTD` compression algorithm, install the corresponding package for your package management system.

    `Install on APT systems`

    === "Install the `lz4` package"

        ```{.bash data-prompt="$"}
        $ sudo apt install lz4
        ```

    === "Install the `zstd` package"

        ```{.bash data-prompt="$"}
        $ sudo apt install zstd
        ```

    `Install on YUM systems`
    
    === "Install the `lz4` package"

        ```{.bash data-prompt="$"}
        $ sudo yum install lz4
        ```

    === "Install the `zstd` package"

        ```{.bash data-prompt="$"}
        $ sudo yum install zstd
        ```


*  Use the `--decompress` option to decompress the backup.

    ```{.bash data-prompt="$"}
    $ xtrabackup --decompress --target-dir=/data/compressed/
    ```

    !!! note
   
        `--parallel` can be used with `--decompress` option to decompress multiple files simultaneously. 

    Percona XtraBackup does not automatically delete compressed files. To clean up the backup directory, use the `--remove-original` option. If you do not remove the compressed files, these files will not be copied or moved to the datadir when using the `--copy-back` or `--move-back` options.

## Prepare the backup

When the files are decompressed you can prepare the backup with the `--prepare` option.

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

The next step is to [Restore a backup](restore-a-backup.md). 

