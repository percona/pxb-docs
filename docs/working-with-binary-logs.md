# Work with binary logs

The `xtrabackup` binary integrates with the `log_status table`. This integration enables `xtrabackup` to print out the backup’s corresponding binary log position, so that you can use this binary log position to provision a new replica or perform point-in-time recovery.

## Find the binary log position

You can find the binary log position corresponding to a backup after the backup has been taken. If your backup is from a server with binary logging enabled, `xtrabackup` creates a file named `xtrabackup_binlog_info` in the target directory. This file contains the binary log file name and position of the exact point when the backup was taken.

??? example "Expected output during the backup stage"

    ```{.text .no-copy}
    210715 14:14:59 Backup created in directory '/backup/'
    MySQL binlog position: filename 'binlog.000002', position '156'
    . . .
    210715 14:15:00 completed OK!
    ```

## Point-in-time recovery

To perform a point-in-time recovery from an `xtrabackup` backup, you should prepare and restore the backup, and then replay binary logs from the point shown in the `xtrabackup_binlog_info` file.

Find a more detailed procedure in the [Point-in-time recovery](point-in-time-recovery.md) document.

## Set up a new replication replica

To set up a new replica, you should prepare the backup, and restore it to the data directory of your new replication replica. In the [CHANGE_REPLICATION_SOURCE_TO with the appropriate options](https://dev.mysql.com/doc/refman/8.1/en/change-replication-source-to.html) command, use the binary log filename and position shown in the `xtrabackup_binlog_info` file to start replication.

A more detailed procedure is found in  [How to setup a replica for replication in 6 simple steps with Percona XtraBackup](set-up-replication.md).
