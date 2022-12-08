# Compressed backup

*Percona XtraBackup* supports compressed backups. A local or streaming
backup can be compressed or decompressed with *xbstream*.

## Create compressed backups

To make a compressed backup, use the `--compress` option along
with the `--backup` and `--target-dir` options. 

The `--compress` option uses the `qpress` tool that you can install with
the `percona-release` package configuration tool as follows:

```{.bash data-prompt="$"}
$ sudo percona-release enable tools
$ sudo apt update
$ sudo apt install qpress
```

!!! note
   
    Enable the repository: `percona-release enable-only tools release`.

If *Percona XtraBackup* is intended to be used in combination with
the upstream MySQL Server, you only need to enable the `tools`
repository: `percona-release enable-only tools`.

Percona XtraBackup supports the following compression algorithms:

`quicklz`
    
To compress files using the `quicklz` compression algorithm, use `--compress` option:

    ```{.bash data-prompt="$"}
    $ xtrabackup --backup --compress --target-dir=/data/backup
    ```

`lz4`

To compress files using the `lz4` compression algorithm, set `--compress` option to `lz4`:

    ```{.bash data-prompt="$"}
    $ xtrabackup --backup --compress=lz4 --target-dir=/data/backup
    ```

`Zstandard (ZSTD)`

The Zstandard (ZSTD) compression algorithm is a [tech preview](../glossary.md#tech-preview) feature. Before using ZSTD in production, we recommend that you test restoring production from physical backups in your environment, and also use the alternative backup method for redundancy.

[Percona XtraBackup 8.0.30-23](../release-notes/8.0/8.0.30-23.0.md) adds support for the `Zstandard (ZSTD)` compression algorithm. `ZSTD` is a fast lossless compression algorithm that targets real-time compression scenarios and better compression ratios. 
    
To compress files using the `ZSTD` compression algorithm, set `--compress` option to `zstd`:

    ```{.bash data-prompt="$"}
    $ xtrabackup --backup --compress=zstd --target-dir=/data/backup
    ```
   
You can specify `ZSTD` compression level with the [`--compress-zstd-level(=#)`](../xtrabackup_bin/xbk_option_reference.md#compress-zstd-level) option. The default value is `1`.

    ```{.bash data-prompt="$"}
    $ xtrabackup --backup --compress-zstd-level=1 --target-dir=/data/backup
    ```

If you want to speed up the compression you can use the parallel
compression, which can be enabled with `--compress-threads` option.
Following example will use four threads for compression:

```{.bash data-prompt="$"}
$ xtrabackup --backup --compress --compress-threads=4 \
--target-dir=/data/compressed/
```

??? example "Expected output"

    ```{.text .no-copy}
    ...
    170223 13:00:38 [01] Compressing ./test/sbtest1.frm to /tmp/compressed/test/sbtest1.frm.qp
    170223 13:00:38 [01]        ...done
    170223 13:00:38 [01] Compressing ./test/sbtest2.frm to /tmp/compressed/test/sbtest2.frm.qp
    170223 13:00:38 [01]        ...done
    ...
    170223 13:00:39 [00] Compressing xtrabackup_info
    170223 13:00:39 [00]        ...done
    xtrabackup: Transaction log of lsn (9291934) to (9291934) was copied.
    170223 13:00:39 completed OK!
    ```

### Prepare the backup

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

### Restore the backup

*xtrabackup* has a `--copy-back` option, which performs the restoration of a backup to the server’s datadir:

```{.bash data-prompt="$"}
$ xtrabackup --copy-back --target-dir=/data/backups/
```

It will copy all the data-related files back to the server’s datadir,
determined by the server’s `my.cnf` configuration file. You should check
the last line of the output for a success message:

??? example "Expected output"

    ```{.text .no-copy}
    170223 13:49:13 completed OK!
    ```

You should check the file permissions after copying the data back. You may need to adjust them with something like:

```{.bash data-prompt="$"}
$ chown -R mysql:mysql /var/lib/mysql
```

Now that the datadir contains the restored data. You are ready to start the server.

