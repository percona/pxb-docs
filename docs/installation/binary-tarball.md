# Installing Percona XtraBackup from a Binary Tarball

!!! note

    The following instructions install Percona XtraBackup 2.4 by downloading and installing a binary tarball. The instructions to install Percona XtraBackup 8.0 by the same method are available in the [Percona XtraBackup 8.0 installation documentation](https://docs.percona.com/percona-xtrabackup/8.0/installation/binary-tarball.html).

Percona provides binary tarballs of Percona XtraBackup. Binary tarballs contain pre-compiled executables, libraries, and other dependencies and are compressed `tar` archives. Extract the binary tarballs to any path.

Binary tarballs are available for [download](https://www.percona.com/downloads/Percona-XtraBackup-2.4/LATEST/) and installation. The following table lists the tarballs available in `Linux - Generic`. Select the *Percona XtraBackup* 2.4 version number and the type of tarball for your installation. Binary tarballs support all distributions.

After you have downloaded the binary tarballs, extract the tarball in the file location of your choice.

| Type    | Name                                                       | Description                                                                        |
| ------- | ---------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Full    | percona-xtrabackup--Linux.x86_64.glibc2.12.tar.gz          | Contains binaries, libraries, test files, and debug symbols                        |
| Minimal | percona-xtrabackup--Linux.x86_64.glibc2.12-minimal.tar.gz  | Contains binaries, and libraries but does not include test files, or debug symbols |

Fetch and extract the correct binary tarball. For example, the following downloads the full tarball for version 2.4.24:

You may need to update the apt repositories and then install `wget`.

```shell
$ apt update
$ apt install wget
```

```shell
$ wget wget https://downloads.percona.com/downloads/Percona-XtraBackup-2.4/Percona-XtraBackup-2.4.27/binary/tarball/percona-xtrabackup-2.4.27-Linux-x86_64.glibc2.12.tar.gz
```
??? example "Expected results"
    ```text
      --2022-12-06 17:01:29--  https://downloads.percona.com/downloads/Percona-XtraBackup-2.4/Percona-XtraBackup-2.4.27/binary/tarball/percona-xtrabackup-2.4.27-Linux-x86_64.glibc2.12.tar.gz
      Resolving downloads.percona.com (downloads.percona.com)... 74.121.199.231, 162.220.4.221, 162.220.4.222
      Connecting to downloads.percona.com (downloads.percona.com)|74.121.199.231|:443... connected.
      HTTP request sent, awaiting response... 200 OK
      Length: 77216741 (74M) [application/x-gzip]
      Saving to: 'percona-xtrabackup-2.4.27-Linux-x86_64.glibc2.12.tar.gz'
    ```

Uncompress the file:

```shell
$ tar xvf percona-xtrabackup-2.4.27-Linux-x86_64.glibc2.12.tar.gz
```
??? example "Expected results"
    ```text
    percona-xtrabackup-2.4.27-Linux-x86_64.glibc2.12/
    percona-xtrabackup-2.4.27-Linux-x86_64.glibc2.12/man/
    percona-xtrabackup-2.4.27-Linux-x86_64.glibc2.12/man/man1/
    percona-xtrabackup-2.4.27-Linux-x86_64.glibc2.12/man/man1/xtrabackup.1
    percona-xtrabackup-2.4.27-Linux-x86_64.glibc2.12/man/man1/xbstream.1
    percona-xtrabackup-2.4.27-Linux-x86_64.glibc2.12/man/man1/xbcrypt.1
    ...
    ```

An installation from a binary tarball requires doing certain tasks manually, such as configuring settings, and policies, that a repository package installation performs automatically.
