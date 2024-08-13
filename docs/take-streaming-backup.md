# Take a streaming backup

Percona XtraBackup supports streaming mode. Streaming mode sends a backup to `STDOUT` in the xbstream format instead of copying the files to the backup directory.

This method enables you to utilize other programs to filter the backup output, enhancing flexibility in backup storage. For instance, compression can be achieved by directing the output to a compression utility. One advantage of streaming backups and employing Unix pipes is that backups can be automatically encrypted.

## Version changes

* Starting with Percona XtraBackup 8.0.33-28, the `--stream` option does not require an `xbstream` parameter. The `xbstream` parameter is optional.

* Using `--encrypt` might create larger backups than expected when used with InnoDB Page Compression.

    To avoid this issue with compressed backups, use the `--compress` option with the `--xbstream` option in Percona XtraBackup 8.0.31-24 and later.

## Use streaming

To utilize the streaming feature, you need to employ the `--stream` option, specifying the stream format (xbstream). Specifying the stream format (xbstream) is optional, starting with Percona XtraBackup 8.0.33-28.

```{.bash data-prompt="$"}
$ xtrabackup --stream=xbstream
```

xtrabackup uses xbstream to stream all of the data files to `STDOUT`, in a
special `xbstream` format. After all data is streamed, xtrabackup stops and also streams the saved transaction log.

When compression is enabled, xtrabackup compresses the output data, except for the metadata, using the specified compression algorithm. Read about the supported compression algorithms in the [Create a compressed backup](create-compressed-backup.md) document.

With xbstream, backups can be copied and compressed simultaneously, significantly speeding up the process. However, if backups are both compressed and encrypted, they need to be decrypted before uncompressing.

|Task  | Command  |
|---------|------|
| Stream the backup into an archive named `backup.xbstream` | `xtrabackup --backup --stream=xbstream > backup.xbstream`|
| Stream the backup into a compressed archive named `backup.xbstream`| `xtrabackup --backup --stream=xbstream --compress > backup.xbstream` |
| Encrypt the backup | `xtrabackup --backup --stream=xbstream  \|gzip \| openssl des3 -salt -k 'password' -out backup.xbstream.gz.des3` |
| Unpack the backup to the current directory | `xbstream -x <  backup.xbstream`
| Send the backup compressed directly to another host and unpack it | `xtrabackup --backup --compress --stream=xbstream | ssh user@otherhost "xbstream -x"`|
| Send the backup to another server using `netcat` | On the destination host:<br />`nc -l 9999 | cat - > /data/backups/backup.xbstream`<br /><br />On the source host:<br />`xtrabackup --backup --stream=xbstream | nc desthost 9999` |
| Send the backup to another server using a one-liner  | `ssh user@desthost “( nc -l 9999 > /data/backups/backup.xbstream & )” && xtrabackup --backup --stream=xbstream | nc desthost 9999` |
| Throttle the throughput to 10MB/sec using the [pipe viewer](https://www.ivarch.com/programs/quickref/pv.shtml) tool | `xtrabackup --backup --stream=xbstream | pv -q -L10m ssh user@desthost “cat - > /data/backups/backup.xbstream”` |
| Checksum the backup during the streaming  | On the destination host:<br />`nc -l 9999 | tee >(sha1sum > destination_checksum) > /data/backups/backup.xbstream`<br /><br />On the source host:<br />`xtrabackup --backup --stream=xbstream | tee >(sha1sum > source_checksum) | nc desthost 9999`<br /><br />Compare the checksums on the source host:<br />`cat source_checksum 65e4f916a49c1f216e0887ce54cf59bf3934dbad`<br /><br />Compare the checksums on the destination host:<br />`cat destination_checksum 65e4f916a49c1f216e0887ce54cf59bf3934dbad` |
| Parallel compression with parallel copying backup | `xtrabackup --backup --compress --compress-threads=8 --stream=xbstream --parallel=4 > backup.xbstream`|

!!! important

    The streamed backup must be prepared before restoration. Streaming mode does not prepare the backup.
