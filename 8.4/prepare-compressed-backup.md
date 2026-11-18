> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-xtrabackup/8.4/llms.txt).

# Decompress and prepare a backup

Before you can prepare the backup you need to decompress all the files. Run the following commands as root or use the sudo command.

## Decompress a backup

- To decompress backups made using `LZ4` or `ZSTD` compression algorithm, install the corresponding package.

  `Install on APT systems`

  **Install the lz4 package**

  ```
  sudo apt install lz4
  ```

  **Install the zstd package**

  ```
  sudo apt install zstd
  ```

  `Install on YUM systems`

  **Install the lz4 package**

  ```
  sudo yum install lz4
  ```

  **Install the zstd package**

  ```
  sudo yum install zstd
  ```

- Use the `--decompress` option to decompress the backup.

  ```
  xtrabackup --decompress --target-dir=/data/compressed/
  ```

  Note

  `--parallel` can be used with `--decompress` option to decompress multiple files simultaneously.

  Percona XtraBackup does not automatically delete compressed files. To clean up the backup directory, use the `--remove-original` option. If you do not remove the compressed files, these files will not be copied or moved to the datadir when using the `--copy-back` or `--move-back` options.

## Prepare the backup

When the files are decompressed you can prepare the backup with the `--prepare` option.

```
xtrabackup --prepare --target-dir=/data/compressed/
```

Confirmation message

```
...
2026-10-13T17:15:23.335977-00:00 0 [Note] [MY-012980] [InnoDB] Shutdown completed; log sequence number 38173718
2026-10-13T17:15:23.343329-00:00 0 [Note] [MY-011825] [Xtrabackup] completed OK!
```

Now the files in `/data/compressed/` are ready to be used by the server.

## Next step

[Restore the backup](https://docs.percona.com/percona-xtrabackup/8.4/restore-a-backup.html)
