# Understand version numbers

A version number identifies the innovtion product release. The product contains the latest features, improvements, and bug fixes at the time of that release.

<style>
    table {
        border-collapse: collapse;
        width=100%;
    }
    table td {
        border: 2px solid black;
        padding: 8px;
        text-align: center;
    }
    tr:nth-child(even){
        background-color:#f5f5f5
    }
</style>

| 8.1.0 | -1 |
|---|---|
| Base version | Minor build version |

Percona uses semantic version numbering, which follows the pattern of base version and build version. Percona assigns unique, non-negative integers in increasing order for each version release. The version number combines the base [MySQL {{vers}}](https://dev.mysql.com/doc/relnotes/mysql/{{vers}}/en/) version number and the minor build version.

The version numbers for Percona XtraBackup 8.1.0-1 define the following information:

* Base version - the leftmost numbers indicate the [MySQL {{vers}}](https://dev.mysql.com/doc/relnotes/mysql/{{vers}}/en/) version used as a base. An increase in base version resets the minor build version to 0.  

* Minor build version - an internal number that denotes the version of the software. A build version increases by one each time the Percona XtraBackup is released.




