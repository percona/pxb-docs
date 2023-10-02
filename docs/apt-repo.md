# Install with an APT repository

Ready-to-use packages are available from the Percona XtraBackup software
repositories and the [download page](https://www.percona.com/downloads).

Specific information on the supported platforms, products, and versions is
described in [Percona Release Lifecycle Overview](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).

## Install Percona XtraBackup through percona-release

Percona XtraBackup, like many other Percona products, is installed with the *percona-release* package configuration tool.
{.power-number}

1. Download a `DEB` package for *percona-release* the repository packages from Percona web:

    ```{.bash data-prompt="$"}
    $ wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb
    ```

2. Install the downloaded package with **dpkg**. To do that, run the following commands as root or with **sudo**: `dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb`
   
    Once you install this package the Percona repositories should be added. You
    can check the repository setup in the `/etc/apt/sources.list.d/percona-release.list` file.

3. Enable the repository: `percona-release enable-only tools release`

    If *Percona XtraBackup* is intended to be used in combination with
    the upstream MySQL Server, you only need to enable the `tools`
    repository: `percona-release enable-only tools`.

4. Refresh the local cache to update the package information:

    ```{.bash data-prompt="$"}
    $ sudo apt update
    ```

5. Install the `percona-xtrabackup-81` package:

    ```{.bash data-prompt="$"}
    $ sudo apt install percona-xtrabackup-81
    ```

6. To decompress backups made using `LZ4` or `ZSTD` compression algorithm, install the corresponding package:

    === "Install the `lz4` package"

        ```{.bash data-prompt="$"}
        $ sudo apt install lz4
        ```

    === "Install the `zstd` package"

        ```{.bash data-prompt="$"}
        $ sudo apt install zstd
        ```

!!! note
 
    For AppArmor profile information, see [Working with AppArmor](work-with-apparmor.md).


!!! admonition "See also"

    To install Percona XtraBackup using downloaded deb packages, see [Install Percona XtraBackup {{release}}](apt-download-deb.md).

    To uninstall Percona XtraBackup, see [Uninstall Percona XtraBackup {{release}}](apt-uninstall-xtrabackup.md)

