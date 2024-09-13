# Install Percona XtraBackup on Red Hat-based systems

Ready-to-use packages are available from the Percona XtraBackup software
repositories and the [download page](https://www.percona.com/downloads/). The Percona yum repository supports popular `RPM`-based operating systems, including the `Amazon Linux AMI`, which has reached its end of life. `Amazon Linux 2` is not supported at this time. 

The easiest way to install the Percona Yum repository is to install an `RPM` that configures yum and installs the [Percona GPG key](https://www.percona.com/downloads/RPM-GPG-KEY-percona).

Specific information on the supported platforms, products, and versions is described in [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).

## Version changes

Starting with [Percona XtraBackup 8.0.35-31], the RPM builds for RHEL 8 and RHEL 9 include ARM packages with the `aarch64.rpm` extension. This extension means Percona XtraBackup is now available for users on ARM-based systems.

We recommend downloading Percona XtraBackup for the same platform as your MySQL-compatible server. For instance, if your server runs on an ARM64 platform, you should download and use the Percona XtraBackup with the `aarch64.rpm` extension for that operating system.

Make sure that you have the `libev` package installed before installing Percona XtraBackup on CentOS 6. For this operating system, the `libev` package is available from [EPEL](https://fedoraproject.org/wiki/EPEL).

## Prerequisites

* Sudo or root access

* Internet connection


## Install from Percona `YUM` repository

The following procedure installs Percona XtraBackup 8.0.
{.power-number}

1. Install the Percona yum repository by running the following command as the `root` user or with sudo: 

    ```{.bash data-prompt="$"}
    $ sudo yum install \
    https://repo.percona.com/yum/percona-release-latest.\
    noarch.rpm
    ```

    ??? example "Example output"

        ```{.text .no-copy}
        Oracle Linux 9 BaseOS Latest (x86_64)                                 6.6 MB/s |  35 MB     00:05
        Oracle Linux 9 Application Stream Packages (x86_64)                   8.5 MB/s |  41 MB     00:04
        Last metadata expiration check: 0:00:06 ago on Mon Sep 23 09:43:33 2024.
        percona-release-latest.noarch.rpm                                      49 kB/s |  27 kB     00:00
        Dependencies resolved.
        ...
        For more information, please visit:
        https://docs.percona.com/percona-software-repositories/percona-release.html


        Verifying        : percona-release-1.0-29.noarch    
                                                    1/1

        Installed:
        percona-release-1.0-29.noarch

        Complete!
        ```

2. Enable the repository: 

    ```{.bash data-prompt="$"}
    $ sudo percona-release enable pxb-80
    ```

    ??? example "Example output"

            ```{.text .no-copy}
            * Enabling the Percona XtraBackup 8.0 repository
            <*> All done!
            ```

3. Install *Percona XtraBackup* by running:

    ```{.bash data-prompt="$"}
    $ sudo yum install percona-xtrabackup-80
    ```

    ??? example "Example output"

        ```{.text .no-copy}
        * Enabling the Percona XtraBackup 8.0 repository
        <*> All done!
        [root@e1dc549c0c65 /]# yum install percona-xtrabackup-80
        PMM2 Client release/x86_64 YUM repository                              13 kB/s | 6.4 kB     00:00
        Percona Release release/noarch YUM repository                         4.3 kB/s | 2.0 kB     00:00
        Percona XtraBackup 8.0 release/x86_64 YUM repository                  363 kB/s | 416 kB     00:01
        Percona Telemetry release/x86_64 YUM repository                       3.1 kB/s | 1.5 kB     00:00
        Dependencies resolved.
        ...

        Complete!
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

## Verify the installation

   Run Percona XtraBackup:

   ```{.bash data-prompt="$"}
   $ xtrabackup --version
   ```

   If this command fails, the installation is incomplete or incorrect.

## Troubleshoot

To troubleshoot a Percona XtraBackup 8.0.x installation on a Red Hat-based system, follow these steps:
{.power-number}

1. This command checks for missing libraries.

    ```{.bash data-prompt="$"}   
    $ ldd $(which xtrabackup) | grep "not found"
    ```

2. Install missing dependencies:


    ```{.bash data-prompt="$"}
    $ sudo yum install <missing-library-name>
    ```

3. Examine log files:

    ```{.bash data-prompt="$"}
    $ sudo journalctl -xe | grep xtrabackup
    ```

4. Ensure the Percona repository is correctly set up:

    ```{.bash data-prompt="$"}
    $ cat /etc/yum.repos.d/percona-release.repo
    ```

5. Update the system to ensure all packages are current:

    ```{.bash data-prompt="$"}
    $ sudo yum update
    ```

6. If issues persist, try a clean reinstall:

    ```{.bash data-prompt="$"}
    $ sudo yum remove percona-xtrabackup-80 
    $ sudo yum clean all 
    $ sudo yum install percona-xtrabackup-80
    ```

7. SELinux might block XtraBackup. Check its status:

    ```{.bash data-prompt="$"} 
    $ getenforce
    ```

8. Set SELinux to permissive temporarily:

    ```{.bash data-prompt="$"} 
    $ sudo setenforce 0
    ```

9. Create a backup to verify functionality:

     ```{.bash data-prompt="$"} 
     $ xtrabackup --backup --target-dir=/tmp/test_backup
     ```

If problems continue, gather all error messages and logs, then consult Percona's documentation or support forums for further assistance.

!!! admonition "See also"

    To install Percona XtraBackup using downloaded rpm packages, see [Install with package manager](yum-download-rpm.md).

    To uninstall Percona XtraBackup, see [Uninstall Percona XtraBackup](yum-uninstall-xtrabackup.md) 

[Percona XtraBackup 8.0.35-31]: release-notes/8.0/8.0.35-31.0.md
[EPEL]: https://fedoraproject.org/wiki/EPEL