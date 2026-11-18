> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-xtrabackup/8.4/llms.txt).

# xtrabackup exit codes

The *xtrabackup* binary exits with the traditional success value of 0 after a backup when no error occurs. If an error occurs during the backup, the exit value is 1.

In certain cases, the exit value can be something other than 0 or 1, due to the command-line option code included from the *MySQL* libraries. An unknown command-line option, for example, will cause an exit code of 255.
