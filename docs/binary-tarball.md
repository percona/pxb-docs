<!--
update example
20230818
--->

# Install from a binary tarball

Binary tarballs contain precompiled executable files, libraries, and other dependencies and are
compressed `tar` archives. Extract the binary tarballs to any path.

Download the binary tarballs from the `Linux - Generic` section on [Percona Product Downloads].

The following example downloads the a tarball:

```{.bash data-prompt="$"}
$ wget https://downloads.percona.com/downloads/Percona-XtraBackup-8.0/Percona-XtraBackup-8.0.34-29/binary/tarball/percona-xtrabackup-8.0.34-29-Linux-x86_64.glibc2.17.tar.gz
```

The output displays the following information:

??? example "Expected output"

    ```{.text .no-copy}
    --2023-08-25 05:56:30--  https://downloads.percona.com/downloads/Percona-XtraBackup-8.0/Percona-XtraBackup-8.0.34-29/binary/tarball/percona-xtrabackup-8.0.34-29-Linux-x86_64.glibc2.17.tar.gz
    Resolving downloads.percona.com (downloads.percona.com)... 2604:2dc0:200:69f::2, 147.135.54.159
    Connecting to downloads.percona.com (downloads.percona.com)|2604:2dc0:200:69f::2|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 470358258 (449M) [application/gzip]
    Saving to: ‘percona-xtrabackup-8.0.34-29-Linux-x86_64.glibc2.17.tar.gz’

    percona-xtrabackup   0%[                       ]   3.17M  1.54MB/s
    ```

[Percona Product Downloads]: https://www.percona.com/downloads/