# Percona XtraBackup binaries overview

Percona XtraBackup provides a comprehensive suite of command-line tools for MySQL database backup and recovery operations. This document introduces the four core binaries that form the foundation of Percona XtraBackup's functionality, helping you understand when and how to use each tool effectively.

## Prerequisites

Before using Percona XtraBackup binaries, ensure you have:

- Appropriate database privileges for backup operations

- Sufficient disk space for backup storage

- Network access (for cloud storage operations)

## Core binaries

### xtrabackup


Purpose: The primary backup and restore utility for MySQL databases.

Key Capabilities:

* Creates hot backups without locking tables

* Supports full, incremental, and compressed backups

* Handles InnoDB, MyISAM, and other storage engines

* Provides point-in-time recovery capabilities

Common Use Cases:

* Daily full database backups

* Incremental backup strategies

* Database migration and cloning

* Disaster recovery preparation

Basic Syntax:

Run the following commands as root or use the sudo command.

```shell
# Create a full backup
xtrabackup --backup --target-dir=/backup/full

# Create an incremental backup
xtrabackup --backup --target-dir=/backup/inc1 --incremental-basedir=/backup/full

# Prepare a backup for restore
xtrabackup --prepare --target-dir=/backup/full
```

Documentation: [xtrabackup Overview](xtrabackup-binary-overview.md)

Command Line Options: [xtrabackup Options](xtrabackup-option-reference.md)

### xbcloud

Purpose: Cloud storage management for backup files.

Key Capabilities:

* Uploads and downloads backups to/from cloud providers

* Supports Amazon S3, Google Cloud Storage, Azure Blob Storage, and MinIO

* Handles large backup files efficiently

* Provides parallel upload/download operations

Common Use Cases:

* Off-site backup storage

* Cross-region backup replication

* Cloud-based disaster recovery

* Backup archival and long-term storage

Basic Syntax:

Run the following commands as root or use the sudo command.

```shell
# Upload backup to S3
xbcloud put s3://my-bucket/backup/ --storage=s3 --s3-bucket=my-bucket

# Download backup from S3
xbcloud get s3://my-bucket/backup/ --storage=s3 --s3-bucket=my-bucket
```

Documentation: [xbcloud Overview](xbcloud-binary-overview.md)

Command Line Options: [xbcloud Options](xbcloud-options.md)

### xbcrypt


Purpose: Encryption and decryption of backup files.

Key Capabilities:

* Encrypts backup files using AES encryption

* Supports multiple encryption algorithms

* Provides secure key management

* Handles both individual files and backup streams

Common Use Cases:

* Securing sensitive database backups

* Compliance with data protection regulations

* Secure backup transmission

* Long-term encrypted storage

Basic Syntax:

Run the following commands as root or use the sudo command.

```shell
# Encrypt a backup file
xbcrypt --encrypt --encrypt-key-file=/path/to/keyfile --input=/backup/backup.xbstream

# Decrypt a backup file
xbcrypt --decrypt --encrypt-key-file=/path/to/keyfile --input=/backup/backup.xbstream.encrypted
```

Documentation: [xbcrypt Overview](xbcrypt-binary-overview.md)

Command Line Options: [xbcrypt Options](xbcrypt-options.md)

### xbstream

Purpose: Streaming backup data for efficient handling of large files.

Key Capabilities:

* Streams backup data to and from files

* Supports compression and decompression

* Handles backup streaming over networks

* Works with standard Unix pipes and redirection

Common Use Cases:

* Streaming backups over network connections

* Real-time backup processing

* Integration with other backup tools

* Efficient handling of large backup files

Basic Syntax:

Run the following commands as root or use the sudo command.

```shell
# Extract a streamed backup
xbstream -x -C /restore/directory < backup.xbstream

# Create a streamed backup
xtrabackup --backup --stream=xbstream | xbstream -c -C /backup/directory
```

Documentation: [xbstream Overview :octicons-link-external-16:](https://docs.percona.com/percona-xtrabackup/{{vers}}/xbstream-binary-overview.html)

Command Line Options: [xbstream Options](xbstream-options.md)

## Common workflows

### Basic backup workflow

1. Create a full backup using `xtrabackup`

2. Optionally encrypt using `xbcrypt`

3. Upload to cloud storage using `xbcloud`

4. Verify backup integrity

### Incremental backup strategy

1. Create initial full backup

2. Create incremental backups based on the full backup

3. Stream incremental backups using `xbstream`

4. Store encrypted backups in cloud storage

### Disaster recovery workflow

1. Download backup from cloud storage

2. Decrypt backup files if necessary

3. Prepare backup using `xtrabackup --prepare`

4. Restore database from prepared backup

## Code examples

### Complete backup and upload workflow

Run the following commands as root or use the sudo command.

```shell
# Create encrypted backup
xtrabackup --backup --target-dir=/tmp/backup --encrypt=AES256 --encrypt-key-file=/etc/mysql/backup.key

# Stream and compress backup
xtrabackup --backup --stream=xbstream --encrypt=AES256 --encrypt-key-file=/etc/mysql/backup.key | \
  xbstream -c -C /tmp/backup

# Upload to cloud storage
xbcloud put s3://my-backup-bucket/$(date +%Y%m%d)/ --storage=s3 --s3-bucket=my-backup-bucket
```

### Restore from cloud storage

Run the following commands as root or use the sudo command.

```shell
# Download backup from cloud
xbcloud get s3://my-backup-bucket/20241201/ --storage=s3 --s3-bucket=my-backup-bucket

# Decrypt backup
xbcrypt --decrypt --encrypt-key-file=/etc/mysql/backup.key --input=/tmp/backup/backup.xbstream.encrypted

# Prepare and restore
xtrabackup --prepare --target-dir=/tmp/backup
xtrabackup --copy-back --target-dir=/tmp/backup
```

## Next steps

Now that you understand the core binaries, consider these next steps:

1. Installation: Follow the [installation guide](installation.md) for your operating system

2. Configuration: Review [configuration options](configure-xtrabackup.md) for your environment

3. Quick Start: Try the [quickstart guide](quickstart-overview.md) for hands-on experience

4. Advanced Topics: Explore [point-in-time recovery](point-in-time-recovery.md) and [replication setup](set-up-replication.md)

## Related documentation

* [Backup and Restore overview](backup-overview.md)

* [Get help](get-help.md)
