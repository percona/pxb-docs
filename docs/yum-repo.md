# Use a YUM repository to install Percona XtraBackup

Ready-to-use packages are available from the Percona XtraBackup software
repositories and the [Percona Software Downloads :octicons-link-external-16:](https://www.percona.com/downloads). The Percona yum repository supports popular `RPM`-based operating systems, including the `Amazon Linux AMI`.

Specific information on the supported platforms, products, and versions is described in [Percona Software and Platform Lifecycle :octicons-link-external-16:](https://www.percona.com/release-lifecycle-overview/#mysql).

<!--

### Percona XtraBackup PRO 

This document provides guidelines on how to install Percona XtraBackup PRO packages from the Percona repositories.

--8<--- "pro-build-announcement.md"

[Percona XtraBackup Pro on Amazon Linux 2023 installation](install-pro.md){.md-button}

-->

## Install Percona XtraBackup from Percona `yum` repository

To install Percona XtraBackup from Percona `yum` repository, do the following steps:
{.power-number}

1. Install the Percona yum repository by running the following command as the `root` user or with **sudo**: 

    ```shell
    sudo yum install \
    https://repo.percona.com/yum/percona-release-latest.\
    noarch.rpm
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Oracle Linux 9 BaseOS Latest (x86_64)           8.4 MB/s |  43 MB     00:05    
        Oracle Linux 9 Application Stream Packages (x86 8.6 MB/s |  47 MB     00:05    
        Last metadata expiration check: 0:00:06 ago on Wed Dec 11 14:12:54 2024.
        percona-release-latest.noarch.rpm                62 kB/s |  27 kB     00:00    
        Dependencies resolved.
        ...
        For more information, please visit:
        https://docs.percona.com/percona-software-repositories/percona-release.html


        Verifying        : percona-release-1.0-29.noarch                          1/1 

        Installed:
        percona-release-1.0-29.noarch                                                 

        Complete!
        ```

2. Enable the repository: 

    ```shell
    sudo percona-release enable pxb-84-lts
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        * Enabling the Percona Packaging Repository repository
        <*> All done!
        ```

3. Install Percona XtraBackup.

    ```shell
    sudo yum install percona-xtrabackup-84
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Percona Release release/noarch YUM repository    16 kB/s | 2.8 kB     00:00
        Percona Packaging Repository release/x86_64 YUM 971 kB/s | 371 kB     00:00
        Percona Telemetry release/x86_64 YUM repository  35 kB/s | 5.4 kB     00:00
        Dependencies resolved.
        ...
        Installing:
         percona-xtrabackup-84    x86_64  8.4.0-7.1.el9       pxb-84-lts-release-x86_64   38 M
        ...
        Complete!
        ```
        
4. Verify the installation.

    ```shell
    xtrabackup --version
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        xtrabackup version {{release}} based on MySQL server 8.4.0 Linux (x86_64) (revision id: 4093cfd8)
        ```

5. To decompress backups made using `LZ4` or `ZSTD` compression algorithm, install the corresponding package:

    === "Install the `lz4` package"

        ```shell
        sudo yum install lz4
        ```

    === "Install the `zstd` package"

        ```shell
        sudo yum install zstd
        ```

!!! admonition "See also"

    To install Percona XtraBackup using downloaded rpm packages, see [Install with package manager](yum-download-rpm.md).

    To uninstall Percona XtraBackup, see [Uninstall Percona XtraBackup](yum-uninstall-xtrabackup.md) 

