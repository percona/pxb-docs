# Understand version numbers

A version number identifies the innovtion product release. The product contains the latest features, improvements, and bug fixes at the time of that release.

| {{vers}}.0 | -1 |
|---|---|
| Base version | Minor build version |

Percona uses semantic version numbering, which follows the pattern of base version and build version. Percona assigns unique, non-negative integers in increasing order for each version release. The version number combines the base [MySQL {{vers}}](https://dev.mysql.com/doc/relnotes/mysql/{{vers}}/en/) version number and the minor build version.

The version numbers for Percona XtraBackup {{release}} define the following information:

* Base version - the leftmost numbers indicate the [MySQL {{vers}}](https://dev.mysql.com/doc/relnotes/mysql/{{vers}}/en/) version used as a base. An increase in base version resets the minor build version to 0.  

* Minor build version - an internal number that denotes the version of the software. A build version increases by one each time the Percona XtraBackup is released.




