> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-xtrabackup/8.4/llms.txt).

# Take an incremental backup using page tracking

To create an incremental backup with page tracking, Percona XtraBackup uses the MySQL `mysqlbackup` component. This component provides a list of pages modified since the last backup. Percona XtraBackup copies only those pages. This operation removes the need to scan the pages in the database.

Page tracking can improve the speed of incremental backups. The speed depends on the number of read requests, not on the number of changed pages. For the effect of scattered changed pages, see [Reduce read requests for scattered changed pages](#reduce-read-requests-for-scattered-changed-pages).

Run the following commands as root or use the `sudo` command.

## Version changes

Percona XtraBackup 8.4.0-8 renames the `--incremental-basedir` option to [`--backup-incremental-base`](https://docs.percona.com/percona-xtrabackup/8.4/xtrabackup-option-reference.html#backup-incremental-base). Percona XtraBackup still accepts `--incremental-basedir`. Percona XtraBackup prints a deprecation warning when you use it. A future release removes `--incremental-basedir`, so update your scripts to use `--backup-incremental-base`.

If you pass both options in the same command, Percona XtraBackup reports an error. Percona XtraBackup does not start the backup.

## Install the component

To use page tracking, do the following:

1. Install the `mysqlbackup` component and enable it on the server:

   ```
   INSTALL COMPONENT "file://component_mysqlbackup";
   ```

1. Check whether the `mysqlbackup` component is installed successfully:

   ```
   SELECT COUNT(1) FROM mysql.component
   WHERE component_urn='file://component_mysqlbackup';
   ```

## Start page tracking manually

After the `mysqlbackup` component is active on the server, start page tracking with the following statement:

```
SELECT mysqlbackup_page_track_set(true);
```

Start page tracking before you take the first backup. This avoids a delay in the first full backup that uses page tracking. Without this statement, Percona XtraBackup can pause during that backup. The following is an example of the message:

Expected output

```
xtrabackup: pagetracking: Sleeping for 1 second, waiting for checkpoint lsn 17852922 /
to reach to page tracking start lsn 21353759
```

Early activation ensures that the page tracking log sequence number (LSN) is higher than the server checkpoint LSN.

## Check the LSN value

Check the LSN where page tracking starts to track changed pages with the following statement:

```
SELECT mysqlbackup_page_track_get_start_lsn();
```

## Use page tracking

Enable page tracking for full and incremental backups with the `--page-tracking` option.

The option has the following benefits:

- Resets page tracking to the start of the backup. This reset allows the next incremental backup to use page tracking.
- Allows an incremental backup to use page tracking if tracking data exists from the checkpoint LSN at backup start.

Memory requirements

Percona XtraBackup processes a list of all the tracked pages in memory. If Percona XtraBackup does not have enough memory for this list, the process throws an error and exits. For example, an incremental backup of 200 GB can need an additional 100 MB of memory. The memory holds the page tracking data.

The following examples create full and incremental backups with the `--page-tracking` option:

**Full backup**

```
xtrabackup --backup --target-dir=$FULL_BACK --page-tracking
```

**Incremental backup**

**8.4.0-8 and later**

```
xtrabackup --backup --target-dir=$INC_BACKUP \
--backup-incremental-base=$FULL_BACKUP --page-tracking
```

**Earlier than 8.4.0-8**

```
xtrabackup --backup --target-dir=$INC_BACKUP \
--incremental-basedir=$FULL_BACKUP --page-tracking
```

After you enable page tracking, the next incremental backup finds changed pages with page tracking.

Known issue

You may generate a bad incremental backup that uses page tracking. The issue occurs when you build an index in place with an exclusive algorithm. The issue requires that you add the index to a table after the last LSN checkpoint. For details, see [PS-8032](https://perconadev.atlassian.net/browse/PS-8032) .

## Reduce read requests for scattered changed pages

During an incremental backup with page tracking, Percona XtraBackup reads only the pages that the server reports as changed. Percona XtraBackup reads consecutive changed pages together. Percona XtraBackup reads each scattered changed page on its own.

Thousands of small reads take far longer than a few large reads. An incremental backup of a large tablespace can be slow even when little data changes.

### Merge reads across gaps

Starting with Percona XtraBackup 8.4.0-7, the [`--page-tracking-merge-gap`](https://docs.percona.com/percona-xtrabackup/8.4/xtrabackup-option-reference.html#page-tracking-merge-gap) option lets Percona XtraBackup merge reads.

When two changed pages are close, a read across the unchanged pages between them costs less than another read. Percona XtraBackup merges these reads automatically. Percona XtraBackup discards the extra pages when it writes the delta. The backup contents and size stay the same. Only the read pattern changes.

With `auto`, Percona XtraBackup measures the storage once at the start of the backup. The measurement covers the time of one read request and the speed of sequential reads. From this measurement, Percona XtraBackup chooses the largest gap of unchanged pages that costs less to read than another request. The gap can differ for each tablespace. The gap depends on the tablespace page size.

The `--page-tracking-merge-gap` option accepts the following values:

- `auto` (default): Omit the option, or set `--page-tracking-merge-gap=auto`. Percona XtraBackup measures the storage and selects the gap.
- A page count, for example `8`: Percona XtraBackup reads changed pages in one request when up to eight unchanged pages separate them. Percona XtraBackup skips the measurement. For compressed tablespaces, Percona XtraBackup scales the count to the physical page size. The byte limit stays the same. A fixed value does not adapt to the storage. A fixed value can read far more data than necessary. A fixed value can also split the reads into too many small requests. Both cases slow the backup. Check the value again after a hardware change.
- `0`: Turns off the feature. Percona XtraBackup reads together only strictly consecutive changed pages, as in releases before 8.4.0-7.

Use the `auto` default. Benchmark your own workload before you set a fixed value. Set a fixed value only if `auto` does not give the best result.

To set a fixed gap, add the option to the incremental backup command:

**8.4.0-8 and later**

```
xtrabackup --backup --target-dir=/data/inc1 \
  --backup-incremental-base=/data/full \
  --page-tracking --page-tracking-merge-gap=8
```

**Earlier than 8.4.0-8**

```
xtrabackup --backup --target-dir=/data/inc1 \
  --incremental-basedir=/data/full \
  --page-tracking --page-tracking-merge-gap=8
```

Merged reads can increase billed reads

A merged read retrieves more bytes than the changed pages alone. Consider this effect if your storage provider charges for reads or limits read throughput. To avoid the extra reads, set the option to `0`.

### Check the read statistics

The backup log reports the storage measurement once. For each tablespace with at least 1000 changed pages, the backup log reports the following values:

- Number of changed pages
- Number of reads before the merge
- Number of reads after the merge
- Resulting read amplification

If the typical gap in a table costs too much to merge, the backup log reports the gap. The backup log also suggests a value to set. Check these log lines when you compare a fixed value with `auto`.

## Stop page tracking

To stop page tracking, run the following statement:

```
SELECT mysqlbackup_page_track_set(false);
```

## Purge page tracking data

Page tracking creates a file in the `datadir` of the server to collect data about changed pages. The file grows until you stop page tracking. If you stop and restart the server, page tracking creates another file. Page tracking also keeps the old file. The old file grows until you stop page tracking explicitly.

Create a full backup after you purge the page tracking data. To purge the page tracking data, run the following statements:

```
SELECT mysqlbackup_page_track_set(false);
SELECT mysqlbackup_page_track_purge_up_to(9223372036854775807);
/* Specify the LSN up to which you want to purge page tracking data.
9223372036854775807 is the highest possible LSN which purges all page
tracking files. */
SELECT mysqlbackup_page_track_set(true);
```

## Uninstall the `mysqlbackup` component

To uninstall the `mysqlbackup` component, run the following statement:

```
UNINSTALL COMPONENT "file://component_mysqlbackup";
```
