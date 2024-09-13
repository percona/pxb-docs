# Install Percona XtraBackup on Debian-based systems

Ready-to-use packages are available from the Percona XtraBackup software
repositories and the [download page](https://www.percona.com/downloads).

Specific information on the supported platforms, products, and versions is
described in [Percona Release Lifecycle Overview](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).

To prevent intermittent backup failures, [update the curl utility in Debian 10](update-curl-utility.md).

This guide walks you through the process of installing Percona XtraBackup 8.0 on Debian-based systems using the Percona-release tool.

## Version changes

Starting with [Percona XtraBackup 8.0.35-31], the APT builds for the following platforms include ARM packages with the `arm64.deb` extension:

* Debian 12

* Debian 11

* Ubuntu 24.04

* Ubuntu 22.04

* Ubuntu 20.04

This extension means Percona XtraBackup is now available for users on ARM-based systems.

We recommend downloading Percona XtraBackup for the same platform as your MySQL-compatible server. For instance, if your server runs on an ARM64 platform, you should download and use the Percona XtraBackup with the `arm64.deb` extension for that operating system.

## Prerequisites

* Sudo or root access

* Internet connection

## Installation steps

The following procedure installs Percona XtraBackup 8.0.
{.power-number}

1. Update the system package list

    ```{.bash data-prompt="$"}
    $ sudo apt update
    ```

    ??? example "Example output"

        ```{.text .no-copy}
        Get:1 http://ports.ubuntu.com/ubuntu-ports jammy InRelease [270 kB]
        Get:2 http://ports.ubuntu.com/ubuntu-ports jammy-updates InRelease [128 kB]
        Get:3 http://ports.ubuntu.com/ubuntu-ports jammy-backports InRelease [127 kB]
        Get:4 http://ports.ubuntu.com/ubuntu-ports jammy-security InRelease [129 kB]
        Get:5 http://ports.ubuntu.com/ubuntu-ports jammy/restricted arm64 Packages [24.2 kB]
        Get:6 http://ports.ubuntu.com/ubuntu-ports jammy/multiverse arm64 Packages [224 kB]
        Get:7 http://ports.ubuntu.com/ubuntu-ports jammy/universe arm64 Packages [17.2 MB]
        Get:8 http://ports.ubuntu.com/ubuntu-ports jammy/main arm64 Packages [1758 kB]
        Get:9 http://ports.ubuntu.com/ubuntu-ports jammy-updates/restricted arm64 Packages [2400 kB]
        Get:10 http://ports.ubuntu.com/ubuntu-ports jammy-updates/multiverse arm64 Packages [29.5 kB]
        Get:11 http://ports.ubuntu.com/ubuntu-ports jammy-updates/universe arm64 Packages [1379 kB]
        Get:12 http://ports.ubuntu.com/ubuntu-ports jammy-updates/main arm64 Packages [2217 kB]
        Get:13 http://ports.ubuntu.com/ubuntu-ports jammy-backports/universe arm64 Packages [31.8 kB]
        Get:14 http://ports.ubuntu.com/ubuntu-ports jammy-backports/main arm64 Packages [81.0 kB]
        Get:15 http://ports.ubuntu.com/ubuntu-ports jammy-security/main arm64 Packages [1949 kB]
        Get:16 http://ports.ubuntu.com/ubuntu-ports jammy-security/restricted arm64 Packages [2330 kB]
        Get:17 http://ports.ubuntu.com/ubuntu-ports jammy-security/multiverse arm64 Packages [24.1 kB]
        Get:18 http://ports.ubuntu.com/ubuntu-ports jammy-security/universe arm64 Packages [1096 kB]
        Fetched 31.4 MB in 7s (4264 kB/s)
        Reading package lists... Done
        Building dependency tree... Done
        Reading state information... Done
        9 packages can be upgraded. Run 'apt list --upgradable' to see them.
        ```


2. Install the curl download utility if it's not installed:

    ```{.bash data-prompt="$"}
    $ sudo apt install curl
    ```

    ??? example "Example output"

        ```{.text .no-copy}
        Reading package lists... Done
        Building dependency tree... Done
        Reading state information... Done
        The following additional packages will be installed:
          ca-certificates libbrotli1 libcurl4 libldap-2.5-0 libldap-common libnghttp2-14 libpsl5 librtmp1
        Suggested packages:
        ...
        Updating certificates in /etc/ssl/certs...
        0 added, 0 removed; done.######################################################################...]
        Running hooks in /etc/ca-certificates/update.d...
        done.
        ```

3. Download the percona-release the repository package:

    ```{.bash data-prompt="$"}
    $ curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb
    ```

    ??? example "Example output"

        ```{.text .no-copy}
        % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                        Dload  Upload   Total   Spent    Left Speed
        100 16510  100 16510    0     0  31433      0 --:--:-- --:--:-- --:--:-- 31447
        ```

4. Install the downloaded package and its dependencies using apt:

    ```{.bash data-prompt="$"}
    $ sudo apt install gnupg2 lsb-release ./percona-release_latest.generic_all.deb
    ```

    ??? example "Example output"

        ```{.text .no-copy}
        Reading package lists... Done
        Building dependency tree... Done
        Reading state information... Done
        Note, selecting 'percona-release' instead of './percona-release_latest.generic_all.deb'
        The following additional packages will be installed:
        ```


5. Refresh the local cache to update the package information:

    ```{.bash data-prompt="$"}
    $ sudo apt update
    ```

    ??? example "Example output"

        ```{.text .no-copy}
        Hit:1 http://repo.percona.com/pmm2-client/apt jammy InRelease
        Hit:2 http://ports.ubuntu.com/ubuntu-ports jammy InRelease
        Hit:3 http://repo.percona.com/prel/apt jammy InRelease
        ...
        ```

6. Enable the repository:

    ```{.bash data-prompt="$"}
    $ percona-release setup pxb-80
    ```
    ??? example "Example output"

        ```{.text .no-copy}
        * Disabling all Percona Repositories
        * Enabling the Percona XtraBackup 8.0 repository
        Hit:1 http://repo.percona.com/prel/apt jammy InRelease
        Get:2 http://repo.percona.com/pxb-80/apt jammy InRelease [18.7 kB]
        Hit:3 http://ports.ubuntu.com/ubuntu-ports jammy InRelease
        Get:4 http://ports.ubuntu.com/ubuntu-ports jammy-updates InRelease [128 kB]
        Hit:5 http://repo.percona.com/telemetry/apt jammy InRelease
        Get:6 http://repo.percona.com/pxb-80/apt jammy/main Sources [3393 B]
        Get:7 http://ports.ubuntu.com/ubuntu-ports jammy-backports InRelease [127 kB]
        Get:8 http://ports.ubuntu.com/ubuntu-ports jammy-security InRelease [129 kB]
        Fetched 406 kB in 1s (274 kB/s)
        Reading package lists... Done
        ```

7. Install the package:

    ```{.bash data-prompt="$"}
    $ sudo apt install percona-xtrabackup-80
    ```

    ??? example "Example output"

        ```{.text .no-copy}

        Reading package lists... Done
        Building dependency tree... Done
        Reading state information... Done
        The following additional packages will be installed:
          libaio1 libcurl4-openssl-dev libdbd-mysql-perl libdbi-perl libev4 libgdbm-compat4 libgdbm6
          libmysqlclient21 libperl5.34 libpopt0 mysql-common netbase perl perl-modules-5.34 rsync zstd
        ...
        Setting up libdbd-mysql-perl:amd64 (4.050-5ubuntu0.22.04.1) ...##########################.........]
        Setting up percona-xtrabackup-80 (8.0.35-31-1.jammy) ...####################################......]
        Processing triggers for libc-bin (2.35-0ubuntu3.8) ...########################################....]
        ```

9. Verify the installation:

    ```{.bash data-prompt="$"}
    $ xtrabackup --version
    ```

    ??? example "Example output"

        ```{.text .no-copy}
        xtrabackup version 8.0.35-31 based on MySQL server 8.0.35 Linux (x86_64) (revision id: 55ec21d7)
        ```

8. Install optional compression packages if you plan to use LZ4 or ZSTD compression:

    === "Install the `lz4` package"

        ```{.bash data-prompt="$"}
        $ sudo apt install lz4
        ```

    === "Install the `zstd` package"

        ```{.bash data-prompt="$"}
        $ sudo apt install zstd
        ```

## Troubleshooting

If you encounter any errors during the installation process, check your system's error logs:

```{.bash data-prompt="$"}
$ sudo tail -n 50 /var/log/syslog
```

Ensure your system meets the minimum requirements for Percona XtraBackup. 

If you encounter permission errors, ensure you're running the commands with `sudo` or have root access.

For AppArmor profile information, see [Working with AppArmor](work-with-apparmor.md).


!!! admonition "Additional resources"

    To install Percona XtraBackup using downloaded deb packages, see [Install Percona XtraBackup 8.0](apt-download-deb.md).

    To uninstall Percona XtraBackup, see [Uninstall Percona XtraBackup 8.0](apt-uninstall-xtrabackup.md)

[Percona XtraBackup 8.0.35-31]: release-notes/8.0/8.0.35-31.0.md