> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-xtrabackup/9.7/llms.txt).

# Install Percona XtraBackup 9.7 using downloaded RPM packages

Download `RPM` packages of the desired series for your architecture from the [Percona Software Downloads](https://www.percona.com/downloads) . If needed, [Percona Software Download instructions](https://docs.percona.com/percona-xtrabackup/9.7/download-instructions.md) are available.

This method requires you to resolve all dependencies and install any missing packages. Always back up your data before making significant system changes.

The following example downloads *Percona XtraBackup* 9.7.2-3 release packages for *RHEL* 9. Run the following commands as root or use the sudo command.

1. Install wget

   ```bash
   sudo dnf install wget
   ```

1. Use `wget` to download the `RPM` package:

   ```bash
   wget https://downloads.percona.com/downloads/Percona-XtraBackup-9.7/Percona-XtraBackup-9.7.2-3/binary/redhat/9/x86_64/percona-xtrabackup-97-9.7.2-31.el9.x86_64.rpm
   ```

1. Install Percona XtraBackup by running:

   ```bash
   sudo dnf install ./percona-xtrabackup-97-9.7.2-31.el9.x86_64.rpm
   ```

## Common dependencies

| Library name | Description                                                                                         |
| ------------ | --------------------------------------------------------------------------------------------------- |
| libev        | A high-performance event-loop library used in asynchronous network applications.                    |
| libgcrypt    | A general-purpose cryptographic library providing encryption, decryption, and hashing algorithms.   |
| openssl      | A robust library for implementing SSL/TLS encryption and cryptographic functions.                   |
| zlib         | A compression library that supports data compression and decompression using the DEFLATE algorithm. |
| libaio       | A library for asynchronous I/O operations, providing non-blocking I/O functionality.                |

If dnf reports missing dependencies, it may offer to install them automatically. If not, you can install these dependencies manually using the following example.

```bash
sudo dnf install libev libgcrypt openssl zlib libaio
```

## Verify the installation

After installation, verify it by checking the version:

```bash
xtrabackup --version
```

## Troubleshoot the installation

| Issue                            | Description                                                             |
| -------------------------------- | ----------------------------------------------------------------------- |
| Permission denied                | Ensure you’re using sudo or have root access for installation commands. |
| Repository issues                | If packages are not found, check your yum repository configuration.     |
| Incompatible OS version          | Double-check your OS version matches the package requirements.          |
| Conflicts with existing packages | Consider removing conflicting packages or use a separate environment.   |

If you encounter persistent issues, consult the Percona XtraBackup documentation or [Get help from Percona](https://docs.percona.com/percona-xtrabackup/9.7/get-help.md).
