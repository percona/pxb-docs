# InnoDB B-tree integrity validation during prepare

## Overview

Percona XtraBackup 8.4.0-6 introduces the [`--check-tables`](xtrabackup-option-reference.md#check-tables) option that validates the structural integrity of InnoDB B-tree indexes during the [`--prepare`](xtrabackup-option-reference.md#prepare) phase. Validation during `--prepare` helps detect corrupted indexes before backup restore or production deployment.

## Why checksum validation is not enough

Percona XtraBackup verifies page checksums during `--backup`. Checksum validation detects physical page corruption, including:

* Torn pages

* Storage bit rot

* Corrupted transfers

* Filesystem-level damage

Checksum validation confirms page integrity at the byte level. B-tree structure validation requires additional checks across related pages.

Structural corruption that can pass checksum validation includes:

* Broken sibling page links

* Incorrect `PAGE_INDEX_ID` assignments

* Missing or misplaced minimum-record flags

* Invalid parent-to-child page references

* Shared external LOB (large object) pages

* All-zero pages with valid checksums

Applying the redo log during `--prepare` copies the existing structural corruption from the source server into the prepared backup. As a result, backups can remain physically consistent while containing logically corrupted indexes.

## How `--check-tables` works

The `--check-tables` option executes `btr_validate_index()` on every committed index in each `.ibd` tablespace using the number of threads specified by [`--parallel`](xtrabackup-option-reference.md#parallel). `--check-tables` detects structural inconsistencies that page checksum verification cannot detect. This option applies only to InnoDB tables.

Validation runs during the `--prepare` phase after applying the redo log. The process operates in read-only mode against backup files and does not modify backup contents. Validation continues even after detecting corrupted tables, allowing all problematic tables and indexes to be reported in a single run.

The option supports:

* [Parallel execution](#parallel-execution) through [`--parallel`](xtrabackup-option-reference.md#parallel)

* Workflows that use [`--apply-log-only`](xtrabackup-option-reference.md#apply-log-only)

* Transportable tablespace export with [`--export`](xtrabackup-option-reference.md#export).

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

This option is functionally equivalent to running `CHECK TABLE` on InnoDB tables, but it executes on the backup during the `--prepare` phase instead of on a running production server.

This allows a significant portion of `CHECK TABLE` workload to be offloaded from production systems to an offline environment where the backup is prepared and validated.

### Detected corruption conditions

| Check | Detected condition |
|------|---------------------|
| Broken sibling links | Invalid sibling or parent navigation pointers |
| `PAGE_INDEX_ID` mismatches | Page index ID does not match index metadata |
| Minimum-record flag validation | Minimum-record flag is missing or invalid |
| Parent-child pointer validation | Child page boundaries do not match parent node structure |
| External LOB validation | Shared, freed, or out-of-bounds LOB page references |
| All-zero page detection | Page contains only zero bytes |

### Parallel execution

The `--check-tables` option uses the existing `--parallel` infrastructure in Percona XtraBackup. Worker threads process tablespaces independently.

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

* Validation does not replace logical consistency checks such as `CHECK TABLE`

## Usage

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
All table checks passed
```

A failed validation operation returns a non-zero exit code and logs the following message:

```text
Table check failed. The backup may be corrupted.
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
