# Uninstall Percona XtraBackup 8.0 on Debian-based systems

Remember to back up any important data before uninstalling software.

To completely uninstall Percona XtraBackup, remove all the installed packages:

```shell
sudo apt remove percona-xtrabackup-80
```

Run the following command to remove all configuration files along with the packages:

```shell
sudo apt purge percona-xtrabackup-80
```

Remove any unused dependencies:

```shell
sudo apt autoremove

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