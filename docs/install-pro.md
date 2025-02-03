# Install Percona XtraBackup Pro

--8<--- "pro-build-announcement.md"

This document provides guidelines how to install Pro packages of Percona XtraBackup from Percona repositories. [Check files in packages built for Percona XtraBackup Pro :material-arrow-right:](pro-files.md){.md-button}

## Install Amazon Linux 2023

!!! note 
    
    Percona XtraBackup 8.0.35-32 Pro build is available for the following platforms:
    
    * Amazon Linux 2023 (AL2023) - We support both AMD64 and ARM64 versions of Amazon Linux 2023.
    
1. Request the access to the pro repository from Percona Support. You will receive the client ID and the access token which you use when downloading the packages.

2. Install the Percona dnf repository by running the following command as the `root` user or with **sudo**: 

    ```{.bash data-prompt="$"}
    $ sudo dnf install \
    https://repo.percona.com/dnf/percona-release-latest.\
    noarch.rpm
    ```

3. Enable the repository: 

    ```{.bash data-prompt="$"}
    $ sudo percona-release enable pxb-80-pro --user_name=<Your PRO repository user name> --repo_token=<Your PRO repository token>
    ```

3. Install Percona XtraBackup:

    ```{.bash data-prompt="$"}
    $ sudo dnf install percona-xtrabackup-pro-80
    ```

4. To decompress backups made using `LZ4` or `ZSTD` compression algorithm, install the corresponding package:

=== "Install the `lz4` package"

    ```{.bash data-prompt="$"}
    $ sudo dnf install lz4
    ```

=== "Install the `zstd` package"

    ```{.bash data-prompt="$"}
    $ sudo dnf install zstd
    ```