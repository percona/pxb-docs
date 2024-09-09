# Binary tarball file names available

For recent versions of Percona XtraBackup, the tar files are organized by the `glibc2` version. You can find this version on your operating system with the following command:

```{.bash data-prompt="$"}
$ ldd --version
```

??? example "Expected output"
    ```text
    ldd (Ubuntu GLIBC 2.35-0ubuntu3.1) 2.35
    Copyright (C) 2022 Free Software Foundation, Inc.
    This is free software; see the source for copying conditions.  There is NO
    warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    Written by Roland McGrath and Ulrich Drepper.
    ```

If the `glibc2` version from your operating system is not listed, then this Percona Server for MySQL version does not support that operating system.

## Binary tarball file name organization

The following lists the platform and the associated full binary file name used by Percona Server for MySQL tar files {{release}}.

| Platform             | Percona XtraBackup tarball name                   | glibc2 version |
|----------------------|--------------------------------------------------------------|-----------|
| Ubuntu 24.04         | Percona-XtraBackup-{{release}}-Linux.x86_64.glibc2.39.tar.gz     | glibc2.39 |
| Ubuntu 22.04         | Percona-XtraBackup-{{release}}-Linux.x86_64.glibc2.35.tar.gz     | glibc2.35 |
| Ubuntu 20.04         | Percona-XtraBackup-{{release}}-Linux.x86_64.glibc2.31.tar.gz     | glibc2.31 |
| Debian 12            | Percona-XtraBackup-{{release}}-Linux.x86_64.glibc2.36.tar.gz     | glibc2.36 |
| Debian 11            | Percona-XtraBackup-{{release}}-Linux.x86_64.glibc2.31.tar.gz     | glibc2.31 |
| Red Hat Enterprise 9 | Percona-XtraBackup-{{release}}-Linux.x86_64.glibc2.34.tar.gz     | glibc2.34 |
| Red Hat Enterprise 8 | Percona-XtraBackup-{{release}}-Linux.x86_64.glibc2.28.tar.gz     | glibc2.28 |


Download the binary tarballs from [Percona Software Downloads].

The following table lists the tarball types available in `Linux - Generic`. Select the *Percona XtraBackup* {{vers}} version, the software or the operating system, and the type of tarball for your installation. Binary tarballs support all distributions.

After you have downloaded the binary tarballs, extract the tarball in the file location of your choice.

| Type         | Name                                                                      | Operating systems                                        | Description                                                                            |
|--------------|---------------------------------------------------------------------------|----------------------------------------------------------|----------------------------------------------------------------------------------------|
| Full         | percona-xtrabackup-{{release}}-Linux.x86_64.glibc2.12.tar.gz         | Built for CentOS 6                                       | Contains binary files, libraries, test files, and debug symbols                        |
| Minimal      | percona-xtrabackup-{{release}}-Linux.x86_64.glibc2.12-minimal.tar.gz | Built for CentOS 6                                       | Contains binary files, and libraries but does not include test files, or debug symbols |                                                                           |                                                          |                                                                          |
| Full         | percona-xtrabackup-{{release}}-Linux.x86_64.glibc2.17.tar.gz         | Compatible with any operating system except for CentOS 6 | Contains binary files, libraries, test files, and debug symbols                        |
| Minimal      | percona-xtrabackup-{{release}}-Linux.x86_64.glibc2.17-minimal.tar.gz | Compatible with any operating system except for CentOS 6 | Contains binary files, and libraries but does not include test files, or debug symbols |                                                                           |                                                          |                                                                                        |

Select a different software, such as Ubuntu 20.04 (Focal Fossa), for a 
tarball for that operating system. You can download the packages together or separately.

[Percona Software Downloads]: https://www.percona.com/downloads

