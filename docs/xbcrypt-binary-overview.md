# The xbcrypt binary overview

To support encryption and decryption of the backups, a new tool `xbcrypt` was
introduced to *Percona XtraBackup*.

**Percona XtraBackup** 8.0.28-20 implements the `XBCRYPT_ENCRYPTION_KEY` environment variable. The variable is only used in place of the `--encrypt_key=name` option. You can use the environment variable or command line option. If you use both, the command line option takes precedence over the value specified in the environment variable.

This utility has been modeled after The [xbstream binary](xbstream-binary-overview.md) to perform encryption and decryption outside of *Percona XtraBackup*. `

For more details on the command-line options, see [xbcrypt command-line options](xbcrypt-options.md)
