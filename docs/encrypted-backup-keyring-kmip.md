# Encrypted tablespaces backup with keyring KMIP 

Percona XtraBackup 8.0.27-19 adds support for the Key Management
Interoperability Protocol (KMIP) which enables the communication between
the key management system and encrypted database server.

Percona XtraBackup has no special requirements for backing up a database
that contains encrypted InnoDB tablespaces.

Percona XtraBackup performs the following actions:

1. Connects to the MySQL server

2. Pulls the configuration

3. Connects to the KMIP server

4. Fetches the necessary keys from the KMIP server

5. Stores the KMIP server configuration settings in  the `xtrabackup_component_keyring_kmip.cnf` file in the backup directory

When preparing the backup, Percona XtraBackup connects to the KMIP server
with the settings from the `xtrabackup_component_keyring_kmip.cnf` file.

## Backup

```
xtrabackup --backup --target-dir=/backup/ --user=root --password="pwd"  
```

## Prepare

```
xtrabackup --prepare --target-dir=/backup/  
```

## Copy-back

