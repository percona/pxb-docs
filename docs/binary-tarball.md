# Install from a binary tarball

Binary tarballs are compressed' tar' archives that contain precompiled executable files, libraries, and other dependencies. You can extract the binary tarballs to any path.

Download the binary tarballs from the `Linux - Generic` section on [Percona Product Downloads].

The following example downloads the tarball:

```{.bash data-prompt="$"}
$ wget https://downloads.percona.com/ \
downloads/Percona-XtraBackup-{{vers}}/ \
Percona-XtraBackup-{{release}}/binary/ \
tarball/percona-xtrabackup-{{release}}-Linux-x86_64.glibc2.28.tar.gz
```

The output displays the following information:

??? example "Expected output"

    ```{.text .no-copy}
    --2024-10-09 04:44:36--  https://downloads.percona.com/downloads/Percona-XtraBackup-8.4/Percona-XtraBackup-8.4.0-       1/binary/tarball/percona-xtrabackup-8.4.0-1-Linux-x86_64.glibc2.28.tar.gz
    Resolving downloads.percona.com (downloads.percona.com)... 147.135.54.159, 2604:2dc0:200:69f::2
    Connecting to downloads.percona.com (downloads.percona.com)|147.135.54.159|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 439358509 (419M) [application/gzip]
    Saving to: ‘percona-xtrabackup-8.4.0-1-Linux-x86_64.glibc2.28.tar.gz’

    percona-xtrabackup-8.4.0-1-Linux-x86_6 100%  
    [============================================================================>] 419.00M  6.67MB/s    in 94s

    2024-10-09 04:46:10 (4.48 MB/s) - ‘percona-xtrabackup-8.4.0-1-Linux-x86_64.glibc2.28.tar.gz’ saved 
    [439358509/439358509]
    ```

[Percona Product Downloads]: https://www.percona.com/downloads/
