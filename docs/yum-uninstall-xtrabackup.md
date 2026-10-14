# Uninstall Percona XtraBackup 8.0 on Red Hat-based systems

Remember to back up any important data before uninstalling software.

Remove the XtraBackup packages:

```shell
sudo yum remove percona-xtrabackup-80
```

To remove all configuration files and packages, run the following command:

```shell
sudo yum remove percona-xtrabackup-80 --remove-leaves
```

Remove any unused dependencies:

```shell
sudo yum autoremove
```

To verify the removal, check the version:

```shell
xtrabackup --version
```

This should return a `command not found`.

You must remove any remaining directories manually:

```shell
sudo rm -rf /var/lib/xtrabackup
```

You can also remove any added Percona repositories from your system manager's configuration.