# Install Percona XtraBackup Pro

--8<--- "pro-build-announcement.md"

This document provides guidelines how to install Pro packages of Percona XtraBackup from Percona repositories. [Check files in packages built for Percona XtraBackup Pro :material-arrow-right:](pro-files.md){.md-button}

## Procedure

!!! note 
    
    Percona XtraBackup 8.4.0-2 Pro build is available for the following platforms:

    * Oracle Linux 9

    * Ubuntu (22.04)

    * Ubuntu (24.04)

    * Debian (12)

1. Request the access to the pro repository from Percona Support. You will receive the client ID and the access token which you use when downloading the packages.

2. Configure the repository and install Percona XtraBackup packages

    === "On Debian or Ubuntu"

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

        6. Enable the specific percona-release product.

            ```{.bash data-prompt="$"}
            $ sudo percona-release enable pxb-84-pro --user_name=<Your PRO repository user name> --repo_token=<Your PRO repository token>
            ```

        7. Install Percona XtraBackup.

            ```{.bash data-prompt="$"}
            $ sudo apt install percona-xtrabackup-pro-84
            ```

        8. Verify the installation.

            ```{.bash data-prompt="$"}
            $ xtrabackup --version
            ```

            ??? example "Expected output"

            ```{.text .no-copy}
            xtrabackup version 8.4.0-2 based on MySQL server 8.4.0 Linux (x86_64) (revision id: da6e1abd)
            ```

        9. To decompress backups made using `LZ4` or `ZSTD` compression algorithm, install the corresponding package:

            === "Install the `lz4` package"

                ```{.bash data-prompt="$"}
                $ sudo apt install lz4
                ```

            === "Install the `zstd` package"

                ```{.bash data-prompt="$"}
                $ sudo apt install zstd
                ```

    === "On RHEL or derivatives"

        1. Install the Percona yum repository by running the following command as the `root` user or with **sudo**: 

            ```{.bash data-prompt="$"}
            $ sudo yum install \
            https://repo.percona.com/yum/percona-release-latest.\
            noarch.rpm
            ```

        2. Enable the repository: 

            ```{.bash data-prompt="$"}
            $ sudo percona-release enable pxb-84-pro --user_name=<Your PRO repository user name> --repo_token=<Your PRO repository token>
            ```

        3. Install Percona XtraBackup:

            ```{.bash data-prompt="$"}
            $ sudo yum install percona-xtrabackup-pro-84
            ```

        4. To decompress backups made using `LZ4` or `ZSTD` compression algorithm, install the corresponding package:

            === "Install the `lz4` package"

                ```{.bash data-prompt="$"}
                $ sudo yum install lz4
                ```

            === "Install the `zstd` package"

                ```{.bash data-prompt="$"}
                $ sudo yum install zstd
                ```
