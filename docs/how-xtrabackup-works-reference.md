# Backup lifecycle reference

Quick-scan facts for privileges, phases, defaults, and behavior. For internals, see [Percona XtraBackup internals](how-xtrabackup-works-explanation.md). For commands and flags, see [How to run a backup lifecycle](how-xtrabackup-works-how-to.md).

## What privileges does PXB require?

Percona XtraBackup (PXB) typically needs the privileges in the following table:

| Privilege | Typical use |
|-----------|-------------|
| `BACKUP_ADMIN` | Read `performance_schema.log_status`. Use `LOCK INSTANCE FOR BACKUP` or `LOCK TABLES FOR BACKUP`. |
| `RELOAD` | Run `FLUSH NO_WRITE_TO_BINLOG BINARY LOGS` at final sync. Run `FLUSH TABLES WITH READ LOCK` when backup locks are unavailable. |
| `LOCK TABLES` | Issue table-level locks in some workflows. |
| `REPLICATION CLIENT` | Use `--slave-info` and related replication metadata. |

[Connection and privileges needed](privileges.md) has the full list.

## What are the three operator-facing phases?

| Step | Phase | What happens |
|------|-------|----------------|
| 1 | Backup (hot copy) | Copy data files. Copy redo for the whole run. |
| 2 | Prepare | Replay redo. Roll back uncommitted work. |
| 3 | Restore | Run `--copy-back` or `--move-back` into `datadir`. |

## What are the in-backup sub-phases?

Final sync is the same in both modes. PXB runs `FLUSH NO_WRITE_TO_BINLOG BINARY LOGS`. PXB reads `performance_schema.log_status`. PXB stops the redo thread and releases locks. With `--lock-ddl=ON` (default), the backup lock is held from backup start through final sync.

| # | `--lock-ddl=ON` | `--lock-ddl=REDUCED` |
|---|-----------------|----------------------|
| 1 | Backup lock: copy InnoDB files and redo | No backup lock: copy InnoDB files and redo |
| 2 | Backup lock: copy non-InnoDB files | Backup lock: copy non-InnoDB files. Recopy DDL-affected tablespaces. |
| 3 | Backup lock: final sync, then release | Backup lock: final sync, then release |

Compare backup locks with `FLUSH TABLES WITH READ LOCK` (FTWRL): [Percona Server backup locks](https://docs.percona.com/percona-server/innovation-release/backup-locks.html).  
MySQL {{vers}}: [`LOCK INSTANCE FOR BACKUP`](https://dev.mysql.com/doc/refman/{{vers}}/en/lock-instance-for-backup.html).

## What are the `--lock-ddl` values?

| Value | When the backup lock is taken (typical) |
|-------|----------------------------------------|
| `ON` (default) | Backup start |
| `REDUCED` | After InnoDB data copy finishes |

`ON` blocks data definition language (DDL) for the whole window from the beginning. `REDUCED` delays the block until InnoDB is copied. InnoDB data manipulation language (DML) keeps running through the main copy under both modes.

## What does `--register-redo-log-consumer` do?

| Field | Detail |
|-------|--------|
| Default | Off |
| Does | Registers PXB as a redo consumer. The server retains a redo file until PXB copies that file. |
| Cost | Redo can pile up. Disk use may spike. |
| Writes | Server may pause writes briefly while the consumer advances. |

## What prepare options affect performance?

| Option | Notes |
|--------|--------|
| `--use-memory` | Random-access memory (RAM) for prepare only (default 100 MB). Larger values often help. |
| `--parallel` | 8.4.0-3 and later: parallel `.delta` apply for incrementals. Not parallel full-backup redo replay. |

Full flags: [xtrabackup option reference](xtrabackup-option-reference.md).

## What does restore copy back?

Restore reads paths from `my.cnf`. Paths include `datadir`, `innodb_data_home_dir`, `innodb_data_file_path`, and `innodb_log_group_home_dir`.

Restore places files in the following order:

* Undo and system tablespaces, then binary logs, then remaining files in parallel (`.ibd`, non-InnoDB tables, `#innodb_redo`), then MyRocks when present.

* File attributes are preserved.

* A successful backup prints binlog coordinates to standard error (STDERR). Redirect STDERR when the workflow must capture coordinates.

## When are backup locks skipped?

Locks stay off only if every table in every schema uses InnoDB. The check includes `mysql`. Commonly `mysql` still holds CSV or MyISAM tables, such as `general_log`. PXB takes backup locks in most installations.

| Server | Notes |
|--------|--------|
| Percona Server for MySQL {{vers}} | `log_status` may carry relay coordinates. `--slave-info` can skip extra locks. |
| Standard MySQL {{vers}} | May need `FLUSH TABLES WITH READ LOCK` with `--slave-info` when relay position is required. |

## How do cloud and streaming backups differ?

Cloud and streaming backups use the same phases. Slow networks extend final sync and can lengthen the backup lock window. See [Take a streaming backup](take-streaming-backup.md) and [xbcloud binary overview](xbcloud-binary-overview.md).

## See also

* [Index of files created by Percona XtraBackup](xtrabackup-files.md)

* [Restore full, incremental, and compressed backups](restore-a-backup.md)

* [Create a full backup](create-full-backup.md)
