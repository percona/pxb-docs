# Make a compressed backup

In order to make a compressed backup, use the `--compress` option along
with the `--backup` and `--target-dir` options. Percona XtraBackup supports the following compression algorithms:

`quicklz`
    
    To compress files using the `quicklz` compression algorithm, use `--compress` option:

    ```{.bash data-prompt="$"}
    $ xtrabackup --backup --compress --target-dir=/data/backup
    ```

`lz4`

    To compress files using the `lz4` compression algorithm, set `--compress` option to `lz4`:

    ```{.bash data-prompt="$"}
    $ xtrabackup --backup --compress=lz4 --target-dir=/data/backup
    ```

`Zstandard (ZSTD)`

    The Zstandard (ZSTD) compression algorithm is a [tech preview](../glossary.md#tech-preview) feature. Before using ZSTD in production, we recommend that you test restoring production from physical backups in your environment, and also use the alternative backup method for redundancy.

    [Percona XtraBackup 8.0.30-23](release-notes/8.0/8.0.30-23.0.md) adds support for the `Zstandard (ZSTD)` compression algorithm. `ZSTD` is a fast lossless compression algorithm that targets real-time compression scenarios and better compression ratios.  
    
    To compress files using the `ZSTD` compression algorithm, set `--compress` option to `zstd`:

    ```{.bash data-prompt="$"}
    $ xtrabackup --backup --compress=zstd --target-dir=/data/backup
    ```

    You can specify `ZSTD` compression level with the [`--compress-zstd-level(=#)`](/docs/xtrabackup_bin/xbk_option_reference.md#compress-zstd-level) option. The defaul value is `1`.

    ```{.bash data-prompt="$"}
    $ xtrabackup --backup --compress-zstd-level=1 --target-dir=/data/backup
    ```

If you want to speed up the compression you can use the parallel
compression, which can be enabled with `--compress-threads`
option. The following example uses four threads for compression.

```{.bash data-prompt="$"}
$ xtrabackup --backup --compress --compress-threads=4 --target-dir=/data/backup
```

Output should look like this:

??? example "Expected output"

    ```{.text .no-copy}
    ...

    [01] Compressing ./imdb/comp_cast_type.ibd to /data/backup/imdb/comp_cast_type.ibd.qp
    [01]        ...done
    ...
    130801 11:50:24  xtrabackup: completed OK
    ```

## Prepare the backup

Before you can prepare the backup you’ll need to uncompress all the files.

If you used `quicklz` compression algorithm, use `qpress` (which is available from [Percona Software repositories](http://www.percona.com/doc/percona-xtrabackup/8.0/installation.html#using-percona-software-repositories)).

You can use the following one-liner to uncompress all the files:

```{.bash data-prompt="$"}
$ for bf in `find . -iname "*\.qp"`; do qpress -d $bf $(dirname $bf) && rm $bf; done
``` 

If you used `lz4` compression algorithm, change this script to search
for `\*.lz4` files:

```{.bash data-prompt="$"}
$ for bf in `find . -iname "*\.lz4"`; do lz4 -d $bf $(dirname $bf) && rm $bf; done
```

*Percona XtraBackup* has implemented `--decompress` option
that can be used to decompress the backup made using `quicklz`, `lz4`, or `ZSTD` compression algorithm.

```{.bash data-prompt="$"}
$ xtrabackup --decompress --target-dir=/data/compressed/
```

When the files are uncompressed you can prepare the backup with the
`--apply-log-only` option:

```{.bash data-prompt="$"}
$ xtrabackup --apply-log-only --target-dir=/data/backup/
```

You should check for a confirmation message:

??? example "Expected output"

    ```{.text .no-copy}
    130802 02:51:02  xtrabackup: completed OK!
    ```

Now the files in `/data/backup/` are ready to be used by the server.

!!! note
   
    *Percona XtraBackup* does not automatically remove the compressed files. In order to clean up the backup directory users should remove the `\*.qp` files.

## Restore the backup

Once the backup has been prepared you can use the `--copy-back` to
restore the backup.

```{.bash data-prompt="$"}
$ xtrabackup --copy-back --target-dir=/data/backup/
```

This will copy the prepared data back to its original location as defined
by the `datadir` variable in the `my.cnf` file.

After the confirmation message, you should check the file permissions after
copying the data back.

??? example "Expected output"

    ```{.text .no-copy}
    130802 02:58:44  xtrabackup: completed OK!
    ```

You may need to adjust the file permissions. The following example
demonstrates how to do it recursively by using **chown**:

```{.bash data-prompt="$"}
$ chown -R mysql:mysql /var/lib/mysql
```

Now, your data directory contains the restored data. You are
ready to start the server.