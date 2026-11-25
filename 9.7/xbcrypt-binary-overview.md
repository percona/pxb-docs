> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-xtrabackup/9.7/llms.txt).

# The xbcrypt binary overview

To support encryption and decryption of the backups, a new tool `xbcrypt` was introduced to *Percona XtraBackup*.

This utility has been modeled after The [xbstream binary](https://docs.percona.com/percona-xtrabackup/9.7/xbstream-binary-overview.md) to perform encryption and decryption outside of Percona XtraBackup.

The `XBCRYPT_ENCRYPTION_KEY` environment variable is only used in place of the `--encrypt_key=name` option. You can use the environment variable or command line option. If you use both, the command line option takes precedence over the value specified in the environment variable.
