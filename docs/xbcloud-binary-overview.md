# The xbcloud binary overview

xbcloud is a cloud storage utility that works with Percona XtraBackup to upload, download, and manage database backups in cloud storage. It enables you to stream backups directly to cloud storage without requiring local disk space, making it ideal for large database environments.

## What's in this document

* [What xbcloud does](#what-xbcloud-does) - Core operations and capabilities

* [Supported cloud storage providers](#supported-cloud-storage-providers) - Available storage options

* [Key features](#key-features) - Streaming, chunking, and advanced features

* [Usage](#usage) - Common usage patterns and examples

* [Supplying parameters](#supplying-parameters) - Configuration methods

* [Advanced usage patterns](#advanced-usage-patterns) - Incremental backups and partial restore

## What xbcloud does

xbcloud provides three essential operations:

* **put** - Upload backups to cloud storage
* **get** - Download backups from cloud storage  
* **delete** - Remove backups from cloud storage

These operations work seamlessly with xtrabackup's streaming capabilities, allowing you to create a complete backup pipeline that streams data directly from your database to cloud storage.

## Supported cloud storage providers

xbcloud supports multiple cloud storage providers:

* Amazon S3 and S3-compatible services (MinIO, Wasabi, Digital Ocean Spaces)
* OpenStack Swift
* Google Cloud Storage
* Microsoft Azure

For detailed configuration instructions, see the individual provider guides:

* [Using the xbcloud binary with Amazon S3](xbcloud-s3.md)
* [Using the xbcloud binary with Swift](xbcloud-swift.md)  
* [Using the xbcloud binary with Google Cloud Storage](xbcloud-gcs.md)
* [Using the xbcloud binary with Microsoft Azure Cloud Storage](xbcloud-azure.md)
* [Using the xbcloud binary with MinIO](xbcloud-minio.md)

## Key features

### Streaming backups
xbcloud accepts input via pipes from xbstream, enabling direct streaming from xtrabackup to cloud storage without requiring local storage space.

### Chunked storage
Backups are stored as separate objects with names like `backup_name/database/table.ibd.NNN...`, where `NNN...` is a zero-padded serial number. The default chunk size is 10MB, which you can adjust using [`--read-buffer-size`](xtrabackup-option-reference.md#read-buffer-size).

### Advanced features
* [Exponential Backoff](xbcloud-exbackoff.md) - Automatically retries failed operations with increasing delays
* [FIFO data sink](xbcloud-binary-fifo-datasink.md) - Enables parallel streaming for high-bandwidth networks (10Gbps+)

!!! important

    To prevent intermittent backup failures, [update the curl utility](update-curl-utility.md).

## Usage

This section shows common xbcloud usage patterns. All examples use Amazon S3 for consistency, but the same principles apply to other storage providers.

### Creating a full backup

A full backup captures the entire database at a point in time. The following command creates a full backup and uploads it to S3:

```shell
xtrabackup --backup --stream=xbstream --target-dir=/tmp/backup | \
xbcloud put --storage=s3 --s3-bucket=my-backups --s3-region=us-west-2 full_backup_$(date +%Y%m%d)
```

This command:
1. Creates a backup using xtrabackup in streaming mode
2. Pipes the backup data to xbcloud
3. Uploads the backup to the S3 bucket with a timestamped name

### Creating an incremental backup

An incremental backup only includes changes since the last backup (full or incremental). First, create the incremental backup:

```shell
xtrabackup --backup --stream=xbstream --incremental-basedir=/tmp/backup \
--target-dir=/tmp/inc-backup | \
xbcloud put --storage=s3 --s3-bucket=my-backups --s3-region=us-west-2 inc_backup_$(date +%Y%m%d_%H%M)
```

### Restoring from cloud storage

To restore a backup, download it from cloud storage and prepare it:

```shell
# Download the backup
xbcloud get --storage=s3 --s3-bucket=my-backups --s3-region=us-west-2 full_backup_20240101 | \
xbstream -xv -C /tmp/restore

# Prepare the backup for use
xtrabackup --prepare --target-dir=/tmp/restore
```

### Partial restore

You can restore specific tables without downloading the entire backup:

```shell
# Download only specific tables
xbcloud get --storage=s3 --s3-bucket=my-backups --s3-region=us-west-2 \
full_backup_20240101 ibdata1 sakila/payment.ibd > /tmp/partial.xbs

# Extract the partial backup
xbstream -xv -C /tmp/partial < /tmp/partial.xbs
```

!!! note
   
    In a Bash shell, the `$?` parameter returns the exit code
    from the last binary. If you use pipes, the
    ${PIPESTATUS[x]} array parameter returns the exit code for each 
    binary in the pipe string.

    ```shell
    xtrabackup --backup --stream=xbstream --target-dir=/storage/backups/ | xbcloud put [options] full_backup
    ...
    ${PIPESTATUS[x]}
    0 0
    true | false
    echo $?
    1
    
    # with PIPESTATUS
    true | false
    echo ${PIPESTATUS[0]} ${PIPESTATUS[1]}
    0 1
    ```

## Supplying parameters

Each storage type has mandatory parameters that you can supply on the command
line, in a configuration file, and via environment variables.

### Configuration files

The parameters the values of which do not change frequently can be stored in
`my.cnf` or in a custom configuration file. The following example is a
template of configuration options under the `[xbcloud]` group:

```text
[xbcloud]
storage=s3
s3-endpoint=http://localhost:9000/
s3-access-key=minio
s3-secret-key=minio123
s3-bucket=backupsx
s3-bucket-lookup=path
s3-api-version=4
```

!!! note

    If you explicitly use a parameter on the command line and in a configuration file, xbcloud uses the value provided on the command line.

### Environment variables

Environment variables provide a secure way to configure xbcloud without exposing credentials in command lines or scripts. xbcloud automatically maps environment variables to their corresponding command-line parameters.

#### How precedence works

When the same parameter is specified in multiple ways, xbcloud uses this precedence order (highest to lowest):

1. Command-line parameters
2. Configuration file values  
3. Environment variables

#### Common environment variables

Each storage provider uses different environment variable names:

* **Amazon S3**: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`
* **OpenStack Swift**: `OS_AUTH_URL`, `OS_USERNAME`, `OS_PASSWORD`
* **Microsoft Azure**: `AZURE_STORAGE_ACCOUNT`, `AZURE_CONTAINER_NAME`, `AZURE_ACCESS_KEY`
* **Google Cloud**: `GOOGLE_ACCESS_KEY`, `GOOGLE_SECRET_KEY`, `GOOGLE_BUCKET_NAME`

#### Example usage

Set environment variables for your storage provider:

```bash
# For Amazon S3
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-west-2"

# Now use xbcloud without specifying credentials
xtrabackup --backup --stream=xbstream | xbcloud put s3://my-bucket/backup-$(date +%Y%m%d)
```

For complete environment variable reference and advanced usage patterns, see [Using environment variable files (.env) with xbcloud](xbcloud-env.md).

#### Security best practices

Environment variable files (`.env`) provide a secure way to manage xbcloud credentials without exposing sensitive information in command lines or scripts. These files store your cloud storage credentials and configuration settings, making them easy to manage and share across different environments while keeping them out of version control.

For detailed guidance on using `.env` files with xbcloud, including setup instructions, security best practices, and troubleshooting tips, see [Using environment variable files (.env) with xbcloud](xbcloud-env.md).

* Never commit environment variables to version control

* Use environment variable files (`.env`) that are excluded from version control

* Set appropriate file permissions on environment variable files (600 or 400)

* Use IAM roles and instance profiles when possible instead of access keys

* Rotate credentials regularly

* Use temporary credentials (session tokens) for short-term access

#### Troubleshooting

Environment variables not being recognized:

* Verify the variable name matches exactly (case-sensitive)

* Check that the variable is exported: `export VARIABLE_NAME="value"`

* Confirm the variable is set: `echo $VARIABLE_NAME`

* Test with a simple command first

Common issues:

* Mixed authentication methods: Avoid mixing environment variables with command-line parameters for the same setting

* Incorrect variable names: Double-check the exact environment variable names for your storage type

* Missing exports: Ensure variables are exported, not just set locally

For detailed examples and storage-specific configuration, see the individual storage provider documentation:

* [Using the xbcloud binary with Amazon S3](xbcloud-s3.md#environment-variables)

* [Using the xbcloud binary with Swift](xbcloud-swift.md#create-a-full-backup-with-swift)

* [Using the xbcloud binary with Microsoft Azure Cloud Storage](xbcloud-azure.md#options)

* [Using the xbcloud binary with Google Cloud Storage](xbcloud-gcs.md)

* [Using the xbcloud binary with MinIO](xbcloud-minio.md)

### Shortcuts

For all operations (put, get, and delete), you can use a shortcut to specify the
storage type, bucket name, and backup name as one parameter instead of using
three distinct parameters (–storage, –s3-bucket, and backup name per se).

!!! note

    Use the following format: ``storage-type://bucket-name/backup-name``

    In this example s3 refers to a storage type, operator-testing 
    is a bucket name, and bak22 is the backup name. 

    ```shell
    xbcloud get s3://operator-testing/bak22 ...
    ```
    
    This shortcut expands as follows:

    ```shell
    xbcloud get --storage=s3 --s3-bucket=operator-testing bak22 ...
    ```

You can supply the mandatory parameters on the command line,
configuration files, and in environment variables.

### Additional parameters

xbcloud accepts additional parameters that you can use with any storage
type. The `--md5` parameter computes the MD5 hash value of the backup
chunks. The result is stored in files that following the `backup_name.md5`
pattern.

```shell
xtrabackup --backup --stream=xbstream \
--parallel=8 2>backup.log | xbcloud put s3://operator-testing/bak22 \
--parallel=8 --md5 2>upload.log
```

You may use the `--header` parameter to pass an additional HTTP
header with the server side encryption while specifying a customer key.

An example of using the ``--header`` for AES256 encryption.

```shell
xtrabackup --backup --stream=xbstream --parallel=4 | \
xbcloud put s3://operator-testing/bak-enc/ \
--header="X-Amz-Server-Side-Encryption-Customer-Algorithm: AES256" \
--header="X-Amz-Server-Side-Encryption-Customer-Key: CuStoMerKey=" \
--header="X-Amz-Server-Side-Encryption-Customer-Key-MD5: CuStoMerKeyMd5==" \
--parallel=8
```

The `--header` parameter is also useful to set the access control list (ACL)
permissions: `--header="x-amz-acl: bucket-owner-full-control`

## Advanced usage patterns

### Incremental backup workflow

Incremental backups capture only changes since the last backup, making them faster and more storage-efficient. Here's the complete workflow using S3:

#### Step 1: Create the base full backup

```shell
xtrabackup --backup --stream=xbstream --target-dir=/tmp/base | \
xbcloud put --storage=s3 --s3-bucket=my-backups --s3-region=us-west-2 \
full_backup_20240101
```

#### Step 2: Create incremental backups

```shell
xtrabackup --backup --stream=xbstream --incremental-basedir=/tmp/base \
--target-dir=/tmp/inc1 | \
xbcloud put --storage=s3 --s3-bucket=my-backups --s3-region=us-west-2 \
inc_backup_20240101_1200
```

#### Step 3: Restore incremental backups

To restore from incremental backups, you must download and prepare them in sequence:

```shell
# Download and prepare the full backup
xbcloud get --storage=s3 --s3-bucket=my-backups --s3-region=us-west-2 \
full_backup_20240101 | xbstream -xv -C /tmp/restore

xtrabackup --prepare --apply-log-only --target-dir=/tmp/restore

# Download and apply the incremental backup
xbcloud get --storage=s3 --s3-bucket=my-backups --s3-region=us-west-2 \
inc_backup_20240101_1200 | xbstream -xv -C /tmp/inc1

xtrabackup --prepare --apply-log-only --target-dir=/tmp/restore \
--incremental-dir=/tmp/inc1

# Final prepare step
xtrabackup --prepare --target-dir=/tmp/restore
```

!!! note
   
    Accelerate the prepare phase for incremental backups with many InnoDB Data (IBD) files by using the `--parallel` option to process delta files concurrently. When using `--parallel` in the prepare phase, always specify a numeric value. The recommended minimum value is 4 (for example, `--parallel=4`).
    
    ```shell
    xtrabackup --prepare --apply-log-only \
    --target-dir=/tmp/restore \
    --incremental-dir=/tmp/inc1 --parallel=4

    xtrabackup --prepare --target-dir=/tmp/restore --parallel=4
    ```

### Partial restore

You can restore specific tables without downloading the entire backup:

```shell
# Download only specific tables
xbcloud get --storage=s3 --s3-bucket=my-backups --s3-region=us-west-2 \
full_backup_20240101 ibdata1 sakila/payment.ibd > /tmp/partial.xbs

# Extract the partial backup
xbstream -xv -C /tmp/partial < /tmp/partial.xbs
```

## Next steps

Now that you understand the basics of xbcloud, here are the recommended next steps:


* Choose your storage provider
  Review the [supported cloud storage providers](#supported-cloud-storage-providers) and select the one that best fits your needs

* Set up authentication
  Follow the provider-specific guide to configure credentials:

  * [Using the xbcloud binary with Amazon S3](xbcloud-s3.md)  
  * [Using the xbcloud binary with Swift](xbcloud-swift.md)  
  * [Using the xbcloud binary with Google Cloud Storage](xbcloud-gcs.md)  
  * [Using the xbcloud binary with Microsoft Azure Cloud Storage](xbcloud-azure.md)  
  * [Using the xbcloud binary with MinIO](xbcloud-minio.md)

* Configure security
  Learn about secure credential management with [Using environment variable files (.env) with xbcloud](xbcloud-env.md)

* Explore advanced features
  Review the [xbcloud command-line options](xbcloud-options.md) for detailed parameter reference

* Test your setup
  Start with a simple full backup using the examples in the [Usage](#usage) section


For troubleshooting and additional help, see the [Troubleshooting](#troubleshooting) section or contact [Percona support](get-help.md).
