> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-xtrabackup/8.4/llms.txt).

# The xbstream binary overview

To support simultaneous compression and streaming, the xbstream binary was added to Percona XtraBackup, along with the xbstream format and tar format. These additions were required to overcome some limitations of traditional archive formats such as tar, cpio, and others, which did not allow streaming dynamically generated files.

Other advantages of xbstream over traditional streaming/archive format include streaming multiple files concurrently (so it is possible to use streaming in the xbstream format together with the –parallel option) and more compact data storage.

For details on the command-line options, see [xbcloud command-line options](https://docs.percona.com/percona-xtrabackup/8.4/xbcloud-options.html). When available, the utility tries to minimize its impact on the OS page cache by using the appropriate `posix_fadvise()` calls.

When compression is enabled with xtrabackup all data is compressed, including the transaction log file and metadata files, using the specified compression algorithm. Read more about supported compression algorithms in the [Create a compressed backup](https://docs.percona.com/percona-xtrabackup/8.4/create-compressed-backup.html) document.
