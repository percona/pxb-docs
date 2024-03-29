# Install Percona XtraBackup {{vers}} using downloaded RPM packages

Download `RPM` packages of the desired series for your architecture from the [download page](https://www.percona.com/downloads/). 

The following example downloads *Percona XtraBackup* {{release}} release package for *CentOS* 7:

```{.bash data-prompt="$"}
$ wget https://www.percona.com/downloads/XtraBackup/Percona-XtraBackup-{{release}}/binary/redhat/7/x86_64/percona-xtrabackup-{{pkg}}-{{release}}.el7.x86_64.rpm
```

Install Percona XtraBackup by running:

```{.bash data-prompt="$"}
$ yum localinstall percona-xtrabackup-{{pkg}}-{{release}}.el7.x86_64.rpm
```

When installing packages manually like this, you’ll need to make sure to resolve all the dependencies and install missing packages yourself.