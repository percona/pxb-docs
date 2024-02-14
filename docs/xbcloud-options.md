# The xbcloud command-line options

Usage: 
 
```{.text .no-copy}
$ xbcloud put [OPTIONS]
$ xbcloud get [OPTIONS]
$ xbcloud delete [OPTIONS]
```

This document contains information on general options and the options available when you select the [Swift authentication version using `swift-auth-version`](#swift-auth-version).

The xbcloud binary has the following general command line options:

## azure-access-key

Usage: `--azure-access-key=name`

The name of the Azure access-key

## azure-container

Usage: `--azure-container=name`

The name of the Azure container

## azure-development-storage

Usage: `--azure-development-storage=name`

If you run the [Azurite emulator](https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azurite?tabs=visual-studio,blob-storage), use this option, and it works with the default credentials provided by Azurite. You can overwrite these default credentials with other options.

## azure-endpoint

Usage: `--azure-endpoint=name`

The name of the Azure endpoint

## azure-storage-account

Usage: `--azure-storage-account=name`

The name of the Azure storage account

## azure-tier-class

Usage: `--azure-tier-class=name`

The name of the Azure tier-class. The possible values are:

* Hot

* Cool

* Archive


## cacert

Usage: `--cacert=name`

The path to the file with Certificate Authority (CA) certificates.

## curl-retriable-errors

Usage: `--curl-retriable-errors=name`

Add a new cURL error code as retriable. For multiple codes, use a comma-separated list.

## fifo-dir

Usage: `--fifo-dir=name`

The directory used to read or write named pipes. In the put mode, xbcloud reads from the named pipes. In the get mode, xbcloud writes to the named pipes.

## fifo-streams

Usage: `--fifo-streams=#`

The number of parallel FIFO stream threads.

## fifo-timeout

Usage: `--fifo-timeout=#`

The number of seconds to wait for the other end to open the stream. The default value is 60.

## google-access-key

Usage: `--google-access-key=name`

The Google Cloud storage access key

## google-bucket-name

Usage: `--google-bucket-name=name`

The Google Cloud storage bucket name

## google-endpoint

Usage: `--google-endpoint=name`

The Google Cloud storage endpoint

## google-region

Usage: `--google-region=name`

The Google Cloud storage region


## google-secret-key

Usage: `--google-secret-key=name`

The Google Cloud storage secret key

## google-session-token

Usage: `--google-session-token=name`

The Google Cloud storage session-token

## google-storage-class

Usage: `--google-storage-class=name`

The Google Cloud storage storage class

The possible values are the following:

* STANDARD

* NEARLINE

* COLDLINE

* ARCHIVE

## header

Usage: `--header=name`

Extra header

## http-retriable-errors

Usage: `--http-retriable-errors=name`

Add a new http error code as retriable. For multiple codes, use a comma-separated list.

## insecure

Usage: `--insecure`

Do not verify the certificate of the server.

## max-backoff

Usage: `--max-backoff=#`

The maximum backoff delay, in milliseconds, between chunk upload or chunk download retries. The default value is 300000.

## max-retries

Usage: `--max-retires=#`

The number of retries for chunk uploads or downloads after a failure. The default value is 10.

## md5

Usage: `--md5=name`

Uploads an MD5 file into the backup directory.

## parallel

Usage: `--parallel=#`

Defines the maximum number of concurrent upload/download requests. The default value is `1`.

## s3-access-key

Usage: `--s3-access-key=name`

The name of the s3 access key

## s3-api-version

Usage: `--s3-api-version=name`

The name of the s3 API version


## s3-bucket

Usage: `--s3-bucket=name`

The name of the s3 bucket

## s3-bucket-lookup

Usage: `--s3-bucket-lookup=name`

The name of the s3 bucket lookup method

## s3-endpoint

Usage: `--s3-endpoint=name`

The name of the s3 endpoint


## s3-region

Usage: `--s3-region=name`

The name of the s3 region

## s3-secret-key

Usage: `--s3-secret-key=name`

The name of the s3 secret key

## s3-session-token

Usage: `--s3-session-token=name`

The name of the s3 session token

## s3-storage-class

Usage: `--s3-storage-class=name`

The name of the s3 storage class and is used to pass custom storage class names provided by the other s3 implementations, such as MinIO.

The possible values are:

* STANDARD

* STANDARD_ID

* GLACIER

## storage name

Usage: `--storage=[S3|SWIFT|GOOGLE|AZURE]`

Defines the Cloud storage option. xbcloud supports Swift, MinIO, Google, Azure, and AWS S3. The default value is `swift`.

## swift-auth-url

Usage: `--swift-auth-url=name`

The Base URL of the Swift authentication service.

## swift-container

Usage: `--swift-container=name`

The Swift container used to store backups.

## swift-key

Usage: `--swift-key`

The Swift key/password (X-Auth-Key)

## swift-storage-url

Usage: `--swift-storage-url=name`

If a name is specified, the xbcloud attempts to get the object-store endpoint for a given region from the keystone response. This option overrides that value.

## swift-user

Usage: `--swift-user=name`

The Swift user name (X-Auth-User).


## timeout

Usage: `--timeout=#`

The number of seconds to wait for activity on the TCP connection. The default value is 120. If the value is 0 (zero), there is no timeout.

## verbose

Usage: `--verbose`

Turns on the cURL tracing.

## Swift authentication options

The Swift specification describes several [authentication options](http://docs.openstack.org/developer/swift/overview_auth.html). The *xbcloud* tool can
authenticate against keystone with API version 2 and 3.

## swift-auth-version

Usage: `--swift-auth-version=name`

Defines the swift authentication version used. 

The possible values are the following: 

* `1.0` - TempAuth

* `2.0` - Keystone v2.0

* `3` - Keystone v3. 

The default value is `1.0`.

## If `--swift-auth-version=2`, the additional options are:

### swift-password

Usage: `--swift-password=name`

Swift password for the user

### swift-region

Usage: `--swift-region=name`

Swift region object-store endpoint

### swift-tenant

Usage: `--swift-tenant=name`

The Swift tenant name 

Either of the `--swift-tenant` or `--swift-tenant-id` can be defined, but you should not use both options together. Both of these options are optional.

### swift-tenant-id

Usage: `--swift-tenant-id=name`

The Swift tenant ID

Either of the `--swift-tenant` or `--swift-tenant-id` can be defined, but you should not use both options together. Both of these options are optional.

## If `--swift-auth-version=3`, the  additional options are:

### swift-domain

Usage: `--swift-domain=name`

The Swift domain name

### swift-domain-id

Usage: `--swift-domain-id=name`

The Swift domain ID

### swift-project

Usage: `--swift-project=name`

The Swift project name

### swift-project-domain

Usage: `--swift-project-domain=name`

The Swift domain name

### swift-project-domain-id

Usage: `--swift-project-domain-id=name`

The Swift domain ID

### swift-project-id

Usage: `--swift-project-id=name`

The Swift project ID

### swift-user-id

Usage: `--swift-user-id=name`

The Swift user ID






