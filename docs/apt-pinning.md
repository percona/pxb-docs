# Pin packages in Debian-based systems

You may need to keep a specific package at a certain version and prevent it from being automatically updated by your package manager. This action is called "pinning" a package.
{.power-number}

1. Create a preference file, `00percona.pref`, in the `/etc/apt/preferences.d/` directory.

2. Set the Pinning priority

    To pin a package, set the `Pin-Priority` to a higher number than the default priority of the packages. This setting makes the packages higher priority over the other sources.

    For example, add the following lines to the preference file:

    ```
    Package: <package_name>
    Pin: release o=Percona Development Team
    Pin-Priority: 1001
    ```

    Replace the `<package_name>` with the package's name. 

3. Save the `00percona.pref` file.

You can pin multiple packages by adding separate entries to the file.

Remove the entry from the file if you no longer want to pin the package.

For more information about the pinning, check the official [debian wiki](http://wiki.debian.org/AptPreferences).