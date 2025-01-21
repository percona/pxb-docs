# Install Percona XtraBackup {{vers}} using downloaded RPM packages

Download `RPM` packages of the desired series for your architecture from the [download page](https://www.percona.com/downloads/). 

The following example downloads *Percona XtraBackup* {{release}} release package for *RHEL* 9:

```{.bash data-prompt="$"}
$ wget https://downloads.percona.com/downloads/Percona-XtraBackup-innovative-release/Percona-XtraBackup-{{release}}/binary/redhat/9/x86_64/percona-xtrabackup-84-{{release}}.1.el9.x86_64.rpm
```

Install Percona XtraBackup by running:

```{.bash data-prompt="$"}
$ yum localinstall percona-xtrabackup-84-{{release}}.1.el9.x86_64.rpm
```

When installing packages manually like this, you’ll need to resolve all the dependencies and install missing packages yourself.
