> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-xtrabackup/9.7/llms.txt).

# Percona XtraBackup binaries overview

Percona XtraBackup provides a comprehensive suite of command-line tools for MySQL database backup and recovery operations. This document introduces the four core binaries that form the foundation of Percona XtraBackup’s functionality, helping you understand when and how to use each tool effectively.

## Version changes

Percona XtraBackup 9.7.2-2 renames the `--incremental-basedir` option to [`--backup-incremental-base`](https://docs.percona.com/percona-xtrabackup/9.7/xtrabackup-option-reference.html#backup-incremental-base). Percona XtraBackup still accepts `--incremental-basedir` but prints a deprecation warning. A future release will remove `--incremental-basedir`, so update your scripts to use `--backup-incremental-base`. If you pass both options in the same command, Percona XtraBackup reports an error and does not start.

## Prerequisites

Before using Percona XtraBackup binaries, ensure you have:

- Appropriate database privileges for backup operations
- Sufficient disk space for backup storage
- Network access (for cloud storage operations)

## Core binaries

### xtrabackup

Purpose: The primary backup and restore utility for MySQL databases.

Key Capabilities:

- Creates hot backups without locking tables
- Supports full, incremental, and compressed backups
- Handles InnoDB, MyISAM, and other storage engines
- Provides point-in-time recovery capabilities

Common Use Cases:

- Daily full database backups
- Incremental backup strategies
- Database migration and cloning
- Disaster recovery preparation

Basic Syntax:

Run the following commands as root or use the sudo command.

```
# Create a full backup
xtrabackup --backup --target-dir=/backup/full

# Create an incremental backup
xtrabackup --backup --target-dir=/backup/inc1 --backup-incremental-base=/backup/full

# Prepare a backup for restore
xtrabackup --prepare --target-dir=/backup/full
```

Documentation: [xtrabackup Overview](https://docs.percona.com/percona-xtrabackup/9.7/xtrabackup-binary-overview.html)

Command Line Options: [xtrabackup Options](https://docs.percona.com/percona-xtrabackup/9.7/xtrabackup-option-reference.html)

### xbcloud

Purpose: Cloud storage management for backup files.

Key Capabilities:

- Uploads and downloads backups to/from cloud providers
- Supports Amazon S3, Google Cloud Storage, Azure Blob Storage, and MinIO
- Handles large backup files efficiently
- Provides parallel upload/download operations

Common Use Cases:

- Off-site backup storage
- Cross-region backup replication
- Cloud-based disaster recovery
- Backup archival and long-term storage

Basic Syntax:

Run the following commands as root or use the sudo command.

```
# Upload backup to S3
xbcloud put s3://my-bucket/backup/ --storage=s3 --s3-bucket=my-bucket

# Download backup from S3
xbcloud get s3://my-bucket/backup/ --storage=s3 --s3-bucket=my-bucket
```

Documentation: [xbcloud Overview](https://docs.percona.com/percona-xtrabackup/9.7/xbcloud-binary-overview.html)

Command Line Options: [xbcloud Options](https://docs.percona.com/percona-xtrabackup/9.7/xbcloud-options.html)

### xbcrypt

Purpose: Encryption and decryption of backup files.

Key Capabilities:

- Encrypts backup files using AES encryption
- Supports multiple encryption algorithms
- Provides secure key management
- Handles both individual files and backup streams

Common Use Cases:

- Securing sensitive database backups
- Compliance with data protection regulations
- Secure backup transmission
- Long-term encrypted storage

Basic Syntax:

Run the following commands as root or use the sudo command.

```
# Encrypt a backup file
xbcrypt --encrypt --encrypt-key-file=/path/to/keyfile --input=/backup/backup.xbstream

# Decrypt a backup file
xbcrypt --decrypt --encrypt-key-file=/path/to/keyfile --input=/backup/backup.xbstream.encrypted
```

Documentation: [xbcrypt Overview](https://docs.percona.com/percona-xtrabackup/9.7/xbcrypt-binary-overview.html)

Command Line Options: [xbcrypt Options](https://docs.percona.com/percona-xtrabackup/9.7/xbcrypt-options.html)

### xbstream

Purpose: Streaming backup data for efficient handling of large files.

Key Capabilities:

- Streams backup data to and from files
- Supports compression and decompression
- Handles backup streaming over networks
- Works with standard Unix pipes and redirection

Common Use Cases:

- Streaming backups over network connections
- Real-time backup processing
- Integration with other backup tools
- Efficient handling of large backup files

Basic Syntax:

Run the following commands as root or use the sudo command.

```
# Extract a streamed backup
xbstream -x -C /restore/directory < backup.xbstream

# Create a streamed backup
xtrabackup --backup --stream=xbstream | xbstream -c -C /backup/directory
```

Documentation: [xbstream Overview](https://docs.percona.com/percona-xtrabackup/9.7/xbstream-binary-overview.html)

Command Line Options: [xbstream Options](https://docs.percona.com/percona-xtrabackup/9.7/xbstream-options.html)

## Common workflows

### Basic backup workflow

1. Create a full backup using `xtrabackup`
1. Optionally encrypt using `xbcrypt`
1. Upload to cloud storage using `xbcloud`
1. Verify backup integrity

### Incremental backup strategy

1. Create initial full backup
1. Create incremental backups based on the full backup
1. Stream incremental backups using `xbstream`
1. Store encrypted backups in cloud storage

### Disaster recovery workflow

1. Download backup from cloud storage
1. Decrypt backup files if necessary
1. Prepare backup using `xtrabackup --prepare`
1. Restore database from prepared backup

## Code examples

### Complete backup and upload workflow

Run the following commands as root or use the sudo command.

```
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

```
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

1. Installation: Follow the [installation guide](https://docs.percona.com/percona-xtrabackup/9.7/installation.html) for your operating system
1. Configuration: Review [configuration options](https://docs.percona.com/percona-xtrabackup/9.7/configure-xtrabackup.html) for your environment
1. Quick Start: Try the [quickstart guide](https://docs.percona.com/percona-xtrabackup/9.7/quickstart-overview.html) for hands-on experience
1. Advanced Topics: Explore [point-in-time recovery](https://docs.percona.com/percona-xtrabackup/9.7/point-in-time-recovery.html) and [replication setup](https://docs.percona.com/percona-xtrabackup/9.7/set-up-replication.html)

## Related documentation

- [Backup and Restore overview](https://docs.percona.com/percona-xtrabackup/9.7/backup-overview.html)
- [Get help](https://docs.percona.com/percona-xtrabackup/9.7/get-help.html)
