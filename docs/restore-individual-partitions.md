# Restore the partition from the backup

Restoring should be done by importing the tables in the partial backup to the
server.

First step is to create new table in which data will be restored.

```{.bash data-prompt="mysql>"}
mysql> CREATE TABLE `name_p4` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`name` text NOT NULL,
`imdb_index` varchar(12) DEFAULT NULL,
`imdb_id` int(11) DEFAULT NULL,
`name_pcode_cf` varchar(5) DEFAULT NULL,
`name_pcode_nf` varchar(5) DEFAULT NULL,
`surname_pcode` varchar(5) DEFAULT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2812744 DEFAULT CHARSET=utf8
```

!!! note
   
    Generate a [.cfg metadata file] by running `FLUSH TABLES ... FOR EXPORT`. The command can only be run on a table, not on the individual table partitions.
    The file is located in the table schema directory and is used for schema verification when importing the tablespace. 

To restore the partition from the backup, the tablespace must be discarded for
that table:

```{.bash data-prompt="mysql>"}
mysql> ALTER TABLE name_p4 DISCARD TABLESPACE;
```

The next step is to copy the `.ibd` file from the backup to the MySQL data directory:

```
cp /mnt/backup/2012-08-28_10-29-09/imdb/name#P#p4.ibd /var/lib/mysql/imdb/name_p4.ibd
```

!!! note
   
    Make sure that the copied files can be accessed by the user running MySQL. 

The last step is to import the tablespace:

```{.bash data-prompt="mysql>"}
mysql> ALTER TABLE name_p4 IMPORT TABLESPACE;
```

[.cfg metadata file]: https://dev.mysql.com/doc/refman/{{vers}}/en/innodb-table-import.html