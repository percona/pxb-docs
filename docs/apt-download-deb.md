# Install Percona XtraBackup 8.0 using downloaded DEB packages

Download `DEB` packages of the desired series for your architecture from [Percona Product Downloads](https://www.percona.com/downloads). 

The following example downloads *Percona XtraBackup* 8.0.26-18 release package for Ubuntu 20.04:

```{.bash data-prompt="$"}
$ wget https://downloads.percona.com/downloads/Percona-XtraBackup-LATEST/Percona-XtraBackup-8.0.26-18/binary/debian/focal/x86_64/percona-xtrabackup-80_8.0.26-18-1.focal_amd64.deb
```

Install Percona XtraBackup by using `dpkg`. Run this command as root or use the sudo command:

```{.bash data-prompt="$"}
$ sudo dpkg -i percona-xtrabackup-80_8.0.26-18-1.focal_amd64.deb
```

!!! warning

    When installing packages manually like this, resolve all the dependencies and install missing packages yourself.