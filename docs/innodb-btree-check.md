# InnoDB B-tree integrity validation during prepare

## Overview

Percona XtraBackup 8.4.0-6 introduces the [`--check-tables`](xtrabackup-option-reference.md#check-tables) option that validates the structural integrity of InnoDB B-tree indexes during the [`--prepare`](xtrabackup-option-reference.md#prepare) phase.

The `--check-tables` option runs `btr_validate_index()` on every committed index in each `.ibd` tablespace and detects structural inconsistencies not covered by page checksum verification.

The validation process:

* Runs during `--prepare`

* Operates in read-only mode

* Does not modify backup contents

* Supports parallel execution through `--parallel`

* Supports workflows that use `--apply-log-only`

* Supports transportable tablespace export with `--export`

Validation during `--prepare` helps detect corrupted indexes before backup restore or production deployment.

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

After applying the redo log during the `--prepare` phase, Percona XtraBackup validates InnoDB index structures in the backup.

The validation process runs in read-only mode against backup files and does not modify backup contents.

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

If the validator detects corruption, validation continues for the remaining indexes and tablespaces to produce a complete report.

## Validation checks

| Check | Detected condition |
|------|---------------------|
| Broken sibling links | Invalid sibling or parent navigation pointers |
| `PAGE_INDEX_ID` mismatches | Page index ID does not match index metadata |
| Minimum-record flag validation | Minimum-record flag is missing or invalid |
| Parent-child pointer validation | Child page boundaries do not match parent node structure |
| External LOB validation | Shared, freed, or out-of-bounds LOB page references |
| All-zero page detection | Page contains only zero bytes |

## Parallel execution

The `--check-tables` option uses the existing `--parallel` infrastructure in Percona XtraBackup. Worker threads process tablespaces independently.

Each worker thread:

1. Retrieves a tablespace from the shared queue

2. Loads metadata for the tablespace

3. Validates committed indexes

4. Reports validation results

## Limitations

The `--check-tables` option has the following limitations:

* Validation runs only during `--prepare`

* Validation increases CPU and I/O usage on the backup host

* Runtime depends on the number of tablespaces and indexes

* Validation does not replace logical consistency checks such as `CHECK TABLE`

## Usage

`--check-tables` is valid only with `--prepare`.

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