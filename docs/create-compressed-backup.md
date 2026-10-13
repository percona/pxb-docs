# Create a compressed backup

Percona XtraBackup supports compressed backups. To make a compressed backup, use the `--compress` option along
with the `--backup` and `--target-dir` options. A local or streaming backup can be compressed or decompressed with [xbstream](xbstream-binary-overview.md).

Run the following commands as root or use the sudo command.

By default, the `--compress` option uses the `zstandard` tool that you can install with
the `percona-release` package configuration tool as follows:

```shell
sudo percona-release enable tools
sudo apt update
sudo apt install zstandard
```

!!! note
   
    Enable the repository: `percona-release enable-only tools release`.

If Percona XtraBackup is intended to be used in combination with
the upstream MySQL Server, you only need to enable the `tools`
repository: `percona-release enable-only tools`.

Percona XtraBackup supports the following compression algorithms:

## Zstandard (ZSTD)

The Zstandard (ZSTD) is a fast lossless compression algorithm that targets real-time compression scenarios and better compression ratios. `ZSTD` is the default compression algorithm for the `--compress` option.

To compress files using the `ZSTD` compression algorithm, use the `--compress` option:

```shell
xtrabackup --backup --compress --target-dir=/data/backup
```

The resulting files have the `\*.zst` format.
   
You can specify `ZSTD` compression level with the [`--compress-zstd-level(=#)`](xtrabackup-option-reference.md#compress-zstd-level) option. The default value is `1`.

```shell
xtrabackup –backup –compress –compress-zstd-level=1 –target-dir=/data/backup
```

## lz4

To compress files using the `lz4` compression algorithm, set the `--compress` option to `lz4`:

```shell
xtrabackup --backup --compress=lz4 --target-dir=/data/backup
```

The resulting files have the `\*.lz4` format. 

If you want to speed up the compression you can use the parallel
compression, which can be enabled with `--compress-threads` option.
Following example will use four threads for compression:

```shell
xtrabackup --backup --compress --compress-threads=4 \
--target-dir=/data/compressed/
```

??? example "Expected output"

    ```{.text .no-copy}
    ...
    2026-10-13T17:24:45.357945-00:00 2 [Note] [MY-011825] [Xtrabackup] Compressing file with space_id 2 ./test/t1.ibd to /data/compressed/test/t1.ibd.zst
    2026-10-13T17:24:45.376746-00:00 2 [Note] [MY-011825] [Xtrabackup] Done: Compressing file with space_id 2 ./test/t1.ibd to /data/compressed/test/t1.ibd.zst
    ...
    2026-10-13T17:24:46.558442-00:00 0 [Note] [MY-011825] [Xtrabackup] Compression ratio: 21.25x
    2026-10-13T17:24:47.563990-00:00 0 [Note] [MY-011825] [Xtrabackup] Transaction log of lsn (38309754) to (38309774) was copied.
    2026-10-13T17:24:47.796682-00:00 0 [Note] [MY-011825] [Xtrabackup] completed OK!
    ```

## Next step

[Prepare the backup](prepare-compressed-backup.md){.md-button}

