# Backup example

This example demonstrates how to set up daily full backups and hourly incremental backups using Percona XtraBackup {{vers}} with a MySQL {{vers}}-compatible database server.

## Assumptions

* Percona XtraBackup {{vers}} is installed on your system.
* A MySQL {{vers}}-compatible database server (for example, Percona Server for MySQL {{vers}}) is running.
* You have created dedicated directories for storing backups and the backup user can write to them:
  * `/backups/mysql/full` — for daily full backups
  * `/backups/mysql/incr` — for hourly incremental backups

!!! warning "Credentials and security"
    Using `--password` on the command line exposes the password in process lists (for example, `ps`). For production, use a [configuration file](configure-xtrabackup.md) or a login path (for example, `--login-path`) instead of passing the password on the command line.

## Daily full backup script

The following script defines the server details such as hostname, username, password, data directory, and backup directory. Replace these with your actual values. The script:

* Defines the server credentials
* Generates a timestamp with the `date` command for the full backup filename
* Uses `xtrabackup` with the `--backup` option for a full backup
* Specifies the directory to store the backup with `--target-dir`
* Uses `--datadir` to point to the location of your MySQL data files
* Provides the credentials with `--user` and `--password` to access the database server
* Creates the target directory if it does not exist
* Runs the backup and reports success or failure based on the exit code

The script does not verify that the backup completed successfully; consider checking the exit code of `xtrabackup` and only then echoing success or writing to logs.

```bash
#!/bin/bash
# Set server details (replace with your actual values)
SERVER_HOST="your_server_hostname"
SERVER_USER="your_db_username"
SERVER_PASSWORD="your_db_password"
DATA_DIR="/var/lib/mysql"          # Replace with your data directory path
BACKUP_DIR="/backups/mysql/full"

# Get current date for filename
TODAY=$(date +%Y-%m-%d)
FULL_BACKUP_FILENAME="${BACKUP_DIR}/${TODAY}"

# Ensure target directory exists
mkdir -p "${FULL_BACKUP_FILENAME}"

# Run xtrabackup with full backup command
if xtrabackup --backup \
  --target-dir="${FULL_BACKUP_FILENAME}" \
  --datadir="${DATA_DIR}" \
  --user="${SERVER_USER}" \
  --password="${SERVER_PASSWORD}"; then
  echo "Daily full backup completed at $(date)"
else
  echo "Daily full backup FAILED at $(date)" >&2
  exit 1
fi
```

## Running the daily script

You can schedule this script to run automatically using cron. For example, to run it every day at midnight (00:00), add this line to your crontab:

```bash
0 0 * * * /path/to/daily_full_backup.sh
```

## Hourly incremental backup script

This script uses the same server details as the daily script. It retrieves the current date and hour for the incremental backup filename. The core command uses `xtrabackup` with the `--backup` and `--incremental` options for an incremental backup. `--target-dir` specifies the directory to store the incremental backup. `--incremental-basedir` must point to the base directory of a completed full or incremental backup. This example uses the **most recent** full backup as the base: `ls -t` lists full backups by modification time (newest first), and `head -n 1` selects that newest directory. The script checks that the base directory exists before running and reports success or failure based on the exit code.

```bash
#!/bin/bash
# Set server details (same as daily script)
SERVER_HOST="your_server_hostname"
SERVER_USER="your_db_username"
SERVER_PASSWORD="your_db_password"
DATA_DIR="/var/lib/mysql"          # Replace with your data directory path
BACKUP_DIR="/backups/mysql/incr"

# Get current date and hour for filename
TODAY=$(date +%Y-%m-%d)
HOUR=$(date +%H)                  # Get current hour (00-23)
INCR_BACKUP_FILENAME="${BACKUP_DIR}/${TODAY}_${HOUR}"

# Set the base directory to the most recent full backup (newest first: ls -t, then head -n 1)
LATEST_FULL=$(ls -t /backups/mysql/full 2>/dev/null | head -n 1)
if [ -z "${LATEST_FULL}" ]; then
  echo "No full backup found; cannot take incremental backup" >&2
  exit 1
fi
BASE_DIR="/backups/mysql/full/${LATEST_FULL}"

# Ensure target directory exists
mkdir -p "${INCR_BACKUP_FILENAME}"

# Run xtrabackup with incremental backup command
if xtrabackup --backup \
  --incremental \
  --target-dir="${INCR_BACKUP_FILENAME}" \
  --incremental-basedir="${BASE_DIR}" \
  --user="${SERVER_USER}" \
  --password="${SERVER_PASSWORD}"; then
  echo "Hourly incremental backup completed at $(date)"
else
  echo "Hourly incremental backup FAILED at $(date)" >&2
  exit 1
fi
```

!!! note "Incremental base directory"
    For a chain of incremental backups, you can set the base to the most recent incremental backup directory instead of the full backup, so each incremental is based on the previous one. The example above bases each hourly backup on the latest full backup for simplicity.

!!! important "Schedule so the full backup completes before incrementals"
    Each incremental must be based on a **completed** full or incremental backup. If the daily full runs at midnight and can take more than an hour, the 01:00 incremental might still see "latest full" as yesterday's backup, and the 02:00 incremental might see today's. That produces two different chains. Ensure the full backup finishes before the first incremental that depends on it: for example, run the full at 00:00 and start incrementals at 02:00, or use a wrapper that runs the first incremental only after the full has completed.

## Running the hourly script

Schedule this script to run every hour using cron:

```bash
0 * * * * /path/to/hourly_incremental_backup.sh
```

## Restore chain

To restore from a full backup and its incrementals you must:

1. **Prepare the full backup** once (apply redo only, no incremental yet).
2. **Apply each incremental in order** (oldest to newest) to the same target directory.
3. **Prepare again** (apply redo and undo) so the backup is consistent.

All incrementals that you apply must form a single chain from one full backup: each incremental is based on the previous one or on the full. Do not mix incrementals from different full backups in one restore. For step-by-step commands, see [Prepare a full backup](prepare-full-backup.md), [Prepare an incremental backup](prepare-incremental-backup.md), and [Restore full and incremental backups](restore-a-backup.md).

## Next steps

* [Prepare a full backup](prepare-full-backup.md) and [prepare an incremental backup](prepare-incremental-backup.md) before restore.
* [Restore full and incremental backups](restore-a-backup.md) when you need to recover data.
