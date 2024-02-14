# Restore a backup

!!! warning
   
    Backup needs to be prepared before it can be restored.

For convenience, *xtrabackup* binary has the `--copy-back` option to copy the backup to the datadir of the server:

```{.bash data-prompt="$"}
$ xtrabackup --copy-back --target-dir=/data/backups/
```

If you don’t want to save your backup, you can use the `--move-back` option which will move the backed up data to the datadir.

If you don’t want to use any of the above options, you can additionally use
**rsync** or **cp** to restore the files.

!!! note
   
    The datadir must be empty before restoring the backup. Also, it’s important to note that MySQL server needs to be shut down before restore is performed. You cannot restore to a datadir of a running mysqld instance (except when importing a partial backup).

Example of the **rsync** command that can be used to restore the backup
can look like this:

```{.bash data-prompt="$"}
$ rsync -avrP /data/backup/ /var/lib/mysql/
```

You should check that the restored files have the correct ownership and permissions.

As files’ attributes will be preserved, in most cases you will need to change the files’ ownership to `mysql` before starting the database server, as they will be owned by the user who created the backup:

```{.bash data-prompt="$"}
$ chown -R mysql:mysql /var/lib/mysql
```

Data is now restored, and you can start the server.

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