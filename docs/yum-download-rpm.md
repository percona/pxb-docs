# Install with RPM packages

This guide walks you through installing Percona XtraBackup 8.0 using DEB packages on Ubuntu-based systems.
{.power-number}

1. Download the appropriate packages for your architecure from [Percona Software Downloads](https://www.percona.com/downloads). This example downloads the Percona XtraBackup 8.0 package for Red Hat Enterprise Linux 9.

    ```{.bash data-prompt="$"}
    $ wget https://downloads.percona.com/downloads/Percona-XtraBackup-LATEST/Percona-XtraBackup-8.0.32-26/binary/redhat/9/x86_64/percona-xtrabackup-80-8.0.32-26.1.el9.x86_64.rpm
    ```

2. Install the package

    ```{.bash data-prompt="$"}
    $ sudo yum localinstall percona-xtrabackup-80-8.0.32-26.1.el9.x86_64.rpm
    ```

## Common dependencies

| Library name | Description                                                                                   |
|--------------|-----------------------------------------------------------------------------------------------|
| libev        | A high-performance event-loop library used in asynchronous network applications.               |
| libgcrypt    | A general-purpose cryptographic library providing encryption, decryption, and hashing algorithms.|
| openssl      | A robust library for implementing SSL/TLS encryption and cryptographic functions.              |
| zlib         | A compression library that supports data compression and decompression using the DEFLATE algorithm.|
| libaio       | A library for asynchronous I/O operations, providing non-blocking I/O functionality.           |

If yum reports missing dependencies, it may offer to install them automatically. If not, you can install these dependencies manually using the following example.

```{.bash data-prompt="$"}
$ sudo yum install libev libgcrypt openssl zlib libaio
```

## Verify the installation

After installation, verify it by checking the version:

```{.bash data-prompt="$"}
$ xtrabackup --version
```

## Troubleshoot the installation

| Issue                         | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| Permission denied              | Ensure you're using sudo or have root access for installation commands.     |
| Repository issues              | If packages are not found, check your yum repository configuration.         |
| Incompatible OS version        | Double-check your OS version matches the package requirements.              |
| Conflicts with existing packages | Consider removing conflicting packages or use a separate environment.     |

If you encounter persistent issues, consult the Percona XtraBackup documentation or reach out to their support forums for assistance.

Remember, when installing packages manually, you're responsible for managing dependencies and potential conflicts. Always back up your data before making significant system changes.