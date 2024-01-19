# The xbstream binary overview

To support simultaneous compression and streaming, a new custom streaming
format called xbstream was introduced to Percona XtraBackup in addition to
the TAR format. That was required to overcome some limitations of traditional
archive formats such as tar, cpio and others which did not allow streaming
dynamically generated files, for example dynamically compressed files. Other
advantages of xbstream over traditional streaming/archive format include
ability to stream multiple files concurrently (so it is possible to use
streaming in the xbstream format together with the –parallel option) and more
compact data storage.

For details on the command-line options, see [xbcloud command-line options].

The utility tries to minimize its impact on the OS page cache by using the
appropriate `posix_fadvise()` calls when available.

When compression is enabled with xtrabackup all data is compressed,
including the transaction log file and meta data files, using the specified
compression algorithm. Read more about supported compression algorithms in the [Create a compressed backup](create-compressed-backup.md) document.

[xbcloud command-line options]: xbcloud-options.md