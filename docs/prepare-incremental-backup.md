# Prepare an incremental backup

Preparing an incremental backup combines a full backup with one or more incremental backups to create a consistent backup that you can restore.

An incremental backup contains the changes made after its base backup. When you create multiple incremental backups as a chain, each backup represents a later state of the database.

For example, you could have the following backups:

```text
/data/backups/base
/data/backups/inc1
/data/backups/inc2
```

These backups form the following chain:

```text
base → inc1 → inc2
```

In this example:

* `/data/backups/base` is the full backup.
* `/data/backups/inc1` is the first incremental backup.
* `/data/backups/inc2` is the final incremental backup.

During the prepare process, Percona XtraBackup applies each incremental backup to the full backup in order. Each step updates the files in `/data/backups/base` and moves the state of the full backup forward to the point when that incremental backup was created. The final prepared backup remains in `/data/backups/base`.

The `--prepare` step for incremental backups differs from the prepare step for full backups. When preparing a full backup, Percona XtraBackup applies committed transactions from the redo log to the data files and rolls back uncommitted transactions to make the backup consistent.

When preparing an incremental chain, you must delay the rollback of uncommitted transactions until you apply the final incremental backup. A transaction that was uncommitted when one backup was created might be committed in a later incremental backup.

Use `--apply-log-only` to apply redo without rolling back uncommitted transactions.

!!! warning

    If you do not use the `--apply-log-only` option to prevent the rollback phase, then your incremental backups are unusable. After transactions have been rolled back, further incremental backups cannot be applied.

Prepare an incremental backup chain in the following order:

1. Prepare the full backup with `--apply-log-only`.
2. Apply each intermediate incremental backup in order with `--apply-log-only`.
3. Apply the final incremental backup without `--apply-log-only`.

## Prepare the full backup

Start by preparing the full backup with `--apply-log-only` to prevent the rollback phase:

```shell
xtrabackup --prepare --apply-log-only --target-dir=/data/backups/base
```

The log sequence number (LSN) identifies a point in the database redo log. Incremental backups use LSNs to identify which changes occurred after the base backup.

The log sequence number in the output should match the `to_lsn` value of the base backup. The output should end with text similar to the following:

??? example "Expected output"

    ```text
    InnoDB: Shutdown completed; log sequence number 1626007
    161011 12:41:04 completed OK!
    ```

!!! warning

    This backup is actually safe to restore as-is now, even though the rollback phase has been skipped. If you restore the backup and start the server, InnoDB detects that the rollback phase was not performed, and completes the rollback in the background, as InnoDB usually does for a crash recovery. InnoDB notifies you that the database was not shut down normally.

## Apply incremental backups

Apply incremental backups to the prepared full backup in the same order in which you created them.

For the example chain, apply `inc1` first and `inc2` last:

```text
base → inc1 → inc2
```

Percona XtraBackup applies the changes from each incremental backup to `/data/backups/base`. The incremental directories contain the changes to apply, but the resulting prepared backup remains in the full backup directory.

### Apply the first incremental backup

Apply the first incremental backup to the full backup:

```shell
xtrabackup --prepare --apply-log-only --target-dir=/data/backups/base \
--incremental-dir=/data/backups/inc1
```

`--target-dir` points to the full backup that you are preparing. `--incremental-dir` points to the incremental backup whose changes you want to apply.

The command applies the delta files from `/data/backups/inc1` to the files in `/data/backups/base`, moving the full backup forward to the state of the first incremental backup. Percona XtraBackup then applies the redo log.

Because another incremental backup follows `inc1`, use `--apply-log-only` to prevent the rollback phase.

The final data remains in `/data/backups/base`, not in the incremental directory.

You should see output similar to the following:

??? example "Expected output"

    ```text
    incremental backup from 1626007 is enabled.
    xtrabackup: cd to /data/backups/base
    xtrabackup: This target seems to be already prepared with --apply-log-only.
    xtrabackup: xtrabackup_logfile detected: size=2097152, start_lsn=(4124244)
    ...
    xtrabackup: page size for /tmp/backups/inc1/ibdata1.delta is 16384 bytes
    Applying /tmp/backups/inc1/ibdata1.delta to ./ibdata1...
    ...
    161011 12:45:56 completed OK!
    ```

The LSN should match the LSN from the first incremental backup. At this point, `/data/backups/base` contains the state of the database as of the first incremental backup.

### Apply the final incremental backup

Percona XtraBackup does not support using the same incremental backup directory to prepare two copies of a backup. Do not run `--prepare` with the same incremental backup directory (the value of `--incremental-dir`) more than once.

After applying `/data/backups/inc1`, apply `/data/backups/inc2` to the same base backup.

In this example, `inc2` is the final incremental backup. Apply it without `--apply-log-only`:

```shell
xtrabackup --prepare --target-dir=/data/backups/base \
--incremental-dir=/data/backups/inc2
```

The command applies the changes from `inc2` to `/data/backups/base` and completes the prepare process.

!!! note

    Use `--apply-log-only` when merging the incremental backups except for the last one. This is why the previous command does not include the `--apply-log-only` option. If `--apply-log-only` is used on the last step, backup remains consistent but the server performs the rollback phase.

After you apply the final incremental backup, `/data/backups/base` contains the prepared backup with all changes through `inc2`.

If your backup chain contains more incremental backups, apply them in order. Use `--apply-log-only` for every intermediate incremental backup and omit it only when applying the final incremental backup.

For example:

```text
base    → --apply-log-only
inc1    → --apply-log-only
inc2    → --apply-log-only
inc3    → final incremental, no --apply-log-only
```

## Speed up the prepare step with --parallel

For incremental backups with many InnoDB Data (IBD) files, you can significantly reduce prepare time by using the `--parallel` option. The `--parallel` option enables the concurrent processing of multiple delta files, thereby maximizing storage bandwidth. The `--parallel` option is especially beneficial when there are many IBD files, even if the IBD files didn't change between backups, as empty delta files are processed quickly in parallel. 

Using `--parallel=X` has effect on the prepare phase. It will use X threads to apply the changes from `.delta` files to the IBD files. When using `--parallel` in the prepare phase, always specify a numeric value. The recommended minimum value is 4 (for example, `--parallel=4`). Note that each thread operates on a single file. If you have a large delta file, there is still only one thread that processes that `.delta` file. Parallelization occurs at the file level, not within individual files.

To apply an intermediate incremental backup with four worker threads, run:

```shell
xtrabackup --prepare --parallel=4 --apply-log-only --target-dir=/data/backups/base \
--incremental-dir=/data/backups/inc1
```

You can also use `--parallel` when applying the final incremental backup. Omit `--apply-log-only` for the final step:

```shell
xtrabackup --prepare --parallel=4 --target-dir=/data/backups/base \
--incremental-dir=/data/backups/inc2
```

## Next step

[Restore the backup](restore-a-backup.md){.md-button}
