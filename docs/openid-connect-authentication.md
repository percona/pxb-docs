# OpenID Connect authentication

Percona XtraBackup 8.4.0-9 adds support for OpenID Connect (OIDC) authentication. With OIDC, the backup account logs in to Percona Server for MySQL with an ID token from an external identity provider (IdP), such as Keycloak, Okta, or Microsoft Entra ID. The backup account needs no password.

To try OIDC authentication step by step, see [Get started with OpenID Connect authentication](quickstart-openid-connect.md).

## How OIDC authentication works

Percona Server for MySQL 8.4.10 and later ship the `auth_openid_connect` server plugin. A database account created `IDENTIFIED WITH auth_openid_connect` logs in with a signed ID token, a JSON Web Token (JWT), instead of a password.

A backup with OIDC authentication runs as follows:

1. You get an ID token for the backup account from your IdP and save the token to a file.

2. You pass the file path to xtrabackup with the [`--authentication-openid-connect-client-id-token-file`](xtrabackup-option-reference.md#authentication-openid-connect-client-id-token-file) option.

3. xtrabackup loads the `authentication_openid_connect_client` client plugin from the directory set by [`--xtrabackup-plugin-dir`](xtrabackup-option-reference.md#xtrabackup-plugin-dir).

4. The client plugin reads the token, checks that the connection is secure, and sends the token to the server during the handshake.

5. The server plugin checks the token signature, issuer, audience, expiry time, and subject. If all checks pass, the server lets xtrabackup in.

xtrabackup uses the same token for every connection to the server:

* The main backup connection

* The metadata lock (MDL) connection

* The query killer connection

* The redo log archiving connection

* The redo log consumer connection

The `--prepare` and `--copy-back` modes do not connect to the server and do not need a token.

## Requirements

To back up a server with OIDC authentication, you need the following:

* Percona Server for MySQL 8.4.10 or later with the `auth_openid_connect` server plugin installed and configured. For details, see [OpenID Connect authentication in Percona Server for MySQL :octicons-link-external-16:](https://docs.percona.com/percona-server/{{vers}}/openid-connect-authentication.html).

* A database account `IDENTIFIED WITH auth_openid_connect` with the [privileges that xtrabackup needs](privileges.md#privileges-needed).

* A valid ID token for that account in a file. The file must contain only the raw JWT: no spaces, no line breaks, no JSON wrapper, and no `Bearer` prefix. The client plugin accepts files up to 10 KB.

* A secure connection to the server: a Unix socket, or TCP with TLS (`--ssl-mode=REQUIRED`). The client and server plugins refuse a plain TCP connection.

* The `authentication_openid_connect_client.so` client plugin in the xtrabackup plugin directory. The Percona XtraBackup packages include this file.

## Client plugin location

Percona XtraBackup installs the client plugin in the following directory:

| Package type   | Directory                         |
|----------------|-----------------------------------|
| RPM            | `/usr/lib64/xtrabackup/plugin/`   |
| DEB            | `/usr/lib/xtrabackup/plugin/`     |
| Binary tarball | `lib/plugin/` inside the tarball directory |

With the RPM or DEB package, `--xtrabackup-plugin-dir` points to this directory by default, so you do not need to set the option.

With a binary tarball, set the option to the plugin directory of the tarball:

```shell
xtrabackup --backup --user=bkpuser \
  --authentication-openid-connect-client-id-token-file=/root/.oidc/id_token.jwt \
  --xtrabackup-plugin-dir=/opt/percona-xtrabackup-8.4/lib/plugin \
  --target-dir=/data/backups/full
```

## Create the backup account

Create the account on the server and grant the backup privileges. The `identity_provider` value must match an IdP name in the `auth_openid_connect_configuration` system variable. The `user` value must match the `sub` claim of the ID token. Keycloak and many other IdPs set `sub` to an internal user ID, not to the login name.

```sql
CREATE USER 'bkpuser'@'localhost'
  IDENTIFIED WITH 'auth_openid_connect'
  AS '{"identity_provider": "my-keycloak", "user": "4c28d537-a635-4b6d-957f-58e3c8860bcc"}';

GRANT BACKUP_ADMIN, PROCESS, RELOAD, LOCK TABLES, REPLICATION CLIENT ON *.* TO 'bkpuser'@'localhost';
GRANT SELECT ON performance_schema.log_status TO 'bkpuser'@'localhost';
GRANT SELECT ON performance_schema.keyring_component_status TO 'bkpuser'@'localhost';
GRANT SELECT ON performance_schema.replication_group_members TO 'bkpuser'@'localhost';
```

The server checks the token when xtrabackup connects, not when you run `CREATE USER`.

## Back up with an ID token

Pass the token file instead of a password.

Connect through the Unix socket:

```shell
xtrabackup --backup --user=bkpuser \
  --socket=/var/lib/mysql/mysql.sock \
  --authentication-openid-connect-client-id-token-file=/root/.oidc/id_token.jwt \
  --target-dir=/data/backups/full
```

Connect over TCP with TLS:

```shell
xtrabackup --backup --user=bkpuser \
  --host=db1.example.com --port=3306 --ssl-mode=REQUIRED \
  --authentication-openid-connect-client-id-token-file=/root/.oidc/id_token.jwt \
  --target-dir=/data/backups/full
```

Prepare and restore the backup as usual. See [Prepare a full backup](prepare-full-backup.md) and [Restore a backup](restore-a-backup.md).

You can also set the option in the `[xtrabackup]` group of your configuration file:

```ini
[xtrabackup]
user=bkpuser
socket=/var/lib/mysql/mysql.sock
authentication-openid-connect-client-id-token-file=/root/.oidc/id_token.jwt
```

## Token file path

xtrabackup reads the path as follows:

* xtrabackup uses an absolute path unchanged.

* A path that starts with `~/` starts from the home directory of the user who runs xtrabackup.

* A relative path starts from the directory where you started xtrabackup.

xtrabackup does not expand `~user/`. An empty file name causes an error.

Use an absolute path in configuration files and scheduled jobs. Restrict access to the token file, for example with `chmod 600`, because anyone who reads the token can log in as the backup account until the token expires.

## Options that work with the token

| Option | Behavior with `--authentication-openid-connect-client-id-token-file` |
|--------|------|
| `--password` | You cannot use both options. The ID token replaces the password. xtrabackup stops with an error before the backup starts. xtrabackup also refuses `-p` before asking for a password. `--skip-password` sets no password, so xtrabackup accepts this option. |
| `--xtrabackup-plugin-dir` | Sets the directory with `authentication_openid_connect_client.so`. |
| `--socket`, `--host`, `--ssl-mode` | The token goes only over a Unix socket or a TLS connection. Plain TCP fails. |
| `--history-user`, `--history-password` | Control the credentials for the backup history connection. See [Backup history connection](#backup-history-connection). |

### Backup history connection

The [`--history`](store-backup-history.md) option writes a record to the `PERCONA_SCHEMA.xtrabackup_history` table. The history connection has no token option of its own and follows these rules:

* Without `--history-user` and `--history-password`, the history connection uses the backup credentials, including the ID token.

* With `--history-user`, the history account must log in with a password set by `--history-password`.

## Log messages

Before the first connection, xtrabackup logs the token file and the plugin directory. Each connection that uses the token says so instead of showing a password status:

```text
Using OpenID Connect ID token file '/root/.oidc/id_token.jwt' for authentication to the server.
Loading the authentication_openid_connect_client plugin from '/usr/lib64/xtrabackup/plugin' (--xtrabackup-plugin-dir).
Connecting to MySQL server host: localhost, user: bkpuser, password: not set (using OpenID Connect ID token), port: not set, socket: /var/lib/mysql/mysql.sock, purpose: backup
```

## Token lifetime

ID tokens are short-lived. Many IdPs issue tokens that expire after a few minutes. xtrabackup does not get or refresh tokens.

xtrabackup opens most connections at the start of the backup, but the query killer connects later. Follow these recommendations:

* Get a fresh token right before each backup, for example in the script that starts xtrabackup.

* Make sure the token lifetime covers the whole backup.

## Troubleshoot

The server rejects a bad token with a generic `Access denied` message. The server error log shows the exact reason.

| Error | Cause and fix |
|-------|---------------|
| `--password and --authentication-openid-connect-client-id-token-file are mutually exclusive: the ID token is the credential.` | Remove `--password` from the command line and from the configuration files. |
| `Cannot load the authentication_openid_connect_client plugin: <reason>` | xtrabackup cannot find the client plugin. Check `--xtrabackup-plugin-dir`. With a binary tarball, set the option to `lib/plugin` in the tarball directory. |
| `Failed to set the ID token file '<path>' for the authentication_openid_connect_client plugin. Check that the file exists and is readable.` | The file does not exist, or the system user who runs xtrabackup cannot read the file. xtrabackup reports this error before contacting the server. |
| `The id token file: <path> does not contain a valid JWT.` | The file holds something other than a raw JWT. Save only the `id_token` value, not the access token or the full JSON response. |
| `Access denied for user ...` | The token expired, the token is not signed by a trusted key, the `sub` claim does not match the account, or the connection is not secure. Check the server error log. For example, `unsecure connection, use TLS, socket or memory` means you need a socket or `--ssl-mode=REQUIRED`. |
| `Access denied` after a server restart or restore | The server lost the `auth_openid_connect_configuration` value because you set the variable with `SET GLOBAL`. Persist the value with `SET PERSIST`, or set the variable in `my.cnf`. |

For more server-side messages, see [Troubleshoot connection failures in Percona Server for MySQL :octicons-link-external-16:](https://docs.percona.com/percona-server/{{vers}}/openid-connect-authentication.html).

## Limitations

* The history connection cannot use a different ID token. A history server that trusts another IdP or audience needs a password account.

* xtrabackup does not request, cache, or refresh ID tokens. Your script or operator must provide a valid token before each backup.

!!! admonition "See also"

    * [Get started with OpenID Connect authentication](quickstart-openid-connect.md)

    * [OpenID Connect authentication in Percona Server for MySQL :octicons-link-external-16:](https://docs.percona.com/percona-server/{{vers}}/openid-connect-authentication.html)

    * [Connection and privileges needed](privileges.md)
