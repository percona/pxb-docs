# Use the xbcloud binary with Swift

## Create a full backup with Swift

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

The following OpenStack environment variables are also recognized and mapped automatically to the corresponding swift parameters (`--storage=swift`):
 
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

## Command-line options

*xbcloud* has the following command line options:

### --storage(=[swift|s3|google])

Cloud storage option. *xbcloud* supports Swift, MinIO, and AWS S3.
The default value is `swift`.

### --swift-auth-url()

The URL of the Swift cluster

### --swift-storage-url()

The xbcloud tries to get the object-store URL for a given region (if any are specified)
from the keystone response. You can override that URL by passing
–swift-storage-url=URL argument.

### --swift-user()

The Swift username (X-Auth-User, specific to Swift)

### --swift-key()

The Swift key/password (X-Auth-Key, specific to Swift)

### --swift-container()

The container to back up into (specific to Swift)

### --parallel(=N)

The maximum number of concurrent upload/download requests. The default value is `1`.

### --cacert()

The path to the file with CA certificates

### --insecure()

Do not verify server's certificate

### Swift authentication options

The Swift specification describes several [authentication options](http://docs.openstack.org/developer/swift/overview_auth.html). The *xbcloud* tool can
authenticate against keystone with API version 2 and 3.

### --swift-auth-version()

Specifies the swift authentication version. The possible values are: `1.0` -
TempAuth, `2.0` - Keystone v2.0, and `3` - Keystone v3. The default value is
`1.0`.

For v2 additional options are:

### --swift-tenant()

Swift tenant name

### --swift-tenant-id()

Swift tenant ID

### --swift-region()

Swift endpoint region

### --swift-password()

Swift password for the user

For v3 additional options are:

### --swift-user-id()

Swift user ID

### --swift-project()

Swift project name

### --swift-project-id()

Swift project ID

### --swift-domain()

Swift domain name

### --swift-domain-id()

Swift domain ID
