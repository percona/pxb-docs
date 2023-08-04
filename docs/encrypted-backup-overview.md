# Backup for an encrypted InnoDB tablespace overview

InnoDB supports [data encryption for InnoDB tables](https://dev.mysql.com/doc/refman/8.0/en/innodb-data-encryption.html)
stored in file-per-table tablespaces. This feature provides an at-rest
encryption for physical tablespace data files.

For an authenticated user or application to access an  encrypted 
tablespace, InnoDB uses the master encryption key to decrypt 
the tablespace key. The master encryption key is stored in a keyring. 
xtrabackup supports two keyring plugins: `keyring_file`, and 
`keyring_vault`. These plugins are installed into the `plugin` directory.

## Version updates

Percona XtraBackup 8.0.28-21 adds support for the Amazon Key Management
Service (AWS KMS). AWS KMS is cloud-based encryption and key management
service. The keys and functionality can be used for other AWS services
or your applications that use AWS. No configuration is required to back
up a server with AWS KMS-enabled encryption. 

Percona XtraBackup 8.0.27-19 adds support for the Key Management
Interoperability Protocol (KMIP) which enables the communication between
the key management system and encrypted database server. 

Percona XtraBackup 8.0.25-17 adds support for the [file-based keyring component](#use-the-component_keyring_file). MySQL uses the component-based infrastructure to extend the server capabilities. See a [comparison of keyring components and keyring plugins](https://dev.mysql.com/doc/refman/8.0/en/keyring-component-plugin-comparison.html)
for more information.


## Incremental encrypted InnoDB tablespace backups with `keyring_file`

The process of taking incremental backups with InnoDB tablespace encryption
is similar to taking the Incremental Backups with unencrypted tablespace. The `keyring-file` component should not used in production or for regulatory compliance.

## Create an incremental backup

To make an incremental backup, begin with a full backup. The xtrabackup
binary
writes a file called `xtrabackup_checkpoints` into the backup’s target
directory. This file contains a line showing the `to_lsn`, which is the
database’s LSN at the end of the backup. First you need to create a full
backup with the following command:

```{.bash data-prompt="$"}
$ xtrabackup --backup --target-dir=/data/backups/base \
--keyring-file-data=/var/lib/mysql-keyring/keyring
```

In order to prepare the backup, you must make a copy of the keyring file yourself. xtrabackup does not copy the keyring file into the backup directory.  Restoring the backup after the keyring has been changed causes errors like `ERROR 3185 (HY000): Can't find master key from keyring, please check keyring plugin is loaded.` when the restore process tries accessing an encrypted table.

If you look at the `xtrabackup_checkpoints` file, you should see
the output similar to the following:

??? example "Expected output"

    ```{.text .no-copy}
    backup_type = full-backuped
    from_lsn = 0
    to_lsn = 7666625
    last_lsn = 7666634
    compact = 0
    recover_binlog_info = 1
    ```

Now that you have a full backup, you can make an incremental backup based
on it. Use a command such as the following:

```{.bash data-prompt="$"}
$ xtrabackup --backup --target-dir=/data/backups/inc1 \
--incremental-basedir=/data/backups/base \
--keyring-file-data=/var/lib/mysql-keyring/keyring
```

To prepare the backup, you must copy the keyring file manually. xtrabackup does not copy the keyring file into the backup directory. 

If the
keyring has not been rotated you can use the same as the one you’ve
backed-up with the base backup. If the keyring has been rotated, or you have 
upgraded the plugin to a component, you must back up the keyring file. 
Otherwise, you cannot prepare the backup.

The `/data/backups/inc1/` directory should now contain delta files, such
as `ibdata1.delta` and `test/table1.ibd.delta`. These represent the
changes since the `LSN 7666625`. If you examine the
`xtrabackup_checkpoints` file in this directory, you should see 
the output similar to the following:

??? example "Expected output"

    ```{.text .no-copy}
    backup_type = incremental
    from_lsn = 7666625
    to_lsn = 8873920
    last_lsn = 8873929
    compact = 0
    recover_binlog_info = 1
    ```

Use this directory as the base for yet another incremental backup:

```{.bash data-prompt="$"}
$ xtrabackup --backup --target-dir=/data/backups/inc2 \
--incremental-basedir=/data/backups/inc1 \
--keyring-file-data=/var/lib/mysql-keyring/keyring
```

## Prepare incremental backups

The `--prepare` step for incremental backups is not the same as for
normal backups. In normal backups, two types of operations are performed to
make
the database consistent: committed transactions are replayed from the log
file
against the data files, and uncommitted transactions are rolled back. You
must
skip the rollback of uncommitted transactions when preparing a backup,
because
transactions that were uncommitted at the time of your backup may be in
progress, and it’s likely that they will be committed in the next
incremental
backup. You should use the `--apply-log-only` option to prevent the
rollback phase.

If you do not use the `--apply-log-only` option to prevent the rollback phase, then your incremental backups are useless. After transactions have been rolled back, further incremental backups cannot be applied.

Beginning with the full backup you created, you can prepare it and then
apply the incremental differences to it. Recall that you have the following backups:

```{.text .no-copy}
/data/backups/base
/data/backups/inc1
/data/backups/inc2
```

To prepare the base backup, you need to run `--prepare` as usual, but
prevent the rollback phase:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --apply-log-only --target-dir=/data/backups/base \
--keyring-file-data=/var/lib/mysql-keyring/keyring
```

??? example "Expected output"

    ```{.text .no-copy}
    InnoDB: Shutdown completed; log sequence number 7666643
    InnoDB: Number of pools: 1
    160401 12:31:11 completed OK!
    ```

To apply the first incremental backup to the full backup, you should use
the following command:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --apply-log-only --target-dir=/data/backups/base \
--incremental-dir=/data/backups/inc1 \
--keyring-file-data=/var/lib/mysql-keyring/keyring
```

The backup should be prepared with the keyring file and type that was used when backup was being taken. This means that if the keyring has been rotated, or you have upgraded from a plugin to a component between the base and incremental backup that you must use the keyring that was in use when the first incremental backup has been taken.

Preparing the second incremental backup is a similar process: apply the
deltas
to the (modified) base backup, and you will roll its data forward in 
time to the point of the second incremental backup:

```{.bash data-prompt="$"}
$ xtrabackup --prepare --target-dir=/data/backups/base \
--incremental-dir=/data/backups/inc2 \
--keyring-file-data=/var/lib/mysql-keyring/keyring
```
Use `--apply-log-only` when merging all incremental backups except the last one. That’s why the previous line does not contain the `--apply-log-only` option. Even if the `--apply-log-only` was used on the last step, backup would still be consistent but in that case  server would perform the rollback phase.

The backup is now prepared and can be restored with `--copy-back` option.
In case the keyring has been rotated you’ll need to restore the keyring which was used to take and prepare the backup.



