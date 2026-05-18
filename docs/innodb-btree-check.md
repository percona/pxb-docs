# InnoDB B-tree integrity validation during prepare

## Overview

Percona XtraBackup 8.4.0-6 introduces the [`--check-tables`](xtrabackup-option-reference.md#check-tables) option that validates the structural integrity of InnoDB B-tree indexes during the [`--prepare`](xtrabackup-option-reference.md#prepare) phase. Validation during `--prepare` helps detect corrupted indexes before restore or production deployment.

## Why checksum validation is not enough

Percona XtraBackup verifies InnoDB page checksums during `--backup`. These checks ensure that the backup contains checksum-valid pages at backup time.

Checksum validation detects physical corruption within individual pages, including:

* Torn pages

* Corrupted writes

* Transfer corruption

* Some storage or filesystem-level corruption

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

Structural corruption can include:

* Broken sibling page links

* Incorrect `PAGE_INDEX_ID` assignments

* Missing or misplaced minimum-record flags

* Invalid parent-to-child page references

* Shared external LOB (large object) pages

* All-zero pages with valid checksums

## How `--check-tables` works

The `--check-tables` option executes `btr_validate_index()` on every committed index in each `.ibd` tablespace using the number of threads specified by [`--parallel`](xtrabackup-option-reference.md#parallel). `--check-tables` detects structural inconsistencies that page checksum verification cannot detect. The option applies only to InnoDB tables.

Percona XtraBackup runs validation during the `--prepare` phase after applying the redo log. The validation process operates in read-only mode against backup files and does not modify backup contents. Validation continues after detecting corruption so that Percona XtraBackup can report all problematic tables and indexes in a single run.

The option supports:

* [Parallel execution](#parallel-execution) through [`--parallel`](xtrabackup-option-reference.md#parallel)

* Workflows that use [`--apply-log-only`](xtrabackup-option-reference.md#apply-log-only)

* Transportable tablespace export with [`--export`](xtrabackup-option-reference.md#export)

For each tablespace, Percona XtraBackup:

1. Loads index metadata

2. Identifies committed indexes

3. Executes `btr_validate_index()` on each index

4. Traverses B-tree pages and validates structural relationships

5. Reports detected inconsistencies

The validation process verifies:

* Sibling page relationships

* Parent-to-child page references

* Page ownership metadata

* Minimum-record markers

* External LOB (large object) page ownership

### Offloading `CHECK TABLE`

The `--check-tables` option provides functionality similar to `CHECK TABLE` for InnoDB tables, but Percona XtraBackup performs validation on backup files during the `--prepare` phase instead of on a running production server.

Validation during `--prepare` moves structural integrity verification from restored database instances to the backup preparation workflow. A backup or staging host can run validation without starting MySQL on the restored backup.

Using `--check-tables` during `--prepare` provides the following operational benefits:

* Eliminates the need to start a MySQL server on restored backups solely for structural validation

* Moves validation workload away from running production systems

* Detects structural corruption earlier in the backup validation workflow

* Detects corruption before restore or deployment

### Detected corruption conditions

| Check | Detected condition |
|------|---------------------|
| Broken sibling links | Invalid sibling-page or parent-page navigation pointers |
| `PAGE_INDEX_ID` mismatches | Page index ID does not match index metadata |
| Minimum-record flag validation | Minimum-record flag is missing or invalid |
| Parent-child pointer validation | Child page boundaries do not match parent node structure |
| External LOB validation | Shared, freed, or out-of-bounds LOB page references |
| All-zero page detection | Page contains only zero bytes |

### Parallel execution

The `--check-tables` option uses the existing `--parallel` infrastructure from Percona XtraBackup. Worker threads process tablespaces independently.

Each worker thread:

1. Retrieves a tablespace from the shared queue

2. Loads metadata for the tablespace

3. Validates committed indexes

4. Reports validation results

### Limitations

The `--check-tables` option has the following limitations:

* Validation runs only during `--prepare`

* Validation increases CPU and I/O usage on the backup host

* Runtime depends on the number of tablespaces and indexes

* For incremental backup chains, run `--check-tables` only during the final prepare stage because the option verifies all tables and indexes each time it runs

* Validation does not replace logical consistency checks such as `CHECK TABLE`

## Usage

The `--check-tables` option uses the thread count specified by `--parallel`. Start with `--parallel=8` and tune the value according to available CPU and disk I/O capacity on the backup host.

### Validate a full backup

```bash
xtrabackup --prepare --check-tables \
  --target-dir=/backups/full \
  --parallel=8
```

### Validate an incremental backup chain

```bash
xtrabackup --prepare --apply-log-only --check-tables \
  --target-dir=/backups/full \
  --incremental-dir=/backups/inc1 \
  --parallel=8
```

### Validate and export tablespaces

```bash
xtrabackup --prepare --export --check-tables \
  --target-dir=/backups/full \
  --parallel=8
```

## Output

A successful validation operation ends with:

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
