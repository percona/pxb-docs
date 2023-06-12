# Install Percona XtraBackup 8.0 using downloaded RPM packages

Download `RPM` packages of the desired series for your architecture from the [download page](https://www.percona.com/downloads/). 

The following example downloads *Percona XtraBackup* 8.0.4 release package for *CentOS* 7:

```{.bash data-prompt="$"}
$ wget https://www.percona.com/downloads/XtraBackup/Percona-XtraBackup-8.0.4/binary/redhat/7/x86_64/percona-xtrabackup-80-8.0.4-1.el7.x86_64.rpm
```

Install Percona XtraBackup by running:

```{.bash data-prompt="$"}
$ yum localinstall percona-xtrabackup-80-8.0.4-1.el7.x86_64.rpm
```

When installing packages manually like this, you’ll need to make sure to resolve all the dependencies and install missing packages yourself.