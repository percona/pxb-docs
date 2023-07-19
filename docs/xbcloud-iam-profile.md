# Use the xbcloud binary with an IAM instance profile

This feature is [tech preview](glossary.md#tech-preview). Before using this feature in production, we recommend that you test restoring from physical backups in your environment and also use the alternative backup method for redundancy.

[Percona XtraBackup 8.0.31-24](release-notes/8.0/8.0.31-24.0.md) adds the ability to use the IAM instance profile when running xbcloud from an EC2 instance.

An authentication system has two elements:

* Who am I?
* What can I do?

A role defines "what can I do." A role provides a method to define a collection of permissions. Roles are assigned to users, services and EC2 instances, the "who am I" element.

The IAM instance profile is the "who" for an EC2 instance and assumes the IAM role, which has permissions. The instance profile has the same name as the IAM role.

An IAM instance profile does not need the `--s3-secret-key` nor the `--s3-access-key` if they are running `xbcloud` from an Amazon EC2 instance. To configure or attach an instance metadata to an EC2 instance, see [How can I grant my Amazon EC2 instance access to an Amazon S3 bucket](https://aws.amazon.com/premiumsupport/knowledge-center/ec2-instance-access-s3-bucket/). 

An example of the command:

```text
$ xtrabackup ... | xbcloud put --storage=s3 --s3-bucket=bucket-name backup-name
```

The xbcloud binary outputs a connect message when successful.

??? example "Expected output"

    ```text
    221121 13:16:26 Using instance metadata for access and secret key
    221121 13:16:26 xbcloud: Successfully connected.
    ```

An important consideration is that the instance metadata has a time to live (TTL) of 6 hours. A backup that takes more than that time contains Expired token errors. Use [Exponential Backoff](xbcloud-exbackoff.md) to retry the upload after fetching new keys from the instance metadata.

??? example "Output when keys have expired"

    ```text
    221121 13:04:52 xbcloud: S3 error message: The provided token has expired.
    221121 13:04:52 xbcloud: Sleeping for 2384 ms before retrying test/mysql.ibd.00000000000000000002 [1]
    221121 13:04:55 xbcloud: S3 error message: The provided token has expired.
    221121 13:04:55 xbcloud: Sleeping for 2887 ms before retrying test/mysql.ibd.00000000000000000003 [1]
    221121 13:04:58 xbcloud: S3 error message: The provided token has expired.
    221121 13:04:58 xbcloud: Sleeping for 2778 ms before retrying test/undo_002.00000000000000000000 [1]
    221121 13:05:00 xbcloud: S3 error message: The provided token has expired.
    221121 13:05:00 xbcloud: Sleeping for 2916 ms before retrying test/undo_002.00000000000000000001 [1]
    221121 13:05:03 xbcloud: S3 error message: The provided token has expired.
    221121 13:05:03 xbcloud: Sleeping for 2794 ms before retrying test/undo_002.00000000000000000002 [1]
    221121 13:05:06 xbcloud: S3 error message: The provided token has expired.
    221121 13:05:06 xbcloud: Sleeping for 2336 ms before retrying test/undo_001.00000000000000000000 [1]
    221121 13:05:09 xbcloud: successfully uploaded chunk: test/mysql.ibd.00000000000000000002, size: 5242923
    221121 13:05:09 xbcloud: successfully uploaded chunk: test/mysql.ibd.00000000000000000003, size: 23
    221121 13:05:09 xbcloud: successfully uploaded chunk: test/undo_002.00000000000000000000, size: 10485802
    221121 13:05:09 xbcloud: successfully uploaded chunk: test/undo_002.00000000000000000001, size: 6291498
    221121 13:05:09 xbcloud: successfully uploaded chunk: test/undo_002.00000000000000000002, size: 22
    221121 13:05:09 xbcloud: successfully uploaded chunk: test/undo_001.00000000000000000000, size: 10485802
    221121 13:05:10 xbcloud: successfully uploaded chunk: test/undo_001.00000000000000000001, size: 6291498
    221121 13:05:10 xbcloud: successfully uploaded chunk: test/undo_001.00000000000000000002, size: 22
    . . .
    221121 13:05:18 xbcloud: successfully uploaded chunk: test/xtrabackup_tablespaces.00000000000000000001, size: 36
    221121 13:05:19 xbcloud: Upload completed. 
    ```
