# Understand version numbers

A version number identifies the product release. The product contains the latest Generally Available (GA) features at the time of that release.

| 8.0.30 | -23 |
|---|---|
| Base version | Minor build version |

Percona uses semantic version numbering, which follows the pattern of base version and build version. Percona assigns unique, non-negative integers in increasing order for each version release. The version number combines the base [MySQL 8.0](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/) version number and the minor build version.

Note that Percona XtraBackup numbering changed after the 8.0.14 version to align Percona XtraBackup versions with Percona Server and MySQL. Find more information in [Aligning Percona XtraBackup Versions with Percona Server for MySQL](https://www.percona.com/blog/2020/08/18/aligning-percona-xtrabackup-versions-with-percona-server-for-mysql/) blog post.

The version numbers for Percona XtraBackup 8.0.30-23 define the following information:

* Base version - the leftmost numbers indicate the [MySQL 8.0](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/) version used as a base. An increase in base version resets the minor build version to 0.  

* Minor build version - an internal number that denotes the version of the software. A build version increases by one each time the Percona XtraBackup is released.

Percona XtraBackup 8.0.28-20 and 8.0.28-21 are multiple releases based on MySQL 8.0.28.


