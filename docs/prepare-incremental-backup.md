# Prepare an incremental backup

The `--prepare` step for incremental backups is not the same
as for full backups. In full backups, two types of operations are performed
to
make the database consistent: committed transactions are replayed from the
log
file against the data files, and uncommitted transactions are rolled back.
You
must skip the rollback of uncommitted transactions when preparing an
incremental backup, because transactions that were uncommitted at the time
of
your backup may be in progress, and it’s likely that they will be committed
in
the next incremental backup. You should use the
`--apply-log-only` option to prevent the rollback phase.

!!! warning
   
    If you do not use the `--apply-log-only` option to prevent the rollback phase, then your incremental backups will be useless. After transactions have been rolled back, further incremental backups cannot be applied.
 
Beginning with the full backup you created, you can prepare it, and then
apply
the incremental differences to it. Recall that you have the following
backups:

```
/data/backups/base
/data/backups/inc1
/data/backups/inc2
```

To prepare the base backup, you need to run `--prepare` as
usual, but prevent the rollback phase:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --apply-log-only --target-dir=/data/backups/base
```

The output should end with text similar to the following:

??? example "Expected output"

    ```{.text .no-copy}
    InnoDB: Shutdown completed; log sequence number 1626007
    161011 12:41:04 completed OK!
    ```

The log sequence number should match the `to_lsn` of the base backup, which
you saw previously.

!!! warning
   
    This backup is actually safe to restore as-is now, even though the rollback phase has been skipped. If you restore it and start MySQL, InnoDB will detect that the rollback phase was not performed, and it will do that in the background, as it usually does for a crash recovery upon start. It will notify you that the database was not shut down normally.

To apply the first incremental backup to the full backup, run the following command:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --apply-log-only --target-dir=/data/backups/base \
--incremental-dir=/data/backups/inc1
```

This applies the delta files to the files in `/data/backups/base`, which
rolls them forward in time to the time of the incremental backup. It then
applies the redo log as usual to the result. The final data is in
`/data/backups/base`, not in the incremental directory. You should see
an output similar to:

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

!!! warning
   
    Percona XtraBackup does not support using the same incremental backup directory to prepare two copies of backup. Do not run `--prepare` with the same incremental backup directory (the value of –incremental-dir) more than once.

Preparing the second incremental backup is a similar process: apply the deltas
to the (modified) base backup, and you will roll its data forward in time to the point of the second incremental backup:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --target-dir=/data/backups/base \
--incremental-dir=/data/backups/inc2
```

!!! note
   
    `--apply-log-only` should be used when merging the incremental backups except the last one. That’s why the previous line does not contain the `--apply-log-only` option. Even if the `--apply-log-only` was used on the last step, backup would still be consistent but in that case server would perform the rollback phase.

Once prepared incremental backups are the same as the full backups, and they can be [restored](restore-a-backup.md) in the same way.