# Prepare an individual partitions backup

To prepare partial backups, follow a procedure similar to restoring individual tables. Apply the logs and use the `--export` option:

```shell
xtrabackup --prepare --export --target-dir=/mnt/backup/2012-08-28_10-29-09
```

You may see warnings in the output about tables that do not exist. This happens
because InnoDB-based engines stores its data dictionary inside the tablespace
files. During the prepare phase, xtrabackup removes entries for tables that were not included in the partial backup from the data dictionary, preventing future warnings or errors.

## Next step

[Restore the partition from the backup](restore-individual-partitions.md){.md-button}

