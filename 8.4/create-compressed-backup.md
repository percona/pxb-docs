> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-xtrabackup/8.4/llms.txt).

# Create a compressed backup

Percona XtraBackup supports compressed backups. To make a compressed backup, use the `--compress` option along with the `--backup` and `--target-dir` options. A local or streaming backup can be compressed or decompressed with [xbstream](https://docs.percona.com/percona-xtrabackup/8.4/xbstream-binary-overview.html).

Run the following commands as root or use the sudo command.

By default, the `--compress` option uses the `zstandard` tool that you can install with the `percona-release` package configuration tool as follows:

```
sudo percona-release enable tools
sudo apt update
sudo apt install zstandard
```

Note

Enable the repository: `percona-release enable-only tools release`.

If Percona XtraBackup is intended to be used in combination with the upstream MySQL Server, you only need to enable the `tools` repository: `percona-release enable-only tools`.

Percona XtraBackup supports the following compression algorithms:

## Zstandard (ZSTD)

The Zstandard (ZSTD) is a fast lossless compression algorithm that targets real-time compression scenarios and better compression ratios. `ZSTD` is the default compression algorithm for the `--compress` option.

To compress files using the `ZSTD` compression algorithm, use the `--compress` option:

```
xtrabackup --backup --compress --target-dir=/data/backup
```

The resulting files have the `\*.zst` format.

You can specify `ZSTD` compression level with the [`--compress-zstd-level(=#)`](https://docs.percona.com/percona-xtrabackup/8.4/xtrabackup-option-reference.html#compress-zstd-level) option. The default value is `1`.

```
xtrabackup –backup –compress –compress-zstd-level=1 –target-dir=/data/backup
```

## lz4

To compress files using the `lz4` compression algorithm, set the `--compress` option to `lz4`:

```
xtrabackup --backup --compress=lz4 --target-dir=/data/backup
```

The resulting files have the `\*.lz4` format.

If you want to speed up the compression you can use the parallel compression, which can be enabled with `--compress-threads` option. Following example will use four threads for compression:

```
xtrabackup --backup --compress --compress-threads=4 \
--target-dir=/data/compressed/
```

Expected output

```
...
2026-10-13T17:15:05.557481-00:00 2 [Note] [MY-011825] [Xtrabackup] space_id: 2, Compressing ./test/t1.ibd to /data/compressed/test/t1.ibd.zst, size 11534336 (11.00 MiB)
2026-10-13T17:15:05.575040-00:00 2 [Note] [MY-011825] [Xtrabackup] space_id: 2, Done: Compressing ./test/t1.ibd to /data/compressed/test/t1.ibd.zst
...
2026-10-13T17:15:06.622555-00:00 0 [Note] [MY-011825] [Xtrabackup] Compression ratio: 21.73x
2026-10-13T17:15:07.624119-00:00 0 [Note] [MY-011825] [Xtrabackup] Transaction log of lsn (38173174) to (38173210) was copied.
2026-10-13T17:15:07.853292-00:00 0 [Note] [MY-011825] [Xtrabackup] completed OK!
```

## Next step

[Prepare the backup](https://docs.percona.com/percona-xtrabackup/8.4/prepare-compressed-backup.html)
