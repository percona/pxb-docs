# How-tos and recipes

## Recipes for xtrabackup


* [Making a Full Backup](backup_scenarios/full_backup.md)


* [Making an Incremental Backup](backup_scenarios/incremental_backup.md)


* [Make a Streaming Backup](howtos/recipes_xbk_stream.md)

* [Making a Compressed Backup](backup_scenarios/compressed_backup.md)


* [Backing Up and Restoring Individual Partitions](howtos/recipes_xbk_partition.md)


## How-tos


* [Privileges and Permissions for Users](howtos/permissions.md)


* [How to set up a replica for replication in 6 simple steps with Percona XtraBackup](howtos/setting_up_replication.md)


* [Verifying Backups with replication and pt-checksum](howtos/backup_verification.md)


* [How to create a new (or repair a broken) GTID-based Replica](howtos/recipes_ibkx_gtid.md)


## Assumptions in this section

Most of the time, the context will make the recipe or tutorial understandable.
To assure that, a list of the assumptions, names and “things” that will appear
in this section is given. At the beginning of each recipe or tutorial they will
be specified in order to make it quicker and more practical.

`HOST`

A system with a *MySQL*-based server installed, configured and running. We
will assume the following about this system:

* the MySQL server is able to communicate with others by the
standard TCP/IP port;

* an SSH server is installed and configured - see here if it is not;

* you have a user account in the system with the appropriate
permissions and

* you have a MySQL’s user account with appropriate Connection and Privileges Needed.

`USER`

An user account in the system with shell access and appropriate permissions
for the task. A guide for checking them is here.

`DB-USER`

An user account in the database server with appropriate privileges for the
task. A guide for checking them is here.
