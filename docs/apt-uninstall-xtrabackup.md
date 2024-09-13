# Uninstall Percona XtraBackup 8.0 on Debian-based systems

Remember to back up any important data before uninstalling software.

To completely uninstall Percona XtraBackup, remove all the installed packages:

```{.bash data-prompt="$"}
$ sudo apt remove percona-xtrabackup-80
```

Run the following command to remove all configuration files along with the packages:

```{.bash data-prompt="$"}
$ sudo apt purge percona-xtrabackup-80
```

Remove any unused dependencies:

```{.bash data-prompt="$"}
$ sudo apt autoremove

```

To verify the removal, check the version:

```{.bash data-prompt="$"}
$ xtrabackup --version
```

This should return a `command not found`.

You must remove any remaining directories manually:

```{.bash data-prompt="$"}
$ sudo rm -rf /var/lib/xtrabackup
```

You can also remove any added Percona repositories from your system manager's configuration.