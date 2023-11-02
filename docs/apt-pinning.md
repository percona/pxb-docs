# Apt pinning packages

In some cases you might need to `pin` the selected packages to avoid the upgrades from the distribution repositories. 

The pinning takes place in the `preference` file. To pin a package, set the `Pin-Priority` to higher numbers.

Make a new file `/etc/apt/preferences.d/00percona.pref`. For example, add the following to the preference file:

```
Package:
Pin: release o=Percona Development Team
Pin-Priority: 1001
```

For more information about the pinning, check the official [debian wiki].

[debian wiki]: http://wiki.debian.org/AptPreferences
