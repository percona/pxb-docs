# The xbcloud command-line options

The xbcloud binary has the following command line options:

## storage

Usage: `--storage=[swift|s3|google]`

Defines the Cloud storage option. xbcloud supports Swift, MinIO, and AWS S3. The default value is `swift`.

## swift-auth-url

Usage: `--swift-auth-url`

The URL of the Swift cluster

## swift-storage-url

Usage: `--swift-storage-url`

The xbcloud tries to get the object-store URL for a given region (if any are specified)
from the keystone response. You can override that URL by passing
[–swift-storage-url=URL](#swift-storage-url) argument.

## swift-user

Usage: `--swift-user`
The Swift username (X-Auth-User, specific to Swift)

## swift-key

Usage: `--swift-key`
The Swift key/password (X-Auth-Key, specific to Swift)

## swift-container

Usage: `--swift-container`

The container to back up into (specific to Swift)

## parallel

Usage: `--parallel=N`

The maximum number of concurrent upload/download requests. The default value is `1`.

## cacert

Usage: `--cacert`

The path to the file with CA certificates

## insecure

Usage: `--insecure`

Do not verify the server's certificate

## Swift authentication options

The Swift specification describes several [authentication options](http://docs.openstack.org/developer/swift/overview_auth.html). The *xbcloud* tool can
authenticate against keystone with API version 2 and 3.

## swift-auth-version

Usage: `--swift-auth-version`

Specifies the swift authentication version. The possible values are: `1.0` -
TempAuth, `2.0` - Keystone v2.0, and `3` - Keystone v3. The default value is
`1.0`.

## For v2 additional options are:

### swift-tenant

Usage: `--swift-tenant`

Swift tenant name

### swift-tenant-id

Usage: `--swift-tenant-id`

Swift tenant ID

### swift-region

Usage: `--swift-region`

Swift endpoint region

### swift-password

Usage: `--swift-password`

Swift password for the user

## For v3, additional options are:

### swift-user-id

Usage: `--swift-user-id`

Swift user ID

### swift-project

Usage: `--swift-project`

Swift project name

### swift-project-id

Usage: `--swift-project-id`

Swift project ID

### swift-domain

Usage: `--swift-domain`

Swift domain name

### swift-domain-id

Usage: `--swift-domain-id`

Swift domain ID
