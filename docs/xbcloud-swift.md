# Use the xbcloud binary with Swift

## Create a full backup with Swift

For details on the command-line options,  see the [xbcloud command-line options]

The following example shows how to make a full backup and upload it to Swift.

```{.bash data-prompt="$"}
$ xtrabackup --backup --stream=xbstream --extra-lsndir=/tmp --target-dir=/tmp | \
xbcloud put --storage=swift \
--swift-container=test \
--swift-user=test:tester \
--swift-auth-url=http://192.168.8.80:8080/ \
--swift-key=testing \
--parallel=10 \
full_backup
```

The following [OpenStack](https://docs.openstack.org/2023.2/) environment variables are also recognized and mapped automatically to the corresponding swift parameters (`--storage=swift`):

* OS_AUTH_URL

* OS_TENANT_NAME

* OS_TENANT_ID

* OS_USERNAME

* OS_PASSWORD

* OS_USER_DOMAIN

* OS_USER_DOMAIN_ID

* OS_PROJECT_DOMAIN

* OS_PROJECT_DOMAIN_ID

* OS_REGION_NAME

* OS_STORAGE_URL

* OS_CACERT

## Restore with Swift

```{.bash data-prompt="$"}
$ xbcloud get [options] <name> [<list-of-files>] | xbstream -x
```

The following example shows how to fetch and restore the backup from Swift:

```{.bash data-prompt="$"}
$ xbcloud get --storage=swift \
--swift-container=test \
--swift-user=test:tester \
--swift-auth-url=http://192.168.8.80:8080/ \
--swift-key=testing \
full_backup | xbstream -xv -C /tmp/downloaded_full

$ xbcloud delete --storage=swift --swift-user=xtrabackup \
--swift-password=xtrabackup123! --swift-auth-version=3 \
--swift-auth-url=http://openstack.ci.percona.com:5000/ \
--swift-container=mybackup1 --swift-domain=Default
```

[xbcloud command-line options]: xbcloud-options.md