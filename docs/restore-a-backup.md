# Restore a backup

!!! warning
   
    Backup needs to be prepared before it can be restored.

For convenience, *xtrabackup* binary has the `--copy-back` option to copy the backup to the datadir of the server:

```{.bash data-prompt="$"}
$ xtrabackup --copy-back --target-dir=/data/backups/
```

If you don’t want to save your backup, you can use the `--move-back` option which will move the backed up data to the datadir.

If you don’t want to use any of the above options, you can additionally use
rsync or cp to restore the files.

!!! note
   
    The datadir must be empty before restoring the backup. Also, it’s important to note that MySQL server needs to be shut down before restore is performed. You cannot restore to a datadir of a running mysqld instance (except when importing a partial backup).

Example of the rsync command that can be used to restore the backup
can look like this:

```{.bash data-prompt="$"}
$ rsync -avrP /data/backup/ /var/lib/mysql/
```

You should check that the restored files have the correct ownership and permissions.

As files’ attributes are preserved, in most cases you must change the files’ ownership to `mysql` before starting the database server, as the files are owned by the user who created the backup:

```{.bash data-prompt="$"}
$ chown -R mysql:mysql /var/lib/mysql
```

Data is now restored, and you can start the server.
