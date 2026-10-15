# Create a full backup

## Command reference

Quick syntax for creating a full backup with common options:

```bash
xtrabackup --backup --target-dir=<path> [--user=<user>] [--password=<password>]
```

| Flag | Required | Description |
|------|----------|-------------|
| `--backup` | Yes | Runs xtrabackup in backup mode. |
| `--target-dir=<path>` | Yes | Directory where the backup is stored. Created if it does not exist. |
| `--user=<user>` | No | MySQL user for connecting to the server (default: current OS user). |
| `--password=<password>` | No | Password for the MySQL user. Omit to be prompted, or use a login file for security. |

Example with authentication:

```bash
xtrabackup --backup --target-dir=/data/backups/ --user=backup --password=secret
```

---

To create a backup, run xtrabackup with the `--backup`
option. You also must specify the `--target-dir` option, which is where
the backup is stored. If the InnoDB data or log files are not stored
in
the same directory, you must specify their location.
If the
target directory does not exist, xtrabackup creates it. If the directory
does
exist and is empty, xtrabackup succeeds.

xtrabackup does not overwrite existing files. It will fail with operating
system error 17, `file exists`.

The following command starts the process. Run all the commands as root or use the sudo command.

```bash
xtrabackup --backup --target-dir=/data/backups/
```

This operation stores the backup at `/data/backups/`. If you specify a
relative path, the target directory is relative to the current directory.

During the backup process, the output shows the copied data
files, and a log file thread that scans and copies from the
log files.

The following is an example of the output:

??? example "Expected output"

    ```{.text .no-copy}
    ...
    2026-10-13T17:14:12.911323-00:00 0 [Note] [MY-011825] [Xtrabackup] Executing FLUSH NO_WRITE_TO_BINLOG ENGINE LOGS...
    2026-10-13T17:14:12.912983-00:00 0 [Note] [MY-011825] [Xtrabackup] The latest check point (for incremental): '36478353'
    2026-10-13T17:14:12.912994-00:00 0 [Note] [MY-011825] [Xtrabackup] Stopping log copying thread at LSN 36479260
    2026-10-13T17:14:12.916037-00:00 0 [Note] [MY-011825] [Xtrabackup] Executing UNLOCK TABLES
    2026-10-13T17:14:12.916228-00:00 0 [Note] [MY-011825] [Xtrabackup] All tables unlocked
    2026-10-13T17:14:12.917457-00:00 0 [Note] [MY-011825] [Xtrabackup] Backup created in directory '/data/backups/'
    2026-10-13T17:14:12.917481-00:00 0 [Note] [MY-011825] [Xtrabackup] MySQL binlog position: filename 'binlog.000004', position '198', GTID of the last change '78cf2c47-c729-11f1-90e4-f23a559b785b:1-5'
    2026-10-13T17:14:12.921613-00:00 0 [Note] [MY-011825] [Xtrabackup] Backup size: 98.59 MiB (103373868 bytes)
    2026-10-13T17:14:13.924839-00:00 0 [Note] [MY-011825] [Xtrabackup] Transaction log of lsn (36478353) to (36479270) was copied.
    2026-10-13T17:14:14.161363-00:00 0 [Note] [MY-011825] [Xtrabackup] completed OK!
    ```

The last line of the output is `completed OK!`. Also check the exit code of the command: `0` means that the backup succeeded, any other value means that it failed.

!!! note
   
    Log copying thread checks the transactional log every second to see if there were any new log records written that need to be copied, but there is a chance that the log copying thread might not be able to keep up with the amount of writes that go to the transactional logs, and will hit an error when the log records are overwritten before they could be read.

After the backup is finished, the target directory will contain files such as the following, for a server with a `test` database that contains two InnoDB tables:

```shell
ls -lh /data/backups/
```

The result should look like this:

??? example "Expected output"

    ```{.text .no-copy}
    total 76M
    -rw-r----- 1 root root  447 Oct 13 17:14 backup-my.cnf
    -rw-r----- 1 root root  198 Oct 13 17:14 binlog.000004
    -rw-r----- 1 root root   16 Oct 13 17:14 binlog.index
    -rw-r----- 1 root root 5.6K Oct 13 17:14 ib_buffer_pool
    -rw-r----- 1 root root  12M Oct 13 17:14 ibdata1
    drwxr-x--- 2 root root 4.0K Oct 13 17:14 mysql
    -rw-r----- 1 root root  31M Oct 13 17:14 mysql.ibd
    drwxr-x--- 2 root root 4.0K Oct 13 17:14 performance_schema
    drwxr-x--- 2 root root 4.0K Oct 13 17:14 sys
    drwxr-x--- 2 root root 4.0K Oct 13 17:14 test
    -rw-r----- 1 root root  16M Oct 13 17:14 undo_001
    -rw-r----- 1 root root  16M Oct 13 17:14 undo_002
    -rw-r----- 1 root root   59 Oct 13 17:14 xtrabackup_binlog_info
    -rw-r----- 1 root root  134 Oct 13 17:14 xtrabackup_checkpoints
    -rw-r----- 1 root root  675 Oct 13 17:14 xtrabackup_info
    -rw-r----- 1 root root 3.5K Oct 13 17:14 xtrabackup_logfile
    -rw-r----- 1 root root   39 Oct 13 17:14 xtrabackup_tablespaces
    ```

The backup can take a long time, depending on how large the database is. It is safe to cancel at any time, because xtrabackup does not modify the database.

## Next step

[Prepare the backup](prepare-full-backup.md){.md-button}
