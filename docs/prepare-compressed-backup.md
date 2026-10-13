# Decompress and prepare a backup

Before you can prepare the backup you need to decompress all the files. Run the following commands as root or use the sudo command.

## Decompress a backup

* To decompress backups made using `LZ4` or `ZSTD` compression algorithm, install the corresponding package.

    `Install on APT systems`

    === "Install the `lz4` package"

        ```shell
        sudo apt install lz4
        ```

    === "Install the `zstd` package"

        ```shell
        sudo apt install zstd
        ```

    `Install on YUM systems`
    
    === "Install the `lz4` package"

        ```shell
        sudo yum install lz4
        ```

    === "Install the `zstd` package"

        ```shell
        sudo yum install zstd
        ```

*  Use the `--decompress` option to decompress the backup.

    ```shell
    xtrabackup --decompress --target-dir=/data/compressed/
    ```

    !!! note
   
        `--parallel` can be used with `--decompress` option to decompress multiple files simultaneously. 

    Percona XtraBackup does not automatically delete compressed files. To clean up the backup directory, use the `--remove-original` option. If you do not remove the compressed files, these files will not be copied or moved to the datadir when using the `--copy-back` or `--move-back` options.

## Prepare the backup

When the files are decompressed you can prepare the backup with the `--prepare` option.

```shell
xtrabackup --prepare --target-dir=/data/compressed/
```

??? example "Confirmation message"

    ```{.text .no-copy}
    ...
    2026-10-13T17:25:02.032550-00:00 0 [Note] [MY-012980] [InnoDB] Shutdown completed; log sequence number 38309910
    2026-10-13T17:25:02.039421-00:00 0 [Note] [MY-011825] [Xtrabackup] completed OK!
    ```

Now the files in `/data/compressed/` are ready to be used by the server.

## Next step

[Restore the backup](restore-a-backup.md){.md-button}

