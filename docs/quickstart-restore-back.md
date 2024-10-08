# Restore the backup

The following steps describe how to restore your backup to another Percona Server container and check whether the data is available.
{.power-number}

1. Create another Docker volume

    ```{.bash data-prompt="$"}
    $ docker volume create myvol2
    ```
    
    ??? example "Expected output"

        ```{.text .no-copy}
        myvol2
        ```

2. Run another Percona Server container to restore the backup to

    | Option | Description |
    |---|---|
    | `--name` | Provides a name to the container. If you do not use this option, Docker adds a random name. |
    | `-d` | Detaches the container. The container runs in the background. |
    | `-e` | Adds an environmental variable. This example adds the  ` MYSQL_ROOT_PASSWORD `  environment variable. The instance refuses to initialize if no environmental variable is added. Choose a more secure password, if needed. |
    | `myvol2` | Indicates the persistent storage for the database. |
    | `8.4` | Use this tag to specify a specific version. |

    You must provide at least one environment variable to access the database, such as `MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_USER`, and `MYSQL_PASSWORD` or the instance refuses to initialize.

    For this document, we are using the `8.4` tag. In Docker, a tag is a label assigned to an image. Tags are used to maintain different versions of an image. If we did not add a tag, Docker uses `latest` as the default tag and downloads the latest image from [percona/percona-server on the Docker Hub].

    To use a Docker volume for persistent storage with a database, specify the path where the database stores its data inside the container, usually `/var/lib/mysql`.

    * Run a Docker container example

        ```{.bash data-prompt="$"}
        $ docker run -d -p 3307:3306 --name psmysql2 -e MYSQL_ROOT_PASSWORD=secret -v myvol2:/var/lib/mysql percona/percona-server:8.4
        ```

    ??? example "Expected output"

        ```{.text .no-copy}

        4501d5524461b4483d414bd218d49ed4f47599add7d7fb81e157951a7a52f3d1
        ```
 
3. Stop `psmysql2` container

    ```{.bash data-prompt="$"}
    $ docker stop psmysql2
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        psmysql2
        ```

4. Remove all created files in `myvol2` to allow xtrabackup restore data to `myvol2`

    The `--rm` option automatically removes the temporary container created from percona/percona-xtrabackup:8.0.34 image after the container exits. 

    ```{.bash data-prompt="$"}
    $ docker run --volumes-from psmysql2 -v backupvol:/backup_84 -it --rm --user root percona/percona-xtrabackup:8.4 /bin/bash -c "rm -rf /var/lib/mysql/*"
    ```

    If the command executes successfully, the expected output is empty.

5. Restore backup of `psmysql` from `backupvol` to a new `psmysql2` instance.

    ```{.bash data-prompt="$"}
    $ docker run --platform linux/amd64 --volumes-from psmysql2 -v backupvol:/backup_84 -it --rm --user root percona/percona-xtrabackup:8.4 /bin/bash -c "xtrabackup --copy-back --datadir=/var/lib/mysql/ --target-dir=/backup_84" 
    ```

    ??? example "Expected output"
    
        ```{.text .no-copy}
        2024-10-07T14:08:59.127166-00:00 0 [Note] [MY-011825] [Xtrabackup] recognized server arguments: --datadir=/var/lib/mysql/
        2024-10-07T14:08:59.128951-00:00 0 [Note] [MY-011825] [Xtrabackup] recognized client arguments: --copy-back=1 --target-dir=/backup_84
        xtrabackup version 8.4.0-1 based on MySQL server 8.4.0 Linux (x86_64) (revision id: 3792f907)
        2024-10-07T14:08:59.129407-00:00 0 [Note] [MY-011825] [Xtrabackup] cd to /backup_84/

        ...

        2024-10-07T14:08:59.129407-00:00 0 1 [Note] [MY-011825] [Xtrabackup] Done: Copying ./ibtmp1 to /var/lib/mysql/ibtmp1 

        2024-10-07T14:08:59.129407-00:00 0 [Note] [MY-011825] [Xtrabackup] completed OK! 
        ``` 

    This command restores the backup files from the `backup_8034` volume to the `psmysql2` container. It uses the `percona/percona-xtrabackup:8.0.34` image to run a temporary container with root privileges. It executes the xtrabackup tool with the `--copy-back` option, which copies the files from the `backup_8034` volume to the /`var/lib/mysql/` directory in the `psmysql2` container. The command uses --rm option to delete the temporary container after it exits.

## Validate the backup

This section describes the backup validation steps assuming that you backed up `mydb` database with the `employees` table as we have in our example. The validation steps may vary depending on your data set.
{.power-number}

1. Change the owner of the files in `myvol2` from `root` to `mysql`

    To avoid permission issues when running `psmysql2` container, you need to change the owner because the files were restored by `root` user and `psmysql2` will use `mysql` user.

    ```{.bash data-prompt="$"}
    $ docker run --volumes-from psmysql2 -v backupvol:/backup_84 -it --rm --user root percona/percona-xtrabackup:8.4 /bin/bash -c "chown -R mysql:mysql /var/lib/mysql/" 
    ```

    If the command executes successfully, the expected output is empty.
 
2. Start the `psmysql2` container

    ```{.bash data-prompt="$"}
    $ docker start psmysql2
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        psmysql2
        ```

3. Connect to the database instance.

    For this example, we have the following options:

    | Option     | Description                                                                        |
    | ---------- | ---------------------------------------------------------------------------------- |
    | `it`       | Interact with the container and be a pseudo-terminal                               |
    | `psmysql2` | Running container name                                                             |
    | `mysql`    | Connects to a database instance                                                    |
    | `-u`       | Specifies the user account used to connect                                         |
    | `-p`       | Use this password when connecting |

    * Connect to the database instance example
    
        ```{.bash data-prompt="$"}
        $ docker exec -it psmysql2 mysql -uroot -p
        ```

        You are prompted to enter the password, which is `secret`.

        ```{.text .no-copy}
        Enter password:
        ```

        You should see the following result.

        ??? example "Expected output"

            ```{.text .no-copy}
            Welcome to the MySQL monitor.  Commands end with ; or \g.
            Your MySQL connection id is 10
            Server version: 8.4.0-1 Percona Server (GPL), Release 1, Revision 238b3c02

            Copyright (c) 2009-2024 Percona LLC and/or its affiliates
            Copyright (c) 2000, 2024, Oracle and/or its affiliates.

            Oracle is a registered trademark of Oracle Corporation and/or its
            affiliates. Other names may be trademarks of their respective
            owners.

            Type 'help;' or '\h' for help. Type '\c' to clear the current input statement. 
            ```

4. Check the list of databases to make sure, the backed up, `mydb` database is in the list.

    ```{.bash data-prompt="mysql>"}
    mysql> show databases; 
    ```

    ??? example "Expected output"
    
        ```{.text .no-copy}
        +--------------------+ 

        | Database           | 

        +--------------------+ 

        | information_schema | 

        | mydb               | 

        | mysql              | 

        | performance_schema | 

        | sys                | 

        +--------------------+ 

        5 rows in set (0.03 sec) 
        ```

5. Use the `mydb` database.

    ```{.bash data-prompt="mysql>"}
    mysql> use mydb; 
    ```

    ??? example "Expected output"
    
        ```{.text .no-copy}
        Database changed
        ```

6. Check that your table contains data

    ```{.bash data-prompt="mysql>"} 
    mysql> SELECT * FROM employees; 
    ```

    ??? example "Expected output"
    
        ```{.text .no-copy}
        +----+--------------------+-----------------------------------+-------------+ 

        | id | name               | email                             | country     | 

        +----+--------------------+-----------------------------------+-------------+ 

        |  1 | Erasmus Richardson | posuere.cubilia.curae@outlook.net | England     | 

        |  2 | Jenna French       | rhoncus.donec@hotmail.couk        | Canada      | 

        |  3 | Alfred Dejesus     | interdum@aol.org                  | Austria     | 

        |  4 | Hamilton Puckett   | dapibus.quam@outlook.com          | Canada      | 

        |  5 | Michal Brzezinski  | magna@icloud.pl                   | Poland      | 

        |  6 | Zofia Lis          | zofial00@hotmail.pl               | Poland      | 

        |  7 | Aisha Yakubu       | ayakubu80@outlook.com             | Nigeria     | 

        |  8 | Miguel Cardenas    | euismod@yahoo.com                 | Peru        | 

        |  9 | Luke Jansen        | nibh@hotmail.edu                  | Netherlands | 

        | 10 | Roger Pettersen    | nunc@protonmail.no                | Norway      | 

        +----+--------------------+-----------------------------------+-------------+ 

        10 rows in set (0.00 sec)
        ```

## Next steps

[Clean up :material-arrow-right:](quickstart-exit.md){.md-button}
