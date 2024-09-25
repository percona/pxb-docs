# Install with DEB packages

This guide walks you through installing Percona XtraBackup 8.0 using DEB packages on Ubuntu-based systems.
{.power-number}

1. Download the DEB package

    On the [Percona Software Downloads](https://www.percona.com/downloads) website, find the Percona XtraBackup 8.0 package for your system. 

    For example, for Ubuntu 20.04, this command downloads the appropriate package:

    ```{.bash data-prompt="$"}
    $ wget https://downloads.percona.com/downloads/Percona-XtraBackup-LATEST/Percona-XtraBackup-8.0.26-18/binary/debian/focal/x86_64/percona-xtrabackup-80_8.0.26-18-1.focal_amd64.deb
    ```

2. Install the package

    Use the dpkg command to install the downloaded package. You need root privileges for this:

    ```{.bash data-prompt="$"}
    $ sudo dpkg -i percona-xtrabackup-80_8.0.26-18-1.focal_amd64.deb
    ```

## Common dependencies for Percona XtraBackup

| Library Name    | Description                                                                                              |
|-----------------|----------------------------------------------------------------------------------------------------------|
| libmysqlclient  | A client library for MySQL, providing essential functions for connecting to and communicating with MySQL databases. |
| libssl          | A cryptographic library used for implementing SSL/TLS encryption, necessary for secure data transmission. |
| libcurl         | A library that enables data transfer via various protocols such as HTTP, FTP, and others, commonly used for handling web requests. |
| libev           | A high-performance event-loop library, often used in network applications for handling asynchronous events efficiently. |
| libgcrypt       | A general-purpose cryptographic library that provides encryption, decryption, and cryptographic hashing algorithms. |
| zlib            | A compression library used for data compression and decompression, supporting the popular DEFLATE compression algorithm. |

## Identify and add missing dependencies

If there are missing dependencies, dpkg shows error messages. Install any missing packages with the following command:

```{.bash data-prompt="$"}
$ sudo apt-get install -f
```

Retry the Percona XtraBackup installation.

## Verify the installation

The following command returns the version information.

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