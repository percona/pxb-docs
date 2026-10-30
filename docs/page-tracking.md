# Take an incremental backup using page tracking

To create an incremental backup with page tracking, Percona XtraBackup uses
the MySQL `mysqlbackup` component. This component provides a list of pages
modified since the last backup, and Percona XtraBackup copies only those
pages. This operation removes the need to scan the pages in the
database. Page tracking can improve the speed of incremental backups. The
speed depends on the number of read requests, not on the number of changed
pages. Scattered changed pages need more read requests than consecutive
changed pages. For details, see [Read scattered changed pages](#read-scattered-changed-pages).

Run the following commands as root or use the sudo command.

## Install the component

To start using the page tracking functionality, do the following:
{.power-number}

1. Install the `mysqlbackup` component and enable it on the server:

    ```sql
    INSTALL COMPONENT "file://component_mysqlbackup";
    ```

2. Check whether the `mysqlbackup` component is installed successfully:

    ```sql
    SELECT COUNT(1) FROM mysql.component WHERE component_urn='file://component_mysqlbackup';
    ```

## Use page tracking

You can enable the page tracking functionality for the full and incremental
backups with the `--page-tracking` option.

The option has the following benefits:

* Resets page tracking to the start of the backup. This reset allows the next incremental backup to use page tracking.

* Allows the use of page tracking for an incremental backup if the page tracking data is available from the backup’s start checkpoint LSN.

Percona XtraBackup processes a list of all the tracked pages in memory. If Percona XtraBackup does not have enough available memory to process this list, the process throws an error and exits. For example, if an incremental backup uses 200GB, Percona XtraBackup can use an additional 100MB of memory to process and store the page tracking data. 

The examples of creating full and incremental backups using the `--page-tracking` option:

=== "Full backup"

    ```shell
    xtrabackup --backup --target-dir=$FULL_BACK --page-tracking
    ```

=== "Incremental backup"

    ```shell
    xtrabackup --backup --target-dir=$INC_BACKUP  
    --incremental-basedir=$FULL_BACKUP --page-tracking
    ```

After enabling the functionality, the next incremental backup finds changed
pages using page tracking.

### Read scattered changed pages

#### Version changes

Percona XtraBackup 9.7.2-2 introduces the [`--page-tracking-merge-gap`](xtrabackup-option-reference.md#page-tracking-merge-gap) option.

#### How Percona XtraBackup reads scattered changed pages

During an incremental backup with page tracking, Percona XtraBackup reads only the pages that the server reports as changed. Percona XtraBackup reads consecutive changed pages together, but reads each scattered changed page on its own. Thousands of small reads take far longer than a few large ones, so an incremental backup of a large tablespace can be slow even when little data has changed.

When two changed pages are close together, reading the unchanged pages between them costs less than issuing another read. Percona XtraBackup combines these reads automatically. Percona XtraBackup discards the extra pages when writing the delta, so the backup contents and size stay the same. Only the read pattern changes.

Use the default value, `auto`. With `--page-tracking-merge-gap=auto`, Percona XtraBackup measures the request round trip and sequential read speed of your storage at the start of each backup. Then Percona XtraBackup calculates the gap for each tablespace from the tablespace page size. The measurement adapts to the storage that the backup runs on, and a fixed value cannot adapt. You do not need to set the option.

`--page-tracking-merge-gap` accepts the following values:

* `auto` (default, recommended): Percona XtraBackup measures your storage and selects the gap for each tablespace, as described above.

* A page count, for example, `8`: Percona XtraBackup reads changed pages separated by up to 8 unchanged pages in a single request, for every tablespace, and skips the measurement. Percona XtraBackup applies the same value regardless of the storage and the page size, so a fixed value can read far more data than necessary or split the reads into too many small requests. Both cases slow down the backup. Set a value only after you benchmark your own workload and confirm that `auto` does not give the best result. Check the value again after a hardware change.

* `0`: turns off the feature. Percona XtraBackup reads together only strictly consecutive changed pages, as in releases before 9.7.2-2.

```shell
xtrabackup --backup --target-dir=/data/inc1 \
  --incremental-basedir=/data/full \
  --page-tracking --page-tracking-merge-gap=8
```

The backup log reports the measurement once. For each tablespace with at least 1000 changed pages, the log then reports the number of changed pages, the number of reads without combining, the number of reads after combining, and the resulting read amplification. If the typical gap in a table costs too much to combine, the log reports the gap and suggests a value to set. Check these log lines when you compare a fixed value with `auto`.

Combining reads more bytes than the changed pages alone. Keep that in mind if your storage provider charges for reads or limits read throughput. To avoid the extra reads, set the option to `0`.

The first full backup using page tracking, Percona XtraBackup may have a delay. The following is an example of the message:

??? example "Expected output"

    ```{.text .no-copy}
    xtrabackup: pagetracking: Sleeping for 1 second, waiting for checkpoint lsn 17852922 /
    to reach to page tracking start lsn 21353759
    ```

Enable page tracking before creating the first backup to avoid this delay. This method ensures that the page tracking log sequence number (LSN) is higher than the checkpoint LSN of the server.

## Start page tracking manually

After the mysqlbackup component is loaded and active on the server, you can
start page tracking manually with the following option:

```sql
SELECT mysqlbackup_page_track_set(true);
```

## Check the LSN value

Check the LSN value starting from which changed pages are tracked with the
following option:

```sql
SELECT mysqlbackup_page_track_get_start_lsn();
```

## Stop page tracking

To stop page tracking, use the following command:

```sql
SELECT mysqlbackup_page_track_set(false);
```

## Purge page tracking data

When you start page tracking, it creates a file under the server’s datadir
to collect data about changed pages. This file grows until you stop the
page tracking. If you stop the server and then restart it, page tracking
creates a new file but also keeps the old one. The old file continues to
grow until you stop the page tracking explicitly.

If you purge the page tracking data, you should create a full backup
afterward. To purge the page tracking data, do the following steps:

```sql
SELECT mysqlbackup_page_track_set(false);
SELECT mysqlbackup_page_track_purge_up_to(9223372036854775807);
/* Specify the LSN up to which you want to purge page tracking data. /
9223372036854775807 is the highest possible LSN which purges all page tracking files.*/
SELECT mysqlbackup_page_track_set(true);
```

## Known issue

If the index is built in place using an exclusive algorithm and then is
added to a table after the last LSN checkpoint, you may generate a bad
incremental backup using page tracking. For more details
see [PS-8032 :octicons-link-external-16:](https://perconadev.atlassian.net/browse/PS-8032).

## Uninstall the mysqlbackup component

To uninstall the mysqlbackup component, use the following statement:

```sql
UNINSTALL COMPONENT "file://component_mysqlbackup"
```
