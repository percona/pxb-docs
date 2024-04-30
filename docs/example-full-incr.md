# Backup example

This example demonstrates how a beginner DBA can set up daily full backups and hourly incremental backups for a large organization using Percona XtraBackup 8.0 with a Percona Server for MySQL 8.0 database server.

## Assumptions

* You have Percona XtraBackup 8.0 installed on your system.
* You have a Percona Server for MySQL 8.0 database server running.
* You have created dedicated directories for storing backups:
    * `/backups/mysql/full` - for daily full backups
    * `/backups/mysql/incr` - for hourly incremental backups

## Daily Full Backup Script

This following script defines the server details like hostname, username, password, data directory, and backup directory. Replace these with your actual values.

* Defines the server credentials

* Generates a timestamp with the `date` command for the full backup filename

* Uses `xtrabackup` with the `--backup` flag for a full backup

* Specifies the directory to store the backup with `--target-dir`

* `--datadir` points to the location of your MySQL data files.

* Provides the credentials with `--user` and `--password` to access the database server.

* Echoes a message confirming the successful backup completion.


```bash
#!/bin/bash

# Set server details (replace with your actual values)
SERVER_HOST="your_server_hostname"
SERVER_USER="your_db_username"
SERVER_PASSWORD="your_db_password"
DATA_DIR="/var/lib/mysql"  # Replace with your data directory path
BACKUP_DIR="/backups/mysql/full"

# Get current date for filename
TODAY=$(date +%Y-%m-%d)
FULL_BACKUP_FILENAME="${BACKUP_DIR}/${TODAY}"

# Run xtrabackup with full backup command
xtrabackup --backup \
  --target-dir="${FULL_BACKUP_FILENAME}" \
  --datadir="${DATA_DIR}" \
  --user="${SERVER_USER}" \
  --password="${SERVER_PASSWORD}"

echo "Daily full backup completed at $(date)"
```

## Running the Daily Script

You can schedule this script to run automatically using cron. For example, to run it every day at midnight (00:00), add this line to your crontab:

```{.bash data-prompt="$"}
$ 0 0 * * * /path/to/daily_full_backup.sh
```

## Hourly Incremental Backup Script

This script uses the same server details as the daily script. It retrieves the current date and hour for the incremental backup filename. The core command uses `xtrabackup` with the `--backup` and `--incremental` flags for an incremental backup. `--target-dir` specifies the directory to store the incremental backup. `--base-dir` points to the latest full backup directory obtained using `ls` and `tail` commands. This ensures the incremental backup references the most recent full backup. Similar to the daily script, it echoes a confirmation message.


```bash
#!/bin/bash

# Set server details (same as daily script)
SERVER_HOST="your_server_hostname"
SERVER_USER="your_db_username"
SERVER_PASSWORD="your_db_password"
DATA_DIR="/var/lib/mysql"  # Replace with your data directory path
BACKUP_DIR="/backups/mysql/incr"

# Get current date and hour for filename
TODAY=$(date +%Y-%m-%d)
HOUR=$(date +%H)  # Get current hour (00-23)
INCR_BACKUP_FILENAME="${BACKUP_DIR}/${TODAY}_${HOUR}"

# Set the base directory for incremental backups (point to the latest full backup)
BASE_DIR="/backups/mysql/full/$(ls -tr /backups/mysql/full | tail -n 1)"

# Run xtrabackup with incremental backup command
xtrabackup --backup \
  --incremental \
  --target-dir="${INCR_BACKUP_FILENAME}" \
  --base-dir="${BASE_DIR}" \
  --user="${SERVER_USER}" \
  --password="${SERVER_PASSWORD}"

echo "Hourly incremental backup completed at $(date)"
```

## Run the Hourly Script

Schedule this script to run every hour using cron.

```{.bash data-prompt="$"}
$ 0 * * * * /path/to/your/script.sh
```