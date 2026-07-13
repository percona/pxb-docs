# Install using downloaded DEB packages

Download `DEB` packages of the desired series for your architecture from the [Percona Software Downloads :octicons-link-external-16:](https://www.percona.com/downloads). If needed, [Percona Software Download instructions](download-instructions.md) are available. 

This method requires you to resolve all dependencies and install any missing packages. Always back up your data before making significant system changes.

The following example downloads Percona XtraBackup {{release}} release package for Ubuntu 22.04. Run the following commands as root or use the sudo command.
{.power-number}

1. Use `wget` to download the `DEB` package:

    ```shell
    wget https://downloads.percona.com/downloads/Percona-XtraBackup-{{vers}}/Percona-XtraBackup-{{release}}/binary/debian/jammy/x86_64/percona-xtrabackup-97_{{release}}-1.jammy_amd64.deb
    ```

2. Install Percona XtraBackup by using `dpkg`:

    ```shell
    sudo dpkg -i percona-xtrabackup-97_{{release}}-1.jammy_amd64.deb
    ```

## Common dependencies

| Library Name    | Description                                                                                              |
|-----------------|----------------------------------------------------------------------------------------------------------|
| libmysqlclient  | A client library for MySQL, providing essential functions for connecting to and communicating with MySQL databases. |
| libssl          | A cryptographic library used for implementing SSL/TLS encryption, necessary for secure data transmission. |
| libcurl         | A library that enables data transfer via various protocols such as HTTP, FTP, and others, commonly used for handling web requests. |
| libev           | A high-performance event-loop library, often used in network applications for handling asynchronous events efficiently. |
| libgcrypt       | A general-purpose cryptographic library that provides encryption, decryption, and cryptographic hashing algorithms. |
| zlib            | A compression library used for data compression and decompression, supporting the popular DEFLATE compression algorithm. |

If there are missing dependencies, `dpkg` shows error messages. Install any missing packages with the following command:

```shell
sudo apt-get install -f
```
Retry the Percona XtraBackup installation.

## Verify the installation

After installation, verify it by checking the version:

```shell
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
