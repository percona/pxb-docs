# Install with package manager

This document demonstrates how to install Percona XtraBackup using downloaded packages.

=== "On Debian / Ubuntu"

    Download deb packages of the desired series for your architecture
    from [Download Percona XtraBackup 8.0](https://www.percona.com/downloads/XtraBackup/). The following
    example downloads *Percona XtraBackup* 8.0.26-18 release package for Ubuntu
    20.04:

    ```{.bash data-prompt="$"}
    $ wget https://downloads.percona.com/downloads/Percona-XtraBackup-LATEST/Percona-XtraBackup-8.0.26-18/binary/debian/focal/x86_64/percona-xtrabackup-80_8.0.26-18-1.focal_amd64.deb
    ```

    Install Percona XtraBackup by running:

    ```{.bash data-prompt="$"}
    $ sudo dpkg -i percona-xtrabackup-80_8.0.26-18-1.focal_amd64.deb
    ```

    When installing packages manually like this, resolve all the dependencies and install missing packages yourself.


=== "On Red Hat Enterprise Linux / CentOS"

    Download rpm packages of the desired series for your architecture from the
    [download page](https://www.percona.com/downloads/XtraBackup/). The following
    example downloads *Percona XtraBackup* 8.0.4 release package for *CentOS* 7:

    ```{.bash data-prompt="$"}
    $ wget https://www.percona.com/downloads/XtraBackup/Percona-XtraBackup-8.0.4/binary/redhat/7/x86_64/percona-xtrabackup-80-8.0.4-1.el7.x86_64.rpm
    ```

    Now you can install *Percona XtraBackup* by running `yum localinstall`:

    ```{.bash data-prompt="$"}
    $ yum localinstall percona-xtrabackup-80-8.0.4-1.el7.x86_64.rpm
    ```

    When installing packages manually like this, you’ll need to make sure to resolve all the dependencies and install missing packages yourself.


!!! admonition "See also"
    
    To uninstall Percona XtraBackup, see [Uninstall Percona XtraBackup](uninstall-percona-xtrabackup.md).


