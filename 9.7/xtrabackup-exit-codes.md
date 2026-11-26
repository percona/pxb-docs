> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-xtrabackup/9.7/llms.txt).

# xtrabackup exit codes

The *xtrabackup* binary exits with the traditional success value of 0 after a backup when no error occurs. Any non-zero exit value means that an error occurred.

The exact non-zero value depends on the error. The command-line option code from the *MySQL* libraries sets some of these values. For example, an unknown command-line option causes an exit code of 255.
