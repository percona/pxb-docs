# Prepare a full backup

After making a backup with the `--backup` option, you need to prepare it in order to [restore](restore-a-backup.md) it. Data files are not point-in-time
consistent until they are prepared, because they were copied at different times as the program ran, and they might have been changed while this was happening.

If you try to start InnoDB with these data files, it will detect corruption and stop working to avoid running on damaged data. The `--prepare` step makes the files perfectly consistent at a single instant in time, so you can run InnoDB on them.

You can run the prepare operation on any machine; it does not need to be on the originating server or the server to which you intend to restore. You can copy the backup to a utility server and prepare it there.

Note that Percona XtraBackup 8.1 can only prepare backups of MySQL
8.1, Percona Server for MySQL 8.1, and Percona XtraDB Cluster 8.1
databases. Releases prior to 8.1 are not supported.

During the prepare operation, xtrabackup boots up a kind of modified embedded InnoDB (the libraries xtrabackup was linked against). The modifications are necessary to disable InnoDB standard safety checks, such as complaining about the log file not being the right size. This warning is not appropriate for working with backups. These modifications are only for the xtrabackup binary; you do not need a modified InnoDB to use xtrabackup for your backups.

The prepare step uses this “embedded InnoDB” to perform crash recovery on the copied data files, using the copied log file. The `prepare` step is very simple to use: you simply run xtrabackup with the `--prepare` option and tell it which directory to prepare, for example, to prepare the previously taken backup run:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --target-dir=/data/backups/
```

When this finishes, you should see an `InnoDB shutdown` with a message such as the following, where again the value of LSN will depend on your system:

??? example "Expected output"

    ```{.text .no-copy}
    InnoDB: Shutdown completed; log sequence number 137345046
    160906 11:21:01 completed OK!
    ```

All following prepares will not change the already prepared data files, you’ll see that output says:

??? example "Expected output"

    ```{.text .no-copy}
    xtrabackup: This target seems to be already prepared.
    xtrabackup: notice: xtrabackup_logfile was already used to '--prepare'.
    ```

It is not recommended to interrupt xtrabackup process while preparing backup because it may cause data files corruption and backup will become unusable. Backup validity is not guaranteed if prepare process was interrupted.

!!! note
   
    If you intend the backup to be the basis for further incremental backups, you should use the `--apply-log-only` option when preparing the backup, or you will not be able to apply incremental backups to it. See the documentation on preparing incremental backups for more details.

After preparing the backup, you can [restore](restore-a-backup.md) the backup.
