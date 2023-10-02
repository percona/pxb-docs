# Prepare a partial backup

The procedure is analogous to restoring individual tables: apply the logs and use the
`--export` option:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --export --target-dir=/path/to/partial/backup
```

When you use the `--prepare` option on a partial backup, you
will see warnings about tables that don’t exist. This is because these tables
exist in the data dictionary inside InnoDB, but the corresponding .ibd
files don’t exist. They were not copied into the backup directory. These tables
will be removed from the data dictionary, and when you restore the backup and
start InnoDB, they will no longer exist and will not cause any errors or
warnings to be printed to the log file.

Could not find any file associated with the tablespace ID: 5

Use `--innodb-directories` to find the tablespace files. If that fails then use `-–innodb-force-recovery=1` to ignore this and to permanently lose all changes to the missing tablespace(s).

## Next step

[Restore the partition from the backup :material-arrow-right:](restore-individual-partitions.md){.md-button}