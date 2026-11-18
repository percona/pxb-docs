> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-xtrabackup/9.7/llms.txt).

# Install with the Percona-release Tool on Debian-based Systems

Ready-to-use packages are available from the Percona XtraBackup software repositories and the [Percona Software Downloads](https://www.percona.com/downloads) .

Specific information on the supported platforms, products, and versions is described in [Percona Release Lifecycle Overview](https://www.percona.com/release-lifecycle-overview/) .

## Install Percona XtraBackup through percona-release

Install Percona XtraBackup, like many other Percona products, with the `percona-release` package configuration tool. Run the following commands as root or use the sudo command.

1. Use the apt package manager to download `percona-release`:

   ```
   sudo apt update
   ```

   Expected output

   ```
   Hit:1 http://archive.ubuntu.com/ubuntu noble InRelease
   Hit:2 http://security.ubuntu.com/ubuntu noble-security InRelease
   Hit:3 http://archive.ubuntu.com/ubuntu noble-updates InRelease
   Hit:4 http://archive.ubuntu.com/ubuntu noble-backports InRelease
   Reading package lists... Done
   ```

1. Install the `curl` download utility if it’s not installed:

   ```
   sudo apt install curl
   ```

   Expected output

   ```
   Reading package lists... Done
   Building dependency tree... Done
   Reading state information... Done
   The following additional packages will be installed:
   ...
   Updating certificates in /etc/ssl/certs...
   0 added, 0 removed; done.########################################################...] 
   Running hooks in /etc/ca-certificates/update.d...
   done.
   ```

1. Download the `percona-release` the repository package:

   ```
   curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb
   ```

   Expected output

   ```
   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                   Dload  Upload   Total   Spent    Left  Speed
   100 16510  100 16510    0     0  29915      0 --:--:-- --:--:-- --:--:-- 30127
   ```

1. Install the downloaded package and its dependencies using `apt`:

   ```
   sudo apt install gnupg2 lsb-release ./percona-release_latest.generic_all.deb
   ```

   Expected output

   ```
   Reading package lists... Done
   Building dependency tree... Done
   Reading state information... Done
   ...
   For example, to enable the Percona Distribution for MySQL 9.7 repository use:

     percona-release setup pdps9.7

   Note: To avoid conflicts with older product versions, the percona-release setup command may disable our original repository for some products.

   For more information, please visit:
   https://docs.percona.com/percona-software-repositories/percona-release.html

   Processing triggers for libc-bin (2.35-0ubuntu3.8) ...
   ```

1. Refresh the local cache to update the package information:

   ```
   sudo apt update
   ```

   Expected output

   ```
   Hit:1 http://repo.percona.com/prel/apt noble InRelease
   Hit:2 http://repo.percona.com/telemetry/apt noble InRelease
   Hit:3 http://archive.ubuntu.com/ubuntu noble InRelease
   Hit:4 http://security.ubuntu.com/ubuntu noble-security InRelease
   Hit:5 http://archive.ubuntu.com/ubuntu noble-updates InRelease
   Hit:6 http://archive.ubuntu.com/ubuntu noble-backports InRelease
   Reading package lists... Done
   ```

1. Enable the specific percona-release product.

   ```
   sudo percona-release enable pxb-97-lts
   ```

   Expected output

   ```
   * Enabling the Percona Packaging Repository repository
   Hit:1 http://repo.percona.com/prel/apt noble InRelease
   Get:2 http://repo.percona.com/pxb-97-lts/apt noble InRelease [12.8 kB]
   Hit:3 http://repo.percona.com/telemetry/apt noble InRelease
   Hit:4 http://archive.ubuntu.com/ubuntu noble InRelease
   Hit:5 http://security.ubuntu.com/ubuntu noble-security InRelease
   Hit:6 http://archive.ubuntu.com/ubuntu noble-updates InRelease
   Hit:7 http://archive.ubuntu.com/ubuntu noble-backports InRelease
   Get:8 http://repo.percona.com/pxb-97-lts/apt noble/main Sources [863 B]
   Get:9 http://repo.percona.com/pxb-97-lts/apt noble/main amd64 Packages [3739 B]
   Fetched 17.4 kB in 4s (3907 B/s)
   Reading package lists...
   ```

1. Install Percona XtraBackup.

   ```
   sudo apt install percona-xtrabackup-97
   ```

   Expected output

   ```
   Reading package lists...
   Building dependency tree...
   Reading state information...
   The following additional packages will be installed:
     libaio1t64 libcurl4-openssl-dev libev4t64 libpopt0 lz4 rsync zstd
   Suggested packages:
     libcurl4-doc libidn-dev libkrb5-dev libldap2-dev librtmp-dev libssh2-1-dev
     libssl-dev pkg-config zlib1g-dev openssh-client openssh-server python3
     python3-braceexpand
   The following NEW packages will be installed:
     libaio1t64 libcurl4-openssl-dev libev4t64 libpopt0 lz4 percona-xtrabackup-97
     rsync zstd
   0 upgraded, 8 newly installed, 0 to remove and 2 not upgraded.
   ...
   Setting up percona-xtrabackup-97 (9.7.2~2-1.noble) ...
   Processing triggers for libc-bin (2.39-0ubuntu8.9) ...
   ```

1. Verify the installation.

   ```
   xtrabackup --version
   ```

   Expected output

   ```
   xtrabackup version 9.7.2-2 based on MySQL server 9.7.1 Linux (x86_64) (revision id: b1c9c341)
   ```

1. To decompress backups made using `LZ4` or `ZSTD` compression algorithm, install the corresponding package:

   **Install the lz4 package**

   ```
   sudo apt install lz4
   ```

   **Install the zstd package**

   ```
   sudo apt install zstd
   ```

Note

For AppArmor profile information, see [Working with AppArmor](https://docs.percona.com/percona-xtrabackup/9.7/work-with-apparmor.html).

See also

To install Percona XtraBackup using downloaded deb packages, see [Install Percona XtraBackup 9.7](https://docs.percona.com/percona-xtrabackup/9.7/apt-download-deb.html).

To uninstall Percona XtraBackup, see [Uninstall Percona XtraBackup 9.7](https://docs.percona.com/percona-xtrabackup/9.7/apt-uninstall-xtrabackup.html)
