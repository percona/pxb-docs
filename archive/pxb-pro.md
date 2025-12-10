# Percona XtraBackup Pro

--8<--- "pro-build-announcement.md"

## Capabilities

The following capabilities have been tested for {{release}} and are available in Percona XtraBackup Pro:

| Name                                | Available since | Description  | 
| ----------------------------------- | ------------- | -------------|
| [Reduced backup lock time](reduction-in-locks.md)| 8.4.0-2 | Reduces the time the server remains locked by `xtrabackup` during full and incremental backups. Allows `Data Definition Language` (DDL) operations on the server while the backup is in progress.|
| Install [Amazon Linux 2023](install-pro.md)| 8.4.0-2 | Amazon Linux 2023 is a purpose-built Linux distribution optimized for AWS. It's designed for performance, security, and seamless integration with the broader AWS ecosystem. We support both AMD64 and ARM64 versions of Amazon Linux 2023.|

## What's in it for you?

* Save on deploying and maintaining build infrastructure as we do the build and testing for you 
* Longer support for older versions of operating systems.  

[Install Percona XtraBackup Pro](install-pro.md){.md-button}

Community users can receive all these capabilities by [building Percona XtraBackup from the same source code](compile-xtrabackup.md).