# Make a streaming backup

Stream mode sends the backup to `STDOUT` in the `xbstream` format instead
of
copying it to the directory named by the first argument. You can pipe the
output
to a local file, or, across the network, to another server.

To extract the resulting `xbstream` file, you **must** use the `xbstream`
utility: `xbstream -x <  backup.xbstream`.

### Examples of Using `xbstream`

| Action   | Command   |
|--------|-----------|
| Stream the backup into an archived named `backup.xbstream` | `$ xtrabackup --backup --stream=xbstream --target-dir= > backup.xbstream` |
| Stream the backup into a compressed archive named `backup.xbstream`  | `$ xtrabackup --backup --stream=xbstream --compress --target-dir= > backup.xbstream`  |
| Encrypt the backup  | `$ xtrabackup --backup --stream=xbstream --target-dir= > backup.xbstream gzip -`` | openssl des3 -salt -k “password” backup.xbstream.gz.des3`  |
| Send the backup to another server and unpack it | `$ xtrabackup --backup --compress --stream=xbstream --target-dir= | ssh user@otherhost “xbstream -x”`|
| Send the backup to another server using `netcat`| On the destination host:<br />`$ nc -l 9999 | cat - > /data/backups/backup.xbstream`<br /><br />On the source host:<br />`$ xtrabackup --backup --stream=xbstream --target-dir= | nc desthost 9999`  |
| Send the backup to another server using a one-liner                                                                 | `$ ssh user@desthost “( nc -l 9999 > /data/backups/backup.xbstream & )” && xtrabackup --backup --stream=xbstream --target-dir= |  nc desthost 9999` |
| Throttle the throughput to 10MB/sec using the [pipe viewer](https://www.ivarch.com/programs/quickref/pv.shtml) tool | `$ xtrabackup --backup --stream=xbstream --target-dir= | pv -q -L10m ssh user@desthost “cat - > /data/backups/backup.xbstream”` |
| Checksum the backup during the streaming | On the destination host:<br />`$ nc -l 9999 | tee >(sha1sum > destination_checksum) > /data/backups/backup.xbstream`<br /><br />On the source host:<br />`$ xtrabackup --backup --stream=xbstream --target-dir= | tee >(sha1sum > source_checksum) | nc desthost 9999`<br /><br />Compare the checksums on the source host:<br />`$ cat source_checksum 65e4f916a49c1f216e0887ce54cf59bf3934dbad`<br /><br />Compare the checksums on the destination host:<br />`$ cat destination_checksum 65e4f916a49c1f216e0887ce54cf59bf3934dbad` |
| Parallel compression with parallel copying backup  | `$ xtrabackup --backup --compress --compress-threads=8 --stream=xbstream --parallel=4 --target-dir=./ > backup.xbstream` |



