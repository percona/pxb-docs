<!---
 fix and rewrite
 20230817
 --->

# Accelerate the backup process

## Copy with the `--parallel` and `--compress-threads` options

When making a local or streaming backup with xbstream binary, multiple files
can be copied at the same time when using the `--parallel` option. This
option specifies the number of threads created by xtrabackup to copy data
files.

To take advantage of this option either the multiple tablespaces option must be
enabled (innodb_file_per_table) or the shared tablespace must be stored
in multiple ibdata files with the innodb_data_file_path option.
Having multiple files for the database (or splitting one into many) doesn’t have
a measurable impact on performance.

As this feature is implemented at the file level, concurrent file transfer
can sometimes increase I/O throughput when doing a backup on highly fragmented
data files, due to the overlap of a greater number of random read requests. You
should consider tuning the filesystem also to obtain the maximum performance
(e.g. checking fragmentation).

If the data is stored on a single file, this option has no effect.

To use this feature, simply add the option to a local backup, for example:

```shell
xtrabackup --backup --parallel=4 --target-dir=/path/to/backup
```

By using the xbstream in streaming backups, you can additionally speed up the
compression process with the `--compress-threads` option. This option
specifies the number of threads created by xtrabackup for parallel data
compression. The default value for this option is 1.

To use this feature, simply add the option to a local backup, for example:

```shell
xtrabackup --backup --stream=xbstream --compress --compress-threads=4 --target-dir=./ > backup.xbstream
```

Before applying logs, compressed files will need to be uncompressed.

## The `--rsync` option

### Version changes

Percona XtraBackup 8.4.0-8 deprecates the [`--rsync`](xtrabackup-option-reference.md#rsync) option. A future release will remove the option. Use [`--lock-ddl=REDUCED`](xtrabackup-option-reference.md#lock-ddl) instead.

!!! note

    You cannot use `--rsync` with the `--stream` option. If you pass both options, Percona XtraBackup reports the following error and does not start the backup:

    ```{.text .no-copy}
    --rsync doesn't work with --stream
    ```
