# How to run a backup lifecycle

Percona XtraBackup (PXB) runs three sequential phases: backup, prepare, and restore. Each section covers one phase and the operational flags that shape locking, redo retention, and recovery output.

Apply the following principles across every lifecycle phase:

* Grant only the privileges that the workflow requires.

* Run backup, prepare, and restore in sequence.

* Capture binary log coordinates for recovery and replication.

* Choose operational flags such as `--lock-ddl` and `--register-redo-log-consumer` to match the workload and lock tolerance.

## How do you grant the minimum privileges?

PXB needs database privileges that match the locking operations and metadata reads in the workflow.

Complete the following privilege steps:
{ .power-number }

1. Grant `BACKUP_ADMIN` so PXB can read `performance_schema.log_status`.

2. Confirm `BACKUP_ADMIN` allows PXB to take `LOCK INSTANCE FOR BACKUP` or `LOCK TABLES FOR BACKUP`.

3. Add `RELOAD`, `LOCK TABLES`, or `REPLICATION CLIENT` when the workflow needs extra capabilities. These include `FLUSH NO_WRITE_TO_BINLOG BINARY LOGS` at final sync, `FLUSH TABLES WITH READ LOCK`, and the `--slave-info` option.

For privilege lists and worked examples, see [Connection and privileges needed](privileges.md).

## How do you run a backup and capture binary log coordinates?

Capture binary log coordinates during the backup phase to support recovery and replica bootstrap.

Complete the following backup steps:
{ .power-number }

1. Run `xtrabackup` against the target directory with the standard options.

2. Redirect standard error (STDERR) to a log file. PXB writes binary log coordinates to STDERR. Example: `xtrabackup ... 2> backupout.log`.

3. Confirm the command returns exit code `0`.

For the artifact list a backup produces, see [Index of files created by Percona XtraBackup](xtrabackup-files.md).

## How do you choose a `--lock-ddl` mode?

PXB uses backup locks to copy non-InnoDB files without blocking InnoDB data manipulation language (DML). The server must support backup locks.

The following table compares the two `--lock-ddl` modes:

| Option | Effect |
|--------|--------|
| `--lock-ddl=ON` (default) | Takes the backup lock at start. DDL stays blocked for the full run unless the workflow changes. |
| `--lock-ddl=REDUCED` | Takes the lock after InnoDB is copied. DDL blocks for a shorter window. The mode accepts DDL contention during the InnoDB phase in exchange for a shorter DDL block. |

!!! warning

    Both modes block schema changes (DDL) for part of the backup window. Schedule DDL outside the backup, or accept the contention.

For a compact comparison, see [Backup lifecycle reference](how-xtrabackup-works-reference.md).

## When should you enable `--register-redo-log-consumer`?

Enable `--register-redo-log-consumer` when heavy write throughput risks purging redo before PXB finishes reading the redo stream. The flag prevents failures caused by missing redo.

Review the following checks before you enable the flag:

* Plan for redo bloat and possible disk exhaustion. The server retains redo longer.

* Monitor free space and I/O throughout the run.

* Abort the backup with Ctrl+C or `SIGTERM` to the `xtrabackup` process if disk space reaches a critical threshold. The consumer releases. The server purges redo. The operator can free space and retry.

The default value is `OFF`. Enable the flag only when spare disk space is available.

## How do you prepare the backup with `--prepare`?

The prepare phase applies redo and rolls back uncommitted transactions. The result is a consistent snapshot.

Complete the following prepare steps:
{ .power-number }

1. Run `xtrabackup --prepare` with `--target-dir` set to the backup directory.

2. For large or incremental backups, tune prepare performance with the following options:

    * Raise `--use-memory` to between 1 GB and 2 GB when random-access memory (RAM) allows. The default value is small.

    * Pass `--parallel` to apply `.delta` files in parallel on incremental backups. Parallel apply is available from 8.4.0-3. The flag does not parallelize first-pass redo on a full backup.

The following command shows a tuned prepare run:

```bash
xtrabackup --prepare --use-memory=2G --parallel=4 --target-dir=/data/backups/
```

!!! warning

    Leave RAM headroom for the OS and `mysqld` when prepare runs on the same host as production. Insufficient headroom triggers out-of-memory (OOM) kills.

For flag references, see [`--use-memory`](xtrabackup-option-reference.md#use-memory) and [`--parallel`](xtrabackup-option-reference.md#parallel).

## How do you restore with `--copy-back` or `--move-back`?

The restore phase places prepared backup files into the destination `datadir` for `mysqld` startup.

Complete the following restore steps:
{ .power-number }

1. Stop `mysqld` if the process owns the destination `datadir`.

2. Run `xtrabackup --copy-back` or `xtrabackup --move-back` with `--target-dir` set to the prepared backup. PXB reads destination paths from the configuration. Paths include `datadir`, InnoDB paths, and log paths.

3. Set ownership and permissions before starting `mysqld`. Example: `chown -R mysql:mysql /var/lib/mysql`. Backup files belong to the user that ran `xtrabackup`. The server expects the `mysql` user.

4. Start `mysqld`.

!!! warning

    `--move-back` destroys the original backup directory. The command moves files instead of copying them. Use `--move-back` only when disk space is constrained. Confirm a separate backup copy is available.

For full restore flows covering full, incremental, and compressed backups, see [Restore full, incremental, and compressed backups](restore-a-backup.md).

## How do you stream backups or upload to object storage?

Streaming backups and cloud uploads follow the same lifecycle as a local backup. Slow networks extend the final-sync phase. The extension keeps the backup lock held through the binary log flush and `log_status` read.

Plan streaming and upload runs with the following guidance:

* Run streaming backups inside a maintenance window.

* Size network bandwidth and destination throughput to keep the final-sync phase short.

* Confirm the destination object store accepts the backup payload size.

For workflow details, see the following references:

* [Take a streaming backup](take-streaming-backup.md)

* [xbcloud binary overview](xbcloud-binary-overview.md)

* [Percona XtraBackup internals](how-xtrabackup-works-explanation.md)
