# Install with the Percona-release Tool on Debian-based Systems

Ready-to-use packages are available from the Percona XtraBackup software
repositories and the [download page].

Specific information on the supported platforms, products, and versions is
described in [Percona Release Lifecycle Overview].

## Install Percona XtraBackup through percona-release

Install Percona XtraBackup, like many other Percona products, with the percona-release package configuration tool.
{.power-number}

1. Use the apt package manager to dowload `percona-release`:

    ```{.bash data-prompt="$"}
    $ sudo apt update
    ```

2. Install the `curl` download utility if it's not installed:

    ```{.bash data-prompt="$"}
    $ sudo apt install curl
    ```
  

3. Download the `percona-release` the repository package:

    ```{.bash data-prompt="$"}
    $ curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb
    ```

    
4. Install the downloaded package and its dependencies using `apt`:

    ```{.bash data-prompt="$"}
    sudo apt install gnupg2 lsb-release ./percona-release_latest.generic_all.deb
    ```
5. Refresh the local cache to update the package information:

    ```{.bash data-prompt="$"}
    $ sudo apt update
    ```
2. Install the downloaded package with **dpkg**. To do that, run the following commands as root or with **sudo**: `dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb`
   

percona-release enable pxb-80 release
percona-release show
percona-release setup pxb80
percona-release apt install percona-xtrabackup (This produced an error: Unknown action specified: apt)
percona-release apt install -y percona-xtrabackup-pxb-80 (This produced an error: Unknown action specified: apt)
apt -y install percona-xtrabackup-80

5. Install the `percona-xtrabackup-{{pkg}}` package:

    ```{.bash data-prompt="$"}
    $ sudo apt install percona-xtrabackup-{{pkg}}
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

    To install Percona XtraBackup using downloaded deb packages, see [Install Percona XtraBackup {{vers}}](apt-download-deb.md).

    To uninstall Percona XtraBackup, see [Uninstall Percona XtraBackup {{vers}}](apt-uninstall-xtrabackup.md)

[download page]: https://www.percona.com/downloads
[Percona Release Lifecycle Overview]: https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql