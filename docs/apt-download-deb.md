# Install with DEB packages

## Version changes

Starting with [Percona XtraBackup 8.0.35-31](release-notes/8.0/8.0.35-31.0.md), the APT builds for the following platforms include ARM packages with the `arm64.deb` extension:

* Debian 12

* Debian 11

* Ubuntu 24.04

* Ubuntu 22.04

* Ubuntu 20.04

This `arm64.deb` extension means Percona XtraBackup is now available for users on ARM-based systems.

We recommend downloading Percona XtraBackup for the same platform as your MySQL-compatible server. For instance, if your server runs on an ARM64 platform, you should download and use the Percona XtraBackup with the `arm64.deb` extension for that operating system.

## Download and install DEB packages

Download `DEB` packages of the desired series for your architecture from the [Percona Software Downloads](https://www.percona.com/downloads). If needed, [Percona Software Download instructions](download-instructions.md) are available. 

This method requires you to resolve all dependencies and install any missing packages. Always back up your data before making significant system changes.

The following example downloads Percona XtraBackup 8.0 release package for Ubuntu 20.04. Run the following commands as root or use the sudo command.
{.power-number}

1. Use `wget` to download the `DEB` package

    ```bash
    wget https://downloads.percona.com/downloads/Percona-XtraBackup-LATEST/Percona-XtraBackup-8.0.26-18/binary/debian/focal/x86_64/percona-xtrabackup-80_8.0.26-18-1.focal_amd64.deb
    ```

2. Install the package

    ```bash
    sudo dpkg -i percona-xtrabackup-80_8.0.26-18-1.focal_amd64.deb
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

```bash
sudo apt-get install -f
```

Retry the Percona XtraBackup installation.

## Verify the installation

The following command returns the version information.

```bash
xtrabackup --version
```

## Troubleshoot the installation

| Issue                         | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| Permission denied              | Ensure you're using sudo or have root access for installation commands.     |
| Repository issues              | If packages are not found, check your yum repository configuration.         |
| Incompatible OS version        | Double-check your OS version matches the package requirements.              |
| Conflicts with existing packages | Consider removing conflicting packages or use a separate environment.     |

If you encounter persistent issues, consult the Percona XtraBackup documentation or [Get help from Percona](get-help.md).
