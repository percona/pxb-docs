# Installing Percona XtraBackup on Red Hat Enterprise Linux and CentOS

!!! note

    The following instructions install Percona XtraBackup 2.4 using the YUM package manager. The instructions to install Percona XtraBackup 8.0 using the YUM package manager are available in the [Percona XtraBackup 8.0 installation documentation](https://docs.percona.com/percona-xtrabackup/8.0/installation/yum_repo.html).

Ready-to-use packages are available from the *Percona XtraBackup* software
repositories and the [download page](https://www.percona.com/downloads/). The Percona
`yum` repository supports popular *RPM*-based operating systems,
including the *Amazon Linux AMI*.

The easiest way to install the *Percona Yum* repository is to install an *RPM*
that configures `yum` and installs the [Percona GPG key](https://repo.percona.com/yum/PERCONA-PACKAGING-KEY).

Specific information on the supported platforms, products, and versions is described in [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).

## What’s in each RPM package?

The `percona-xtrabackup-24` package contains the latest *Percona XtraBackup*
GA binaries and associated files.

The `percona-xtrabackup-24-debuginfo` package contains the debug symbols for
binaries in `percona-xtrabackup-24`.

The `percona-xtrabackup-test-24` package contains the test suite for *Percona XtraBackup*.

The `percona-xtrabackup` package contains the older version of the
*Percona XtraBackup*.

## Installing *Percona XtraBackup* from Percona `yum` repository

1. Install the `percona-release` configuration tool

    You can install the yum repository for percona-release
    by running the following command as a `root` user or with
    `sudo`:

    ```shell
    $ yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
    ```

    You should see some output such as the following:

    ```text
    Retrieving https://repo.percona.com/yum/percona-release-latest.noarch.rpm
    Preparing...                ########################################### [100%]
       1:percona-release        ########################################### [100%]
    ```

    !!! note

        *RHEL*/*Centos* 5 doesn’t support installing the packages directly from the remote location so you’ll need to download the package first and install it manually with rpm:

    ```shell
    $ wget https://repo.percona.com/yum/percona-release-latest.noarch.rpm
    $ rpm -ivH percona-release-latest.noarch.rpm
    ```

2. Testing the repository

    Make sure packages are now available from the repository, by executing the
    following command:

    ```shell
    $ yum list | grep percona
    ```

    You should see output similar to the following:

    ```text
    ...
    percona-xtrabackup-20.x86_64               2.0.8-587.rhel5             percona-release-x86_64
    percona-xtrabackup-20-debuginfo.x86_64     2.0.8-587.rhel5             percona-release-x86_64
    percona-xtrabackup-20-test.x86_64          2.0.8-587.rhel5             percona-release-x86_64
    percona-xtrabackup-21.x86_64               2.1.9-746.rhel5             percona-release-x86_64
    percona-xtrabackup-21-debuginfo.x86_64     2.1.9-746.rhel5             percona-release-x86_64
    percona-xtrabackup-22.x86_64               2.2.13-1.el5                percona-release-x86_64
    percona-xtrabackup-22-debuginfo.x86_64     2.2.13-1.el5                percona-release-x86_64
    percona-xtrabackup-debuginfo.x86_64        2.3.5-1.el5                 percona-release-x86_64
    percona-xtrabackup-test.x86_64             2.3.5-1.el5                 percona-release-x86_64
    percona-xtrabackup-test-21.x86_64          2.1.9-746.rhel5             percona-release-x86_64
    percona-xtrabackup-test-22.x86_64          2.2.13-1.el5                percona-release-x86_64
    ...
    ```

3. Enable the repository: `percona-release enable-only tools release`

    If *Percona XtraBackup* is intended to be used in combination with
    the upstream MySQL Server, you only need to enable the `tools`
    repository: `percona-release enable-only tools`.

4. Install *Percona XtraBackup* by running:  `yum install percona-xtrabackup-24`

    !!! warning

        In order to successfully install *Percona XtraBackup* on CentOS prior to version 7, the `libev` package needs to be installed first. This package `libev` package can be installed from the [EPEL](https://fedoraproject.org/wiki/EPEL) repositories.

## Percona `yum` Testing Repository

Percona offers pre-release builds from our testing repository. To subscribe to
the testing repository, you’ll need to enable the testing repository in
/etc/yum.repos.d/percona-release.repo. To do so, set both
`percona-testing-$basearch` and `percona-testing-noarch` to
`enabled = 1` (Note that there are 3 sections in this file: release, testing
and experimental - in this case it is the second section that requires
updating). 

!!! note

    You’ll need to install the Percona repository first (ref above) if this hasn’t been done already.

1. To be able to make compressed backups, install the `qpress` package:
   
    ```shell
    $ yum install qpress
    ```

    !!! admonition "See also"

        [Compressed Backup](../backup_scenarios/compressed_backup.md#compressed-backup)

## Installing *Percona XtraBackup* using downloaded rpm packages

Download the packages of the desired series for your architecture from the
[download page](https://www.percona.com/downloads). Following
example will download *Percona XtraBackup* 2.4.28 release package for
*CentOS* 9:

```shell
$ wget https://downloads.percona.com/downloads/Percona-XtraBackup-2.4/\
Percona-XtraBackup-2.4.28/binary/redhat/9/x86_64/percona-xtrabackup-24-2.4.28-1.el9.x86_64.rpm
```

Now you can install *Percona XtraBackup* by running:

```shell
$ yum localinstall percona-xtrabackup-24-2.4.28-1.el9.x86_64.rpm
```

!!! note

    When installing packages manually like this, you'll need to make sure to resolve all the dependencies and install missing packages yourself.

## Uninstalling *Percona XtraBackup*

To completely uninstall *Percona XtraBackup* you’ll need to remove all the
installed packages.

Remove the packages

```shell
yum remove percona-xtrabackup
```

<script>
    (function(h,o,t,j,a,r){
        h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
        h._hjSettings={hjid:3857510,hjsv:6};
        a=o.getElementsByTagName('head')[0];
        r=o.createElement('script');r.async=1;
        r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
        a.appendChild(r);
    })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
</script>