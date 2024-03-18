# Install Percona XtraBackup 8.0 from a binary tarball

Binary tarballs provide a ready-to-use application since they contain precompiled executables, libraries, and dependencies. Installing from a tarball is straightforward — extract the files to your desired location. Compiling or building from source is unnecessary, which saves time and effort. You avoid the compilation process, which can be time-consuming and error-prone.

Binary tarballs provide only the necessary files, reducing disk space usage. A binary tarball installation allows customization since you can choose installation paths, configure options, and tailor the application to your requirements. Binary tarballs often come with version numbers, letting you track and update the installed version as needed.

Be aware of the following when installing from a binary tarball:

* Binary tarballs bundle dependencies within themselves. If your system already has specific libraries or versions installed, you may have conflicts.

* Binary tarball installation bypasses the package manager. Package managers handle updates, dependencies, and conflict resolution. Manual management of updates becomes necessary.

* Binary tarballs may not receive security patches automatically. You must actively monitor and apply updates.

* Binary tarball custom installation can scatter files. It may not adhere to standard paths, which makes maintenance challenging.

## Download the tarball 

You can download the binary tarballs from the `Linux - Generic` section on the [Percona Product Downloads](https://www.percona.com/downloads/). For more information, see the [download instructions]. For information on the available binary tarball names, see [binary tarball names].


The following command is an example of downloading a tarball for Linux/Generic:

```{.bash data-prompt="$"}
$ wget https://downloads.percona.com/downloads/Percona-XtraBackup-8.0/Percona-XtraBackup-8.0.35-30/binary/tarball/percona-xtrabackup-8.0.35-30-Linux-x86_64.glibc2.17.tar.gz
```

??? example "Expected result"

    ```{.text .no-copy}
    --2024-03-18 11:34:50--  https://downloads.percona.com/downloads/Percona-XtraBackup-8.0/Percona-XtraBackup-8.0.35-30/binary/tarball/percona-xtrabackup-8.0.35-30-Linux-x86_64.glibc2.17.tar.gz
    Resolving downloads.percona.com (downloads.percona.com)... 147.135.54.159, 2604:2dc0:200:69f::2
    Connecting to downloads.percona.com (downloads.percona.com)|147.135.54.159|:443... connected.
    ...
    percona-xtrabackup-8.0 100%[==========================>] 448.02M  2.56MB/s    in 5m 5s
    2024-03-18 11:39:56 (1.47 MB/s) - 'percona-xtrabackup-8.0.35-30-Linux-x86_64.glibc2.17.tar.gz' saved [469780148/469780148]
    ```

## Extract the tarball

After downloading the tarball to the selected location, use the following command to extract the tarball:

```{.bash data-prompt="$"}
$ tar -xvf percona-xtrabackup-8.0.35-30-Linux-x86_64.glibc2.17.tar.gz
```

??? example "Expected result"

    ```{.text .no-copy}
    percona-xtrabackup-8.0.35-30-Linux-x86_64.glibc2.17/
    percona-xtrabackup-8.0.35-30-Linux-x86_64.glibc2.17/bin/
    percona-xtrabackup-8.0.35-30-Linux-x86_64.glibc2.17/bin/xbcloud_osenv
    percona-xtrabackup-8.0.35-30-Linux-x86_64.glibc2.17/bin/xtrabackup
    percona-xtrabackup-8.0.35-30-Linux-x86_64.glibc2.17/bin/xbcrypt
    percona-xtrabackup-8.0.35-30-Linux-x86_64.glibc2.17/bin/xbstream
    percona-xtrabackup-8.0.35-30-Linux-x86_64.glibc2.17/bin/xbcloud
    ...
    ```

After the extraction, navigate to the `bin` directory to find the binary files. 


```{.bash data-prompt="$"}
$ cd percona-xtrabackup-8.0.35-30-Linux-x86_64.glibc2.17/bin
```

In the bin directory, run one of the binary files.

```{.bash data-prompt="$"}
$ ./xtrabackup --version
```

??? example "Expected result"

    ```{.text .no-copy}
    ./xtrabackup version 8.0.35-30 based on MySQL server 8.0.35 Linux (x86_64) (revision id: 6beb4b49)
    ```

[download instructions]: download-instructions.md
[binary tarball names]: binary-tarball-names.md