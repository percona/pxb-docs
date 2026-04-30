# InnoDB B-tree validation during prepare

The [`--check-tables`](./xtrabackup-option-reference.md#check-tables) option adds a structural validation step to the `--prepare` phase of Percona XtraBackup 8.4. It verifies the integrity of InnoDB B-tree indexes in a backup by detecting structural inconsistencies that are not covered by page-level checksums.

Page checksums ensure that individual pages are not corrupted at the byte level. However, they do not verify whether those pages form a valid B-tree structure. As a result, structurally corrupted indexes can still pass checksum validation.

`--check-tables` runs `btr_validate_index()` on every committed index in every `.ibd` tablespace. It detects issues such as broken sibling pointers, incorrect `PAGE_INDEX_ID` values, missing or incorrect min-record flags, parent-child pointer mismatches, all-zero pages, and inconsistent external LOB page references.

The validation runs entirely during the `--prepare` phase, operates in read-only mode, and does not modify backup data. It can be executed in parallel using `--parallel` and integrates with `--apply-log-only` and `--export` workflows.

By moving structural validation into the backup preparation stage, `--check-tables` allows corruption to be detected before a backup is promoted for production use.

--------------------------------------------------------------------------------------------------------------

# InnoDB B-tree integrity validation during prepare

Percona XtraBackup 8.4 introduces `--check-tables`, a new feature for the `--prepare` phase that validates InnoDB B-tree structures. Unlike standard checksums, this tool detects deep structural corruption—like broken links or mismatched pointers—without impacting the production database. By shifting discovery to the preparation stage, it prevents operators from deploying corrupted backups.

## Backup and Prepare: A Quick Refresher

Percona XtraBackup (PXB) is a hot, non-blocking backup tool for MySQL. A full backup proceeds in two logical phases.

### Phase 1 — `--backup`

PXB copies InnoDB data files while the server keeps running. Because the server continues writing during the copy, PXB also streams the redo log generated during the backup window. The result is a snapshot of data files plus redo entries that bring them forward to a consistent point.

By itself, this snapshot is not immediately restorable: pages may reflect partially applied changes, and the backup represents a mixture of committed and in-flight transactions.

### Phase 2 — `--prepare`

PXB replays the captured redo log against the copied data files. This is equivalent to InnoDB crash recovery:

- Redo is applied to bring pages forward
- Uncommitted transactions are rolled back (if needed)

After prepare, the backup becomes crash-consistent and can be safely restored.

A useful mental model: the backup is a photograph plus a journal; prepare replays the journal to make the photograph coherent.

## The Problem: Why Checksums Are Not Enough

PXB already verifies page checksums during `--backup`. These checks detect physical corruption such as torn pages or bit-level damage.

However, a page checksum only answers whether a page is intact at the byte level. It does not validate whether the **B-tree structure formed by those pages is correct**.

As a result, structural corruption can pass checksum validation, including:

- Broken sibling links in B-tree pages
- Incorrect `PAGE_INDEX_ID` assignments
- Missing or misplaced minimum-record flags
- Invalid parent-child pointer relationships
- External LOB pages shared between multiple records
- All-zero pages that still produce valid checksums

These issues produce backups that are internally consistent at the byte level but logically corrupted at the index level.

Worse, redo application during `--prepare` faithfully preserves any pre-existing structural corruption in the source.

## The Solution: `--check-tables`

`--check-tables` extends the `--prepare` phase by validating the structural integrity of every InnoDB B-tree index in the backup.

It runs `btr_validate_index()` over all committed indexes in all tablespaces and detects:

- Broken sibling links
- Incorrect `PAGE_INDEX_ID`
- Missing or incorrect min-record flags
- Parent-child pointer mismatches
- All-zero pages
- Shared or inconsistent external LOB pages

The validation is:

- **Read-only**
- **Parallel (scales with `--parallel`)**
- **Compatible with incremental prepare and export**
- **Non-intrusive to production workloads**

It shifts corruption detection from post-deployment validation to the backup preparation stage.

## Output

A successful run ends with:


## Benefits

The `--check-tables` option provides the following benefits:

* Detects structural index corruption that is not visible to page checksum validation
* Validates B-tree consistency across all InnoDB indexes in the backup
* Runs entirely on backup data with no impact on the production server
* Supports parallel execution using `--parallel` for scalable validation
* Integrates with incremental and export workflows during `--prepare`

## Limitations

* Validation is performed only during the `--prepare` phase
* Increased CPU and I/O usage on the backup host during validation
* Runtime depends on number of tablespaces and indexes in the backup
* Does not replace logical validation tools such as `CHECK TABLE` on a live server

## How it works

During `--prepare`, after redo log application completes, XtraBackup performs structural validation of InnoDB indexes.

For each tablespace:

1. Loads index metadata from the backup
2. Iterates through all committed indexes
3. Executes `btr_validate_index()` on each index tree
4. Validates structural relationships between pages and records
5. Reports any detected inconsistencies

The validation is read-only and does not modify pages or metadata in the backup.

## Parallel execution

Validation is parallelized using the existing `--parallel` infrastructure in XtraBackup.

Each worker thread processes independent tablespaces:

- Retrieves a tablespace from a shared iterator
- Loads index definitions from SDI data
- Validates each index using `btr_validate_index()`
- Reports errors independently of other threads

Validation is not fail-fast; all workers continue processing to produce a complete report of detected corruption.

## Usage

Final prepare step:

```bash
xtrabackup --prepare --check-tables \
           --target-dir=/backups/full \
           --parallel=8
```

Incremental prepare:

```bash
xtrabackup --prepare --apply-log-only --check-tables \
           --target-dir=/backups/full \
           --incremental-dir=/backups/inc1 \
           --parallel=8
```

## Output

A successful run ends with:

```text
All table checks passed
```

If corruption is detected:

```text
Table check failed. The backup may be corrupted.
```

The process returns a non-zero exit code and logs detailed information about each detected issue.

## Summary

`--check-tables` extends the `--prepare` phase with structural validation of InnoDB B-tree indexes. It complements page checksum verification by detecting inconsistencies in index structure, enabling earlier detection of backup corruption before deployment to production systems.
