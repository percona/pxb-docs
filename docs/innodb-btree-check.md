# InnoDB B-tree integrity validation during prepare

## Overview

The [`--check-tables`](xtrabackup-option-reference.md#check-tables) option validates the structural integrity of InnoDB B-tree indexes during the [`--prepare`](xtrabackup-option-reference.md#prepare) phase. Validation during `--prepare` helps detect corrupted indexes before restore or production deployment.

## Why checksum validation is not enough

Percona XtraBackup verifies InnoDB page checksums during `--backup`. These checks ensure that the backup contains checksum-valid pages at backup time.

Checksum validation detects physical corruption within individual pages, including:

* Torn-page corruption

* Write corruption

* Transfer corruption

* Storage or filesystem corruption

When the server modifies a page while XtraBackup copies it, XtraBackup retries the copy until the checksum becomes consistent. The retry process prevents partially modified pages from entering the backup.

A successful backup therefore guarantees checksum-valid pages, but checksum validation alone cannot guarantee a fully valid restore.

### Corruption can happen after backup creation

A backup can become corrupted after creation because of storage or filesystem issues.

During `--prepare`, XtraBackup only re-validates pages involved in redo application. Pages outside redo processing may never undergo another checksum check.

For this reason, running `CHECK TABLE` after restore remains a recommended practice. `CHECK TABLE` forces page reads and validates both checksums and structural consistency.

### Checksums do not verify page relationships

Checksum validation only confirms that the bytes within a page match the checksum stored in the page header.

XtraBackup does not validate B-tree structure or relationships between pages during backup. As a result, structurally corrupted pages can still enter the backup if those pages remain checksum-valid on the source server.

Structural corruption rarely occurs and usually results from server bugs, backup tool bugs, storage failures, or filesystem-level corruption.

Structural corruption can break B-tree page relationships, page metadata consistency, and external LOB references. For a complete list of detected corruption conditions, see [Detected corruption conditions](#detected-corruption-conditions).

## How `--check-tables` works

The `--check-tables` option executes `btr_validate_index()` on every index that is present and active in the InnoDB data dictionary for each `.ibd` tablespace, using the number of threads specified by [`--parallel`](xtrabackup-option-reference.md#parallel). `--check-tables` detects structural inconsistencies that page checksum verification cannot detect. The option applies only to InnoDB tables.

In addition to structural validation, when `--check-tables` is used, XtraBackup verifies page checksums during InnoDB B-tree index traversal and performs additional checksum verification of the system tablespace (`ibdata*`) and undo tablespaces (`undo*.ibu`).

Percona XtraBackup runs validation during the `--prepare` phase after applying the redo log. The validation process operates in read-only mode against backup files and does not modify backup contents. Validation continues after detecting corruption so that Percona XtraBackup can report all problematic tables and indexes in a single run.

For each tablespace, Percona XtraBackup:

1. Loads index metadata

2. Identifies committed indexes

3. Executes `btr_validate_index()` on each index

4. Traverses B-tree pages and validates structural relationships

5. Reports detected inconsistencies

The option also works with:

* [Parallel execution](#parallel-execution) through [`--parallel`](xtrabackup-option-reference.md#parallel)

* Workflows that use [`--apply-log-only`](xtrabackup-option-reference.md#apply-log-only)

* Transportable tablespace export with [`--export`](xtrabackup-option-reference.md#export)

### Detected corruption conditions

The validation process performs the following structural checks:

| Check | Detected condition |
|------|---------------------|
| Broken sibling links | Invalid sibling-page or parent-page navigation pointers |
| `PAGE_INDEX_ID` mismatches | Page index ID does not match index metadata |
| Minimum-record flag validation | Minimum-record flag is missing or invalid |
| Parent-child pointer validation | Child page boundaries do not match parent node structure |
| External LOB validation | Shared, freed, or out-of-bounds LOB page references |
| All-zero page detection | Page contains only zero bytes |
| PRIMARY and secondary index record-count validation | Record count mismatch between the PRIMARY index and secondary indexes |

### Offloading `CHECK TABLE`

Similar to the InnoDB `CHECK TABLE` command, the `--check-tables` option validates InnoDB tables. However, Percona XtraBackup performs this validation offline on backup files during the `--prepare` phase, avoiding any performance impact on a live production server.

Validation during `--prepare` moves structural integrity verification from restored database instances to the backup preparation workflow. A backup or staging host can run validation without starting MySQL on the restored backup.

Using `--check-tables` during `--prepare` provides the following operational benefits:

* Eliminates the need to start a MySQL server on restored backups solely for structural validation

* Moves validation workload away from running production systems

* Detects structural corruption earlier in the backup validation workflow

* Detects corruption before restore or deployment

### Parallel execution

The `--check-tables` option uses the existing `--parallel` infrastructure from Percona XtraBackup. Worker threads process tablespaces independently.

Each worker thread:

1. Retrieves a tablespace from the shared queue

2. Loads metadata for the tablespace

3. Validates committed indexes

4. Reports validation results

### Limitations

The `--check-tables` option has the following limitations:

* Validation applies only to InnoDB tables and does not validate MyISAM or RocksDB tables

* Validation runs only during `--prepare`

* Validation increases CPU and I/O usage on the backup host

* Runtime depends on the number of tablespaces and indexes

* For incremental backups, use `--check-tables` only during the final prepare stage because the option verifies all tables and indexes each time it runs

* Checksum corruption may cause XtraBackup to abort with an assertion failure instead of exiting gracefully

## Usage

The `--check-tables` option uses the thread count specified by `--parallel`. Start with `--parallel=8` and adjust the value according to CPU availability and disk I/O capacity on the backup host.

### Validate a full backup

```bash
xtrabackup --prepare --check-tables \
  --target-dir=/backups/full \
  --parallel=8
```

### Validate an incremental backup

The `--check-tables` option can be used together with `--apply-log-only`. However, because validation scans all tables and indexes each time it runs, it's recommended using the option during the final prepare stage of an incremental backup.

```bash
xtrabackup --prepare --check-tables \
  --target-dir=/backups/full \
  --parallel=8
```

### Validate and export tablespaces

```bash
xtrabackup --prepare --export --check-tables \
  --target-dir=/backups/full \
  --parallel=8
```

## Output

A successful validation operation typically ends with a message similar to:

```text
2026-05-15T15:41:57.808327+01:00 2 [Note] [MY-011825] [Xtrabackup] Checking: mysql/replication_group_member_actions
2026-05-15T15:41:57.808630+01:00 2 [Note] [MY-011825] [Xtrabackup] Checking: mysql/replication_group_configuration_version
2026-05-15T15:41:57.808810+01:00 2 [Note] [MY-011825] [Xtrabackup] Checking: mysql/server_cost
2026-05-15T15:41:57.808998+01:00 2 [Note] [MY-011825] [Xtrabackup] Checking: mysql/engine_cost
2026-05-15T15:41:57.809190+01:00 2 [Note] [MY-011825] [Xtrabackup] Checking: mysql/proxies_priv
2026-05-15T15:41:57.809511+01:00 2 [Note] [MY-011825] [Xtrabackup] Checking: mysql/ndb_binlog_index
2026-05-15T15:41:58.051499+01:00 0 [Note] [MY-011825] [Xtrabackup] All table checks passed.
```

A failed validation operation returns a non-zero exit code. During validation, XtraBackup logs each table as it processes it:

```text
2026-05-15T13:42:23.691691+01:00 2 [Note] [MY-011825] [Xtrabackup] Checking: test/t1
2026-05-15T13:42:23.697349+01:00 2 [Note] [MY-011825] [Xtrabackup] Checking: test/t_lob
2026-05-15T13:42:23.782555+01:00 2 [Note] [MY-011825] [Xtrabackup] Checking: mysql/dd_properties
2026-05-15T13:42:23.782835+01:00 2 [Note] [MY-011825] [Xtrabackup] Checking: mysql/innodb_dynamic_metadata
...
```

If validation detects corruption, XtraBackup reports the affected tables and ends with the following summary message:

```text
2026-05-15T13:42:24.670469+01:00 0 [ERROR] [MY-011825] [Xtrabackup] Table check failed. The backup may be corrupted.
```

The log contains detailed information for each detected inconsistency.

### Corruption examples

1. Sibling page relationships corruption.

    ??? example "Expected output"

        ```{.text .no-copy}
        2026-05-15T13:42:20.270268+01:00 2 [ERROR] [MY-013051] [InnoDB]
        In pages [page id: space=2, page number=5]
        and [page id: space=2, page number=6]
        of index PRIMARY of table test.t1

        InnoDB: broken FIL_PAGE_NEXT or FIL_PAGE_PREV links
        ```

2. Parent-to-child page references corruption.

    ??? example "Expected output"

        ```{.text .no-copy}
        2026-05-15T13:38:12.343921+01:00 2 [ERROR] [MY-011825] [InnoDB]
        B-tree corruption: page 0 is empty but is not the root page
        in index PRIMARY. Possible all-zero (unflushed) page.
        ```

3. Page ownership metadata corruption.

    ??? example "Expected output"

        ```{.text .no-copy}
        2026-05-15T13:38:12.343894+01:00 2 [ERROR] [MY-011866] [InnoDB]
        Page index id 0 != data dictionary index id 204
        ```

4. Minimum-record markers corruption.

    ??? example "Expected output"

        ```{.text .no-copy}
        2026-05-15T13:42:27.237530+01:00 2 [ERROR] [MY-014011] [InnoDB]
        Minimum record flag is wrongly set to rec on page '4'
        at level '0' for index 'PRIMARY' of table 'sys/sys_config'.
        ```

5. External LOB page ownership corruption.

    ??? example "Expected output"

        ```{.text .no-copy}
        2026-05-15T13:42:34.475996+01:00 2 [ERROR] [MY-011825] [InnoDB] Invalid record! External LOB first page cannot be shared between two records
        2026-05-15T13:42:34.476009+01:00 2 [ERROR] [MY-011825] [InnoDB] The external LOB first page is [page id: space=4294967294, page number=1002]
        2026-05-15T13:42:34.476014+01:00 2 [ERROR] [MY-011825] [InnoDB] The first occurrence of the external LOB first page is in record : page_no: 992 with heap_no: 4
        ```