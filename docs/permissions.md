# Permissions needed

We will be referring to *permissions* to the ability of a user to access
and perform changes on the relevant parts of the host’s filesystem,
starting/stopping services and installing software.

By *privileges*, we refer to the abilities of a database user to perform
different kinds of actions on the database server.

There are many ways for checking the permission on a file or directory. For
example, `ls -ls /path/to/file` or `stat /path/to/file | grep Access` will
do the job:

```{.bash data-prompt="$"}
$ stat /etc/mysql | grep Access
``` 
The result could look like this:

??? example "Expected output"

    ```{.text .no-copy}
    Access: (0755/drwxr-xr-x)  Uid: (    0/    root)   Gid: (    0/    root)
    Access: 2011-05-12 21:19:07.129850437 -0300
    $ ls -ld /etc/mysql/my.cnf
    -rw-r--r-- 1 root root 4703 Apr  5 06:26 /etc/mysql/my.cnf
    ```

As in this example, `my.cnf` is owned by `root` and not writable for anyone
else. Assuming that you do not have `root`‘s password, you can check what
permissions you have on these types of files with `sudo -l`:

```{.bash data-prompt="$"}
$ sudo -l
```
The results could look like this:

??? example "Expected output"

    ```{.text .no-copy}
    Password:
    You may run the following commands on this host:
    (root) /usr/bin/
    (root) NOPASSWD: /etc/init.d/mysqld
    (root) NOPASSWD: /bin/vi /etc/mysql/my.cnf
    (root) NOPASSWD: /usr/local/bin/top
    (root) NOPASSWD: /usr/bin/ls
    (root) /bin/tail
    ```

Being able to execute with `sudo` scripts in `/etc/init.d/`, `/etc/rc.d/`
or `/sbin/service` is the ability to start and stop services.

Also, If you can execute the package manager of your distribution, you can
install or remove software with it. If not, having `rwx` permission over a
directory will let you do a local installation of software by compiling it
there. This is a typical situation in many hosting companies’ services.

There are other ways for managing permissions, such as using *PolicyKit*, *
Extended ACLs* or *SELinux*, which may be preventing or allowing your
access. You should check them in that case.

!!! admonition "See also"

    [Connection and privileges needed](privileges.md)