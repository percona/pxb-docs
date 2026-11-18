> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-xtrabackup/8.4/llms.txt).

# Use the xbcloud binary with Google Cloud Storage

## Create a full backup with Google Cloud Storage

The support for Google Cloud Storage is implemented using the interoperability mode. This mode was especially designed to interact with cloud services compatible with Amazon S3.

See also

[Cloud Storage Interoperability](https://cloud.google.com/storage/docs/interoperability)

```
xtrabackup --backup --stream=xbstream --extra-lsndir=/tmp --target-dir=/tmp | \
xbcloud put --storage=google \
--google-endpoint=`storage.googleapis.com` \
--google-access-key='YOUR-ACCESSKEYID' \
--google-secret-key='YOUR-SECRETACCESSKEY' \
--google-bucket='mysql_backups'
--parallel=10 \
$(date -I)-full_backup
```

The following options are available when using Google Cloud Storage:

- –google-access-key =
- –google-secret-key =
- –google-bucket =
- –google-storage-class=name

Note

The Google storage class name options are the following:

- STANDARD
- NEARLINE
- COLDLINE
- ARCHIVE

See also

[Google storage classes - the default Google storage class depends on the storage class of the bucket](https://cloud.google.com/storage/docs/changing-default-storage-class)
