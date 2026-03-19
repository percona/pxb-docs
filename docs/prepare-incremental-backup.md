# Prepare an incremental backup

The `--prepare` step for incremental backups differs from full backups. For full backups, committed transactions are replayed from the log file to the data files, and uncommitted transactions are rolled back to ensure consistency. When preparing an incremental backup, you must skip the rollback of uncommitted transactions, as these may still be in progress and could be committed in a subsequent incremental backup. Use the `--apply-log-only` option when preparing the first full backup to prevent the rollback phase from occurring.

!!! warning
   
    If you do not use the `--apply-log-only` option to prevent the rollback phase, then your incremental backups are unusable. After transactions have been rolled back, further incremental backups cannot be applied.
  
Start by preparing the full backup, then apply the incremental differences to that backup.  

For example, you could have the following backups:

```text
/data/backups/base
/data/backups/inc1
/data/backups/inc2
```

To prepare the base backup, you need to run `--prepare` as
usual, but prevent the rollback phase:

```shell
xtrabackup --prepare --apply-log-only --target-dir=/data/backups/base
```

The log sequence number should match the `to_lsn` of the base backup The output should end with text similar to the following:

??? example "Expected output"

    ```{.text .no-copy}
    InnoDB: Shutdown completed; log sequence number 1626007
    161011 12:41:04 completed OK!
    ```

!!! warning
   
    This backup is actually safe to restore as-is now, even though the rollback phase has been skipped. If you restore the backup and start the server, InnoDB detects that the rollback phase was not performed, and completes the rollback in the background, as InnoDB usually does for a crash recovery. InnoDB notifies you that the database was not shut down normally.

To apply the first incremental backup to the full backup, run the following command:

```shell
xtrabackup --prepare --apply-log-only --target-dir=/data/backups/base \
--incremental-dir=/data/backups/inc1
```

This command applies the delta files to the files in `/data/backups/base`, which
rolls them forward in time to the time of the incremental backup. The redo log is then applied as usual. The final data is in
`/data/backups/base`, not in the incremental directory.

You should see an output similar to:

??? example "Expected output"

    ```{.text .no-copy}
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

Again, the LSN should match what you saw from your earlier inspection of
the first incremental backup. If you restore the files from
`/data/backups/base`, you should see the state of the database as of the first incremental backup.

### Faster prepare step with --parallel

For incremental backups with many InnoDB Data (IBD) files, you can significantly reduce prepare time by using the `--parallel` option. The `--parallel` option enables the concurrent processing of multiple delta files, thereby maximizing storage bandwidth. The `--parallel` option is especially beneficial when there are many IBD files, even if the IBD files didn't change between backups, as empty delta files are processed quickly in parallel. 

Using `--parallel=X` has effect on the prepare phase. It will use X threads to apply the changes from `.delta` files to the IBD files. When using `--parallel` in the prepare phase, always specify a numeric value. The recommended minimum value is 4 (for example, `--parallel=4`). Note that each thread operates on a single file. If you have a large delta file, there is still only one thread that processes that `.delta` file. Parallelization occurs at the file level, not within individual files.

An example command with the `--parallel` option:

```shell
xtrabackup --prepare --parallel=4 --apply-log-only --target-dir=/data/backups/base \
--incremental-dir=/data/backups/inc1
```

### Prepare a second incremental backup
   
Percona XtraBackup does not support using the same incremental backup directory to prepare two copies of backup. Do not run `--prepare` with the same incremental backup directory (the value of –incremental-dir) more than once.

Preparing the second incremental backup is a similar process: apply the deltas
to the (modified) base backup, and you will roll the base backup's data forward in time to the point of the second incremental backup:

```shell
xtrabackup --prepare --target-dir=/data/backups/base \
--incremental-dir=/data/backups/inc2
```

You can also use the `--parallel` option here to speed up the process:

```shell
xtrabackup --prepare --parallel=4 --target-dir=/data/backups/base \
--incremental-dir=/data/backups/inc2
```

!!! note
   
    Use `--apply-log-only` when merging the incremental backups except for the last one. This is why the previous command does not include the `--apply-log-only` option. If `--apply-log-only` is used on the last step, backup remains consistent but the server performs the rollback phase.

## Next step

[Restore the backup](restore-a-backup.md){.md-button}
