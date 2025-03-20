# Clean up

In this document you'll learn how to:

* Exit the MySQL command client shell and the Docker container

* Remove the Docker container and the Docker image

* Remove the Docker volume.

The steps are as follows:
{.power-number}

1. To exit the MySQL command client shell in `psmysql2` container, we use `exit`. You can also use the `\q` or `quit` commands. The execution of the statement also closes the connection.

    ```{.bash data-prompt="mysql>"}
    mysql> exit
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Bye
        ```

2. Remove docker containers and images, if you no longer need docker containers / images or want to free up disk space. To remove a docker container, use the command `docker rm` followed by the container name or the container ID. To remove a docker image, use the command `docker rmi` followed by the image ID or name and the tag. The example uses the `-f` option to force the removal.

    * Remove `psmysql2`, `psmysql` and `pxb` Docker containers:

        ```{.bash data-prompt="$"}
        $ docker container rm psmysql2 -f
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            psmysql2
            ```

        ```{.bash data-prompt="$"}
        $ docker container rm psmysql -f
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            psmysql
            ```
        
        ```{.bash data-prompt="$"}
        $ docker container rm pxb -f
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            pxb
            ```

    * Remove `percona/percona-server:8.0.34` and `percona/percona-xtrabackup:8.0.34` Docker images

        ```{.bash data-prompt="$"}
        $ docker image rmi percona/percona-server:8.0.34
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            Untagged: percona/percona-server:8.0.34
            ```

        ```{.bash data-prompt="$"}
        $ docker image rmi percona/percona-xtrabackup:8.0.34
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            Untagged: percona/percona-server:8.0.34
            Untagged: percona/percona-server@sha256:4944f9b365e0dc88f41b3b704ff2a02d1459fd07763d7d1a444b263db8498e1f
            Deleted: sha256:b2588da614b1f382468fc9f44600863e324067a9cae57c204a30a2105d61d9d9
            Deleted: sha256:1ceaa6dc89e328281b426854a3b00509b5df13826a9618a09e819a830b752ebd
            Deleted: sha256:77471692427a227eb16d06907357956c3bb43f0fdc3ecf6f8937e1acecae24fe
            Deleted: sha256:8db06cc7b0430437edc7f118b139d2195cb65e2e8025f9a4517d16778f615384
            Deleted: sha256:e5a57a2fafec4ab9482240f28927651d56545c19626e344aceb8be3704c3c397
            Deleted: sha256:f86198f39b893674d44d424c958f23183bf919d2ced20e1f519714d0972d75ed
            Deleted: sha256:db9672f7e12e374d5e9016b758a29d5444e8b0fd1246a6f1fc5c2b3c847dddcf
            ```

3. Remove docker volume if a container does not use the volume, and you no longer need it

    Remove `backupvol` and `myvol2` Docker volumes:

    ```{.bash data-prompt="$"}
    $ docker volume rm backupvol
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        backupvol
        ```

    ```{.bash data-prompt="$"}
    $ docker volume rm myvol2
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        myvol2
        ```

## Next step

[Next steps :material-arrow-right:](quickstart-next-steps.md){.md-button}