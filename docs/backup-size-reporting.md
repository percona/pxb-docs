# Backup size reporting

## Overview

Percona XtraBackup reports the size of every successful backup in `xtrabackup_info` and reports the same values in the XtraBackup error log.

Backup size reporting helps estimate storage requirements, check that backups work correctly, and plan restores for compressed and streamed backups.

## Why external tools cannot accurately measure backup size

External tools cannot reliably determine the final size of XtraBackup output in many backup configurations.

Backup size often differs from the MySQL datadir size because Percona XtraBackup also copies redo log data generated during the backup process.

Several backup features further change the final output size:

* [`--stream=xbstream`](binaries-overview.md#xbstream) adds xbstream metadata

* [`--compress`](create-compressed-backup.md) reduces the final backup size according to data compressibility

* Sparse InnoDB tablespaces affect filesystem size reporting

* Streaming and cloud uploads may not produce local backup files for measurement

* Compression, encryption, and streaming pipelines prevent external tools from accurately calculating final backup size

Compressed backups also require sufficient free space during decompression and restore. Reporting the uncompressed backup size helps estimate restore storage requirements before recovery operations begin.

## How backup size reporting works

Percona XtraBackup records backup size at the end of every successful backup. Backup size reporting is enabled by default and requires no additional configuration.

Percona XtraBackup calculates backup size after all backup operations complete, including:

* Compression

* Encryption

* xbstream formatting

* Sparse file handling

For sparse InnoDB tablespaces, Percona XtraBackup counts only written data fragments and excludes filesystem hole ranges.

The reported backup size matches the exact number of bytes written to the backup destination.

Compressed backups additionally report:

* `uncompressed_backup_size`

* Compression ratio

Percona XtraBackup calculates `uncompressed_backup_size` separately from the final compressed backup size so that the reported value reflects the logical backup size before compression.

Percona XtraBackup stores the reported values in:
Expand commentComment on line R60Resolved
* `xtrabackup_info`

* XtraBackup error log

### Reported values

| Field | Description |
|---|---|
| `backup_size` | Final backup output size in bytes |
| `uncompressed_backup_size` | Total uncompressed logical backup size in bytes |
| Compression ratio | Ratio between `uncompressed_backup_size` and `backup_size` reported in the XtraBackup error log |

### `xtrabackup_info`

Percona XtraBackup writes backup size metadata to `xtrabackup_info` in the backup output.

Depending on backup configuration, `xtrabackup_info` in the backup output may be:

* Plaintext

* Compressed

* Encrypted

* Embedded inside an xbstream archive

Streamed backups store `xtrabackup_info` inside the xbstream output.

If `xtrabackup_info` is not plaintext, you can create a separate plaintext copy of `xtrabackup_info` using the `--extra-lsndir=<dir>` option.

!!! note

    Files created in the `--extra-lsndir=<dir>` directory are not part of the backup.

### XtraBackup error log

Percona XtraBackup prints information about backup size near the end of the backup operation before the `completed OK!` message.

The log output includes:

* Human-readable size

* Exact byte count

* Compression ratio

## Output

### Uncompressed backup example

The following example shows `xtrabackup_info` from a backup created with `--target-dir`.

```text
uuid = 122a291d-48b0-11f1-9d76-047bcbcb6b7e
name =
tool_name = xtrabackup
tool_command = --backup --no-defaults --user=root --socket=/tmp/pxb-folder/mysql.sock --target-dir=/tmp/pxb-folder/backup --extra-lsndir=/tmp/pxb-folder/lsndir --datadir=/tmp/pxb-folder/datadir
tool_version = 8.4.0-6
ibbackup_version = 8.4.0-6
server_version = 8.4.8-8
server_flavor = Percona Server (GPL), Release 8, Revision 1c288264
start_time = 2026-05-05 19:27:26
end_time = 2026-05-05 19:27:28
lock_time = 0
binlog_pos = filename 'binlog.000002', position '158'
innodb_from_lsn = 0
innodb_to_lsn = 24785178
partial = N
incremental = N
format = file
compressed = N
encrypted = N
lock_ddl_type = ON
backup_size = 88689086
```

The XtraBackup error log contains the corresponding backup size entry:

```text
2026-05-05T19:27:28.140024+01:00 0 [Note] [MY-011825] [Xtrabackup] Backup size: 84.58 MiB (88689086 bytes)
2026-05-05T19:27:29.382428+01:00 0 [Note] [MY-011825] [Xtrabackup] completed OK!
```

### Compressed backup example

Compressed backups additionally report the uncompressed backup size and compression ratio.

The following example shows the final lines of `xtrabackup_info` with backup size values reported in bytes:

```text
backup_size = 1832398
uncompressed_backup_size = 88689148
```

The XtraBackup error log contains the corresponding output:

```text
2026-05-05T19:27:42.851038+01:00 0 [Note] [MY-011825] [Xtrabackup] Backup size: 1.75 MiB (1832398 bytes)
2026-05-05T19:27:42.851055+01:00 0 [Note] [MY-011825] [Xtrabackup] Uncompressed backup size: 84.58 MiB (88689148 bytes)
2026-05-05T19:27:42.851065+01:00 0 [Note] [MY-011825] [Xtrabackup] Compression ratio: 48.40x
```

Percona XtraBackup calculates the compression ratio as:

```text
uncompressed_backup_size / backup_size
```
