# Create a full backup

To create a backup, run **xtrabackup** with the `--backup`
option. You also need to specify the `--target-dir` option, which is where
the backup will be stored, if the *InnoDB* data or log files are not stored
in
the same directory, you might need to specify the location of those, too.
If the
target directory does not exist, *xtrabackup* creates it. If the directory
does
exist and is empty, *xtrabackup* will succeed.

*xtrabackup* will not overwrite existing files, it will fail with operating
system error 17, `file exists`.

To start the backup process run:

```{.bash data-prompt="$"}
$ xtrabackup --backup --target-dir=/data/backups/
```

This will store the backup at `/data/backups/`. If you specify a
relative path, the target directory will be relative to the current directory.

During the backup process, you should see a lot of output showing the data
files being copied, as well as the log file thread repeatedly scanning the
log files and copying from it. Here is an example that shows the log thread
scanning the log in the background, and a file copying thread working on the `ibdata1` file:

??? example "Expected output"

    ```{.text .no-copy}
    160906 10:19:17 Finished backing up non-InnoDB tables and files
    160906 10:19:17 Executing FLUSH NO_WRITE_TO_BINLOG ENGINE LOGS...
    xtrabackup: The latest check point (for incremental): '62988944'
    xtrabackup: Stopping log copying thread.
    .160906 10:19:18 >> log scanned up to (137343534)
    160906 10:19:18 Executing UNLOCK TABLES
    160906 10:19:18 All tables unlocked
    160906 10:19:18 Backup created in directory '/data/backups/'
    160906 10:19:18 [00] Writing backup-my.cnf
    160906 10:19:18 [00]        ...done
    160906 10:19:18 [00] Writing xtrabackup_info
    160906 10:19:18 [00]        ...done
    xtrabackup: Transaction log of lsn (26970807) to (137343534) was copied.
    160906 10:19:18 completed OK!
    ```

The last thing you should see is something like the following, where the
value of the `<LSN>` will be a number that depends on your system:

```{.bash data-prompt="$"}
$ xtrabackup: Transaction log of lsn (<LSN>) to (<LSN>) was copied.
```

!!! note
   
    Log copying thread checks the transactional log every second to see if there were any new log records written that need to be copied, but there is a chance that the log copying thread might not be able to keep up with the amount of writes that go to the transactional logs, and will hit an error when the log records are overwritten before they could be read.

After the backup is finished, the target directory will contain files such as the following, assuming you have a single InnoDB table `test.tbl1` and you are using MySQL’s innodb_file_per_table option:

```{.bash data-prompt="$"}
$ ls -lh /data/backups/
```

The result should look like this:

??? example "Expected output"

    ```{.text .no-copy}
    total 182M
    drwx------  7 root root 4.0K Sep  6 10:19 .
    drwxrwxrwt 11 root root 4.0K Sep  6 11:05 ..
    -rw-r-----  1 root root  387 Sep  6 10:19 backup-my.cnf
    -rw-r-----  1 root root  76M Sep  6 10:19 ibdata1
    drwx------  2 root root 4.0K Sep  6 10:19 mysql
    drwx------  2 root root 4.0K Sep  6 10:19 performance_schema
    drwx------  2 root root 4.0K Sep  6 10:19 sbtest
    drwx------  2 root root 4.0K Sep  6 10:19 test
    drwx------  2 root root 4.0K Sep  6 10:19 world2
    -rw-r-----  1 root root  116 Sep  6 10:19 xtrabackup_checkpoints
    -rw-r-----  1 root root  433 Sep  6 10:19 xtrabackup_info
    -rw-r-----  1 root root 106M Sep  6 10:19 xtrabackup_logfile
    ```

The backup can take a long time, depending on how large the database is. It is safe to cancel at any time, because *xtrabackup* does not modify the database.

The next step is to [prepare](prepare-full-backup.md) the backup in order to restore it. 

<script>
    (function(h,o,t,j,a,r){
        h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
        h._hjSettings={hjid:3857510,hjsv:6};
        a=o.getElementsByTagName('head')[0];
        r=o.createElement('script');r.async=1;
        r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
        a.appendChild(r);
    })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
</script>
