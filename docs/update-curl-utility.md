# Dependency compatibility and limitations

xbcloud depends on several system libraries for correct operation. Some versions of these dependencies are known to cause unexpected terminations or
unstable behavior and are therefore not supported.

If you are experiencing unexpected terminations or intermittent failures, verify that your environment does not use any of the versions listed below.

## libcurl

Certain versions of `libcurl` are known to cause unexpected terminations or connection
reuse issues in `xbcloud`. The following versions are not supported.

### Unsupported versions

`libcurl 7.64.0 `

* Known to mishandle reuse of closed connections

* May cause intermittent backup failures in `xbcloud`

`libcurl versions ≥ 8.11.1 and < 8.12.0`

* Affected by double close of an eventfd file descriptor, [CVE-2025-0665 :octicons-link-external-16:](https://github.com/advisories/GHSA-cc57-hgv8-p56r)

* May cause unexpected terminations when `xbcloud` uses `libcurl`

### Upgrade or downgrade options

You should always upgrade `xbcloud` to the latest version, as it includes fixes for all known issues and compatibility problems.

If the installed `libcurl` version is not supported, update it depending on the operating system and available repositories.

* Recommended - Upgrade to libcurl `8.12.0 or later` if these versions are compatible with your operating system.

* If upgrading to the latest version `≥ 8.12.0` is not possible, downgrade to a supported version earlier than 8.11.1 to avoid the vulnerability associated with [CVE-2025-0665 :octicons-link-external-16:](https://github.com/advisories/GHSA-cc57-hgv8-p56r). Ensure that the downgrade is compatible with other system dependencies.

### Check the installed libcurl version

To check the installed libcurl version, run:

```bash
curl --version
```

### Upgrade libcurl - Recommended

The following steps show how to update the libcurl to version 8.12.0 on Debian 12. Administrator privileges are necessary for installing packages and configuring system services.
{.power-number}

1. Edit the `/etc/apt/sources.list` to add the following:

    ```
    deb http://deb.debian.org/debian bookworm-backports main
    ```

2. Refresh the `apt` sources:

    ```bash
    sudo apt update
    ```

3. Install the version from `bookworm-backports`:

    ```bash
    sudo apt install -t bookworm-backports libcurl4 curl
    ```

4. Verify the version number:

    ```bash
    curl --version
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        curl 8.12.0 (x86_64-pc-linux-gnu) libcurl/8.12.0
        ```

### Downgrade libcurl

The following steps show how to downgrade the libcurl to the default Debian 12 version 7.88.1. Administrator privileges are necessary for installing packages and configuring system services.
{.power-number}

1. Update the package list:

    ```bash
    sudo apt update
    ```

2. Reinstall the default system version of libcurl and curl:

    ```bash
    sudo apt install --reinstall libcurl4 curl
    ```

3. Verify the version number:

    ```bash
    curl --version
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        curl 7.88.1 (x86_64-pc-linux-gnu) libcurl/7.88.1 OpenSSL/3.0.9 zlib/1.2.13 libidn2/2.3.4 libssh/0.10.5
        Release-Date: 2023-08-02
        Protocols: dict file ftp ftps gopher http https imap imaps ldap ldaps mqtt pop3 pop3s rtsp smb smbs smtp smtps telnet tftp 
        Features: AsynchDNS IDN IPv6 Largefile NTLM NTLM_WB SSL libz TLS-SRP HTTP2 HSTS HTTPS-proxy Metalink
        ```
