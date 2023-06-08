# Create a compressed backup

Percona XtraBackup supports compressed backups. A local or streaming
backup can be compressed or decompressed with *xbstream*.

!!! note

    Starting with Percona XtraBackup 8.0.31-24 using qpress/QuickLZ to compress backups is deprecated and may be removed in future versions. We recommend using either `LZ4` or Zstandard (`ZSTD`) compression algorithms.

To make a compressed backup, use the `--compress` option along
with the `--backup` and `--target-dir` options. 

By default, the `--compress` option uses the `qpress` tool that you can install with
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

The Zstandard (ZSTD) compression algorithm is a [tech preview](glossary.md#tech-preview) feature. Before using ZSTD in production, we recommend that you test restoring production from physical backups in your environment, and also use the alternative backup method for redundancy.

[Percona XtraBackup 8.0.30-23](release-notes/8.0/8.0.30-23.0.md) adds support for the `Zstandard (ZSTD)` compression algorithm. `ZSTD` is a fast lossless compression algorithm that targets real-time compression scenarios and better compression ratios. 
    
To compress files using the `ZSTD` compression algorithm, set `--compress` option to `zstd`:

```{.bash data-prompt="$"}
$ xtrabackup --backup --compress=zstd --target-dir=/data/backup
```
   
You can specify `ZSTD` compression level with the [`--compress-zstd-level(=#)`](xtrabackup-option-reference.md#compress-zstd-level) option. The default value is `1`.

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

The next step is to [prepare](prepare-compressed-backup.md) the backup in order to [restore](restore-a-backup.md) it. 


