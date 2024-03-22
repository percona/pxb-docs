# Take a streaming backup

Percona XtraBackup supports streaming mode. Streaming mode sends a backup to `STDOUT` in the *xbstream* format instead of copying the files to the backup directory.

This method allows you to use other programs to filter the output of the backup,
providing greater flexibility for storage of the backup. For example,
compression is achieved by piping the output to a compression utility. One of
the benefits of streaming backups and using Unix pipes is that the backups can
be automatically encrypted.

To use the streaming feature, run the `--stream` option.

```{.bash data-prompt="$"}
$ xtrabackup --stream
```

*xtrabackup* uses *xbstream* to stream all of the data files to `STDOUT`, in a
special `xbstream` format. After it finishes streaming all of the data files
to `STDOUT`, it stops xtrabackup and streams the saved log file too.

When compression is enabled, *xtrabackup* compresses the output data, except for the meta and non-InnoDB files which are not compressed, using the specified compression algorithm. Percona XtraBackup supports the following compression algorithms:

## Zstandard (ZSTD)

The Zstandard (ZSTD) is a fast lossless compression algorithm that targets real-time compression scenarios and better compression ratios. `ZSTD` is the default compression algorithm for the `--compress` option.

To compress files using the `ZSTD` compression algorithm, use the `--compress` option:

```{.bash data-prompt="$"}
$ xtrabackup --backup --compress --target-dir=/data/backup
```

The resulting files have the `\*.zst` format.
   
You can specify `ZSTD` compression level with the [`--compress-zstd-level(=#)`](xtrabackup-option-reference.md#compress-zstd-level) option. The default value is `1`.

```{.bash data-prompt="$"}
$ xtrabackup –backup –compress –compress-zstd-level=1 –target-dir=/data/backup
```

## lz4

To compress files using the `lz4` compression algorithm, set the `--compress` option to `lz4`:

```{.bash data-prompt="$"}
$ xtrabackup --backup --compress=lz4 --target-dir=/data/backup
```

The resulting files have the `\*.lz4` format. 
    
To decompress files, use the `--decompress` option.

In case backups were both compressed and encrypted, they must be decrypted before they are uncompressed.

|Task  | Command  |
|---------|------|
| Stream the backup into an archive named `backup.xbstream` | `xtrabackup --backup --stream > backup.xbstream`|
| Stream the backup into a compressed archive named `backup.xbstream`| `xtrabackup --backup --stream --compress > backup.xbstream` |
| Encrypt the backup | `xtrabackup --backup --stream  |gzip  | openssl des3 -salt -k 'password' -out  backup.xbstream.gz.des3` | 
| Unpack the backup to the current directory | `xbstream -x < backup.xbstream`
| Send the backup compressed directly to another host and unpack it | `xtrabackup --backup --compress --stream | ssh user@otherhost "xbstream -x"`|
| Send the backup to another server using `netcat` | On the destination host:<br />`nc -l 9999 | cat - > /data/backups/backup.xbstream`<br /><br />On the source host:<br />`xtrabackup --backup --stream | nc desthost 9999` |
| Send the backup to another server using a one-liner  | `ssh user@desthost “( nc -l 9999 > /data/backups/backup.xbstream & )” && xtrabackup --backup --stream | nc desthost 9999` |
| Throttle the throughput to 10MB/sec using the [pipe viewer](https://www.ivarch.com/programs/quickref/pv.shtml) tool | `xtrabackup --backup --stream | pv -q -L10m ssh user@desthost “cat - > /data/backups/backup.xbstream”` |
| Checksum the backup during the streaming  | On the destination host:<br />`nc -l 9999 | tee >(sha1sum > destination_checksum) > /data/backups/backup.xbstream`<br /><br />On the source host:<br />`xtrabackup --backup --stream | tee >(sha1sum > source_checksum) | nc desthost 9999`<br /><br />Compare the checksums on the source host:<br />`cat source_checksum 65e4f916a49c1f216e0887ce54cf59bf3934dbad`<br /><br />Compare the checksums on the destination host:<br />`cat destination_checksum 65e4f916a49c1f216e0887ce54cf59bf3934dbad` |
| Parallel compression with parallel copying backup | `xtrabackup --backup --compress --compress-threads=8 --stream --parallel=4 > backup.xbstream`|

!!! important

    The streamed backup must be prepared before restoration. Streaming mode does not prepare the backup.
