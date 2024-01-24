# The xtrabackup binary overview

The *xtrabackup* binary is a compiled C program that is linked with the *InnoDB*
libraries and the standard *MySQL* client libraries.

For details on the xtrabackup command-line options, see [xtrabackup command-line options].

*xtrabackup* enables point-in-time backups of *InnoDB* / *XtraDB* tables
together with the schema definitions, *MyISAM* tables, and other portions of the
server.

The *InnoDB* libraries provide the functionality to apply a log to data
files. The *MySQL* client libraries are used to parse command-line options and
configuration file.

The tool runs in either `--backup` or `--prepare` mode,
corresponding to the two main functions it performs. There are several
variations on these functions to accomplish different tasks, and there are two
less commonly used modes, `--stats` and `--print-param`.

[xtrabackup command-line options]: xtrabackup-option-reference.md

