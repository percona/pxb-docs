## Update the curl utility in Debian 10

The default curl version, 7.64.0, in Debian 10 has known issues when
attempting to reuse an already closed connection. This issue directly
affects `xbcloud` and users may see intermittent backup failures.

For more details,
see [curl #3750](https://github.com/curl/curl/issues/3750)
or [curl #3763](https://github.com/curl/curl/pull/3763).

Follow these steps to upgrade curl to version 7.74.0:
{.power-number}

1. Edit the `/etc/apt/sources.list` to add the following:

    ```
    deb http://ftp.de.debian.org/debian buster-backports main
    ```

2. Refresh the `apt` sources:

    ```{.bash data-prompt="$"}
    $ sudo apt update
    ```

3. Install the version from `buster-backports`:

    ```{.bash data-prompt="$"}
    $ sudo apt install curl/buster-backports
    ```

4. Verify the version number:

    ```{.bash data-prompt="$"}
    $ curl --version
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        curl 7.74.0 (x86_64-pc-linux-gnu) libcurl/7.74.0
        ```