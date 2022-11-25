# Install Percona XtraBackup on Debian and Ubuntu

Ready-to-use packages are available from the Percona XtraBackup software
repositories and the [download page](https://www.percona.com/downloads/XtraBackup/).

Specific information on the supported platforms, products, and versions is
described in [Percona Release Lifecycle Overview](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).

!!! important

    To prevent intermittent backup failures, [update the curl utility in Debian 10](../xbcloud/update-curl-utility.md).

## What’s in each DEB package?

|Package|Contains|
|--- |--- |
|percona-xtrabackup-80|The latest Percona XtraBackup GA binaries and associated files|
|percona-xtrabackup-dbg-80|The debug symbols for binaries in `percona-xtrabackup-80`|
|percona-xtrabackup-test-80|The test suite for Percona XtraBackup|
|percona-xtrabackup|The older version of the Percona XtraBackup|

## Install Percona XtraBackup through percona-release

Percona XtraBackup, like many other Percona products, is installed
with the *percona-release* package configuration tool.

1. Download a deb package for *percona-release* the repository packages
    from Percona web:

    ```{.bash data-prompt="$"}
    $ wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb
    ```

2. Install the downloaded package with **dpkg**. To do that, run the
    following commands as root or with **sudo**: `dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb`
   
    Once you install this package the Percona repositories should be added. You
    can check the repository setup in the
    `/etc/apt/sources.list.d/percona-release.list` file.

3. Enable the repository: `percona-release enable-only tools release`

    If *Percona XtraBackup* is intended to be used in combination with
    the upstream MySQL Server, you only need to enable the `tools`
    repository: `percona-release enable-only tools`.

4. Remember to update the local cache: `apt update`


5. After that you can install the `percona-xtrabackup-80` package:

    ```{.bash data-prompt="$"}
    $ sudo apt install percona-xtrabackup-80
    ```

6. To make compressed backups, install the `qpress` package:

    ```{.bash data-prompt="$"}
    $ sudo apt install qpress
    ```

7. To decompress backups made using `ZSTD` compression algorithm, install the `zstd` package:
    
    ```{.bash data-prompt="$"}
    $ sudo apt install zstd
    ```

!!! note
 
    For AppArmor profile information, see [Working with AppArmor](https://docs.percona.com/percona-xtrabackup/8.0/security/pxb-apparmor.html).

## Apt-pin the packages

In some cases you might need to “pin” the selected packages to avoid the
upgrades from the distribution repositories. Make a new file
`/etc/apt/preferences.d/00percona.pref` and add the following lines in it:

```
Package: *
Pin: release o=Percona Development Team
Pin-Priority: 1001
```

For more information about the pinning, check the official [debian wiki](http://wiki.debian.org/AptPreferences).

!!! admonition "See also"

    To install Percona XtraBackup using downloaded deb packages, see [Install with package manager](install-with-package-manager.md).

    To uninstall Percona XtraBackup, see [Uninstall Percona XtraBackup](uninstall-percona-xtrabackup.md)

