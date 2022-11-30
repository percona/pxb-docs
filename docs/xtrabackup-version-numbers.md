# Understand version numbers

A version number identifies the product release. The product contains the latest Generally Available (GA) features at the time of that release. 

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

| 2.4 | 26 |
|---|---|
| Base version | Minor build version|

Percona uses semantic version numbering, which follows the pattern of base version and minor build. Percona assigns unique, non-negative integers in increasing order for each minor build release. The version number combines the base Percona XtraBackup version number and the minor build version.

Percona does not release a new version of Percona XtraBackup 2.4 for every release of MySQL 5.7. Percona XtraBackup 2.4 is compatible with newer versions of MySQL 5.7. 

The version numbers for Percona XtraBackup 2.4.26 define the following information:

* Base version - the leftmost number indicates the version of the Percona XtraBackup that is based on [MySQL 5.7](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/). An increase in base version resets the minor build version to 0.  

* Minor build version - an internal number that denotes the version of the software. A build version increases by one each time the Percona XtraBackup is released.

