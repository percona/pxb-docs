# Prepare an individual partitions backup

For preparing partial backups, the procedure is analogous to restoring
individual tables. Apply the logs and use xtrabackup --export:

```{.bash data-prompt="$"}
$ xtrabackup --apply-log --export /mnt/backup/2012-08-28_10-29-09
```

You may see warnings in the output about tables that do not exist. This happens
because InnoDB-based engines stores its data dictionary inside the tablespace
files. xtrabackup removes the missing tables (those that haven’t been selected in the partial
backup) from the data dictionary in order to avoid future warnings or errors.

## Next step

[Restore the partition from the backup :material-arrow-right:](restore-individual-partitions.md){.md-button}

