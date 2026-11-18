> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-xtrabackup/8.4/llms.txt).

# Use a YUM repository to install Percona XtraBackup

Ready-to-use packages are available from the Percona XtraBackup software repositories and the [Percona Software Downloads](https://www.percona.com/downloads) . The Percona yum repository supports popular `RPM`-based operating systems, including the `Amazon Linux AMI`.

Specific information on the supported platforms, products, and versions is described in [Percona Software and Platform Lifecycle](https://www.percona.com/release-lifecycle-overview/#mysql) .

## Install Percona XtraBackup from Percona `yum` repository

To install Percona XtraBackup from Percona `yum` repository, do the following steps:

1. Install the Percona yum repository by running the following command as the `root` user or with **sudo**:

   ```
   sudo yum install \
   https://repo.percona.com/yum/percona-release-latest.\
   noarch.rpm
   ```

   Expected output

   ```
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

1. Enable the repository:

   ```
   sudo percona-release enable pxb-84-lts
   ```

   Expected output

   ```
   * Enabling the Percona Packaging Repository repository
   <*> All done!
   ```

1. Install Percona XtraBackup.

   ```
   sudo yum install percona-xtrabackup-84
   ```

   Expected output

   ```
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

1. Verify the installation.

   ```
   xtrabackup --version
   ```

   Expected output

   ```
   xtrabackup version 8.4.0-7 based on MySQL server 8.4.0 Linux (x86_64) (revision id: 4093cfd8)
   ```

1. To decompress backups made using `LZ4` or `ZSTD` compression algorithm, install the corresponding package:

   **Install the lz4 package**

   ```
   sudo yum install lz4
   ```

   **Install the zstd package**

   ```
   sudo yum install zstd
   ```

See also

To install Percona XtraBackup using downloaded rpm packages, see [Install with package manager](https://docs.percona.com/percona-xtrabackup/8.4/yum-download-rpm.html).

To uninstall Percona XtraBackup, see [Uninstall Percona XtraBackup](https://docs.percona.com/percona-xtrabackup/8.4/yum-uninstall-xtrabackup.html)
