# Create a compressed backup

Percona XtraBackup supports compressed backups. To make a compressed backup, use the `--compress` option along
with the `--backup` and `--target-dir` options. A local or streaming backup can be compressed or decompressed with [xbstream](xbstream-binary-overview.md).

By default, the `--compress` option uses the `zstandard` tool that you can install with
the `percona-release` package configuration tool as follows:

```{.bash data-prompt="$"}
$ sudo percona-release enable tools
$ sudo apt update
$ sudo apt install zstandard
```

!!! note
   
    Enable the repository: `percona-release enable-only tools release`.

If Percona XtraBackup is intended to be used in combination with
the upstream MySQL Server, you only need to enable the `tools`
repository: `percona-release enable-only tools`.

Percona XtraBackup supports the following compression algorithms:

`Zstandard (ZSTD)`

The Zstandard (ZSTD) is a fast lossless compression algorithm that targets real-time compression scenarios and better compression ratios. `ZSTD` is the default compression algorithm for the `--compress` option.

To compress files using the `ZSTD` compression algorithm, use the `--compress` option:

```{.bash data-prompt="$"}
$ xtrabackup --backup --compress --target-dir=/data/backup
```

The resulting files have the `\*.zst` format.
   
You can specify `ZSTD` compression level with the [`--compress-zstd-level(=#)`](xtrabackup-option-reference.md#compress-zstd-level) option. The default value is `1`.

```{.bash data-prompt="$"}
$ xtrabackup –backup –compress –compress-zstd-level=1 –target-dir=/data/backup
```

`lz4`

To compress files using the `lz4` compression algorithm, set the `--compress` option to `lz4`:

```{.bash data-prompt="$"}
$ xtrabackup --backup --compress=lz4 --target-dir=/data/backup
```

The resulting files have the `\*.lz4` format. 

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

The next step is to [prepare](prepare-compressed-backup.md) the backup in order to [restore](restore-a-backup.md) it. 


