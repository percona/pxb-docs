# Get started with OpenID Connect authentication

This guide shows how to back up Percona Server for MySQL with an account that logs in with an OpenID Connect (OIDC) ID token from Keycloak. You install and configure the server plugin, create a backup account, get an ID token, and run a backup without a password.

The guide takes about 20 minutes.

For details about the feature, see [OpenID Connect authentication](openid-connect-authentication.md).

## Before you begin

Make sure you have the following:

* Percona Server for MySQL 8.4.10 or later with `auth_openid_connect.so` in the `plugin_dir` directory.

* Percona XtraBackup 8.4.0-9 or later, installed from an RPM or DEB package.

* A Keycloak server with a realm, an OIDC client, and a user for backups.

* `curl` and `jq` on the host where you run xtrabackup.

* A MySQL administrative account with the `INSERT` privilege on `mysql.plugin`, the `SYSTEM_VARIABLES_ADMIN` privilege, and the `CREATE USER` privilege.

Run the shell commands in this guide as `root` on the database host, because xtrabackup needs read access to the data directory.

## Quickstart values

Replace the following example values with your own:

| Item | Example value |
|------|---------------|
| Keycloak host | `keycloak.example.com` |
| Keycloak realm | `master` |
| Keycloak client ID | `mysql-oidc` |
| Keycloak user | `backup-operator` |
| `sub` claim of the Keycloak user | `4c28d537-a635-4b6d-957f-58e3c8860bcc` |
| IdP name in MySQL | `my-keycloak` |
| MySQL backup account | `bkpuser@localhost` |
| MySQL socket | `/var/lib/mysql/mysql.sock` |
| Token file | `/root/.oidc/id_token.jwt` |
| Backup directory | `/data/backups/full` |

To find the `sub` claim, open the user in the Keycloak admin console and copy the user ID.

## Install the server plugin

Connect to the server as the administrative user and install the plugin:

```sql
INSTALL PLUGIN auth_openid_connect SONAME 'auth_openid_connect.so';
```

Check that the plugin is active:

```sql
SELECT PLUGIN_NAME, PLUGIN_STATUS
FROM INFORMATION_SCHEMA.PLUGINS
WHERE PLUGIN_NAME = 'auth_openid_connect';
```

??? example "Expected output"

    ```{.text .no-copy}
    +---------------------+---------------+
    | PLUGIN_NAME         | PLUGIN_STATUS |
    +---------------------+---------------+
    | auth_openid_connect | ACTIVE        |
    +---------------------+---------------+
    ```

## Configure trust for Keycloak

Tell the server which IdP to trust. The server gets the signing keys from the Keycloak JWKS endpoint. The `audiences` value must match the Keycloak client ID, because Keycloak puts the client ID in the `aud` claim of the ID token.

```sql
SET PERSIST auth_openid_connect_configuration = 'JSON://{
  "my-keycloak": {
    "issuer-name": "https://keycloak.example.com/realms/master",
    "jwks-url": "https://keycloak.example.com/realms/master/protocol/openid-connect/certs",
    "audiences": ["mysql-oidc"]
  }
}';
```

`SET PERSIST` keeps the value after a server restart. A value set with `SET GLOBAL` disappears after a restart, and then every OIDC login fails.

## Create the backup account

Create an account that logs in with an ID token. The `user` value is the `sub` claim of the Keycloak user:

```sql
CREATE USER 'bkpuser'@'localhost'
  IDENTIFIED WITH 'auth_openid_connect'
  AS '{"identity_provider": "my-keycloak", "user": "4c28d537-a635-4b6d-957f-58e3c8860bcc"}';
```

Grant the privileges that xtrabackup needs for a full backup:

```sql
GRANT BACKUP_ADMIN, PROCESS, RELOAD, LOCK TABLES, REPLICATION CLIENT ON *.* TO 'bkpuser'@'localhost';
GRANT SELECT ON performance_schema.log_status TO 'bkpuser'@'localhost';
GRANT SELECT ON performance_schema.keyring_component_status TO 'bkpuser'@'localhost';
GRANT SELECT ON performance_schema.replication_group_members TO 'bkpuser'@'localhost';
```

For the full list of privileges, see [Connection and privileges needed](privileges.md).

## Get an ID token from Keycloak

Create a private directory for the token:

```shell
mkdir -p -m 700 /root/.oidc
```

Request a token and save the `id_token` field to a file. Replace `<password>` with the password of the Keycloak user:

```shell
umask 077
curl -sS --fail -X POST \
  https://keycloak.example.com/realms/master/protocol/openid-connect/token \
  -d 'grant_type=password' \
  -d 'client_id=mysql-oidc' \
  -d 'scope=openid' \
  -d 'username=backup-operator' \
  -d 'password=<password>' \
  | jq -er .id_token > /root/.oidc/id_token.jwt

chmod 600 /root/.oidc/id_token.jwt
```

`umask 077` makes the shell create the token file readable only by `root`. `--fail` makes `curl` stop on an HTTP error, and `jq -e` stops with an error when the response has no `id_token` field.

Check that the file holds a JWT. A JWT has three parts separated by dots:

```shell
awk -F. '{print NF}' /root/.oidc/id_token.jwt
```

??? example "Expected output"

    ```{.text .no-copy}
    3
    ```

Keep the following in mind:

* The Keycloak client must allow the password grant. In the Keycloak admin console, open the client and enable **Direct access grants**.

* The plugin needs the ID token, not the access token.

* The `scope=openid` parameter is required. Without this parameter, Keycloak returns no ID token.

* This example uses a public client. For a confidential client, also send the `client_secret` parameter.

* The password grant suits tests and demos. In production, use the authorization code flow with PKCE or the device authorization flow.

ID tokens expire quickly. Get a fresh token right before each backup.

## Run the backup

Run xtrabackup with the token file instead of a password. The RPM and DEB packages already point `--xtrabackup-plugin-dir` to the client plugin, so you do not need to set the option.

```shell
xtrabackup --backup --user=bkpuser \
  --socket=/var/lib/mysql/mysql.sock \
  --authentication-openid-connect-client-id-token-file=/root/.oidc/id_token.jwt \
  --target-dir=/data/backups/full
```

??? example "Expected output"

    ```{.text .no-copy}
    ...
    [Note] [MY-011825] [Xtrabackup] Using OpenID Connect ID token file '/root/.oidc/id_token.jwt' for authentication to the server.
    [Note] [MY-011825] [Xtrabackup] Loading the authentication_openid_connect_client plugin from '/usr/lib64/xtrabackup/plugin' (--xtrabackup-plugin-dir).
    [Note] [MY-011825] [Xtrabackup] Connecting to MySQL server host: localhost, user: bkpuser, password: not set (using OpenID Connect ID token), port: not set, socket: /var/lib/mysql/mysql.sock, purpose: backup
    ...
    [Note] [MY-011825] [Xtrabackup] completed OK!
    ```

To connect over TCP instead of the socket, add `--host`, `--port`, and `--ssl-mode=REQUIRED`. The plugins refuse a plain TCP connection.

## Prepare the backup

The `--prepare` mode does not connect to the server, so you do not need the token:

```shell
xtrabackup --prepare --target-dir=/data/backups/full
```

To restore the backup, see [Restore a backup](restore-a-backup.md).

## Clean up

Remove the token file:

```shell
rm /root/.oidc/id_token.jwt
```

If you created the account only for this guide, drop the account:

```sql
DROP USER 'bkpuser'@'localhost';
```

To remove the server plugin, see [Uninstall the plugin in Percona Server for MySQL :octicons-link-external-16:](https://docs.percona.com/percona-server/{{vers}}/openid-connect-authentication.html).

## Additional resources

* [OpenID Connect authentication](openid-connect-authentication.md)

* [OpenID Connect authentication in Percona Server for MySQL :octicons-link-external-16:](https://docs.percona.com/percona-server/{{vers}}/openid-connect-authentication.html)

* [Get started with OpenID Connect authentication in Percona Server for MySQL :octicons-link-external-16:](https://docs.percona.com/percona-server/{{vers}}/quickstart-openid-connect.html)

* [Keycloak Server Administration Guide :octicons-link-external-16:](https://www.keycloak.org/docs/latest/server_admin/)
