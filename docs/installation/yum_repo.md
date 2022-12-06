# Install Percona XtraBackup on Red Hat Enterprise Linux and CentOS

Ready-to-use packages are available from the Percona XtraBackup software
repositories and the [download page](https://www.percona.com/downloads/XtraBackup/). The Percona yum repository supports popular `RPM`-based operating systems, including the `Amazon Linux AMI`.

The easiest way to install the Percona Yum repository is to install an `RPM`
that configures yum and installs the [Percona GPG key](https://www.percona.com/downloads/RPM-GPG-KEY-percona).

Specific information on the supported platforms, products, and versions is described in [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).

## What’s in each RPM package?

|Package|Contains|
|--- |--- |
|percona-xtrabackup-80|The latest Percona XtraBackup GA binaries and associated files|
|percona-xtrabackup-80-debuginfo|The debug symbols for binaries in percona-xtrabackup-80|
|percona-xtrabackup-test-80|The test suite for Percona XtraBackup|
|percona-xtrabackup|The older version of the Percona XtraBackup|

## Install Percona XtraBackup from Percona `yum` repository

1. Install the Percona yum repository by running the following command as the `root` user or with **sudo**: 

    ```{.bash data-prompt="$"}
    $ sudo yum install \
    https://repo.percona.com/yum/percona-release-latest.\
    noarch.rpm
    ```

2. Enable the repository: 

    ```{.bash data-prompt="$"}
    $ sudo percona-release enable-only tools release
    ```

    If *Percona XtraBackup* is intended to be used in combination with
    the upstream MySQL Server, you only need to enable the `tools repository: 

    ```{.bash data-prompt="$"}
    $ sudo percona-release enable-only tools
    ```

3. Install *Percona XtraBackup* by running:

    ```{.bash data-prompt="$"}
    $ sudo yum install percona-xtrabackup-80
    ```

    !!! warning

        Make sure that you have the `libev` package installed before installing *Percona XtraBackup* on CentOS 6. For this operating system, the `libev` package is available from the [EPEL](https://fedoraproject.org/wiki/EPEL) repositories.

4. To be able to make compressed backups, install the `qpress` package:

    ```{.bash data-prompt="$"}
    $ yum install qpress
    ```

5. To decompress backups made using `ZSTD` compression algorithm, install the `zstd` package:
    
    ```{.bash data-prompt="$"}
    $ yum install zstd
    ```

!!! admonition "See also"

    To install Percona XtraBackup using downloaded rpm packages, see [Install with package manager](install-with-package-manager.md).

    To uninstall Percona XtraBackup, see [Uninstall Percona XtraBackup](uninstall-percona-xtrabackup.md) 

