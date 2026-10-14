# Compile and install from source

The following instructions compile Percona XtraBackup {{vers}} from source and install it. Run the commands as root or use `sudo`.

!!! note "Disk space and build time"

    The source tree with its submodules takes about 5.7 GB, and the build directory takes from about 2 GB to 8 GB, depending on the platform. Plan for at least 15 GB of free disk space. On a machine with 2 vCPUs, the build takes about 70 minutes. These figures were measured with Percona XtraBackup 8.4.

## 1. Install the prerequisites

Install `git`, a supported compiler, `cmake`, and the libraries that Percona XtraBackup links against. Percona XtraBackup {{vers}} also needs the TI-RPC library and the `rpcgen` tool. Percona XtraBackup {{vers}} requires GCC 11 or later, or Clang 14 or later.

=== "RHEL 9 and compatible (Rocky Linux, AlmaLinux, Oracle Linux)"

    Some build dependencies, such as `libev-devel` and `procps-ng-devel`, are in the CodeReady Linux Builder (CRB) repository. Enable the repository, then install the packages:

    ```shell
    sudo dnf install -y git dnf-plugins-core
    sudo dnf config-manager --set-enabled crb
    sudo dnf install -y gcc-toolset-14-gcc gcc-toolset-14-gcc-c++ gcc-toolset-14-binutils \
      gcc-toolset-14-annobin-annocheck gcc-toolset-14-annobin-plugin-gcc \
      cmake make openssl-devel libaio-devel bison libtool ncurses-devel libgcrypt-devel \
      libev-devel libcurl-devel zlib-devel zstd vim-common procps-ng-devel \
      libtirpc-devel rpcgen
    ```

    The repository name differs by distribution:

    * Rocky Linux and AlmaLinux: `crb`, as in the command above.
    * Red Hat Enterprise Linux: run `sudo subscription-manager repos --enable codeready-builder-for-rhel-9-$(arch)-rpms` instead of the `dnf config-manager` command.
    * Oracle Linux 9: run `sudo dnf config-manager --set-enabled ol9_codeready_builder` instead.

    On RHEL 9, `cmake` does not accept the system GCC. It looks for the compiler in `/opt/rh/gcc-toolset-14` and stops with an error if the gcc-toolset-14 packages are missing. You do not need to enable the toolset with `scl`: `cmake` finds it.

    To install the man pages, install the `python3-sphinx` package first:

    ```shell
    sudo dnf install -y python3-sphinx
    ```

=== "Ubuntu 24.04 or later, Debian 13"

    ```shell
    sudo apt update
    sudo apt install git bison pkg-config cmake devscripts debconf debhelper automake \
      ca-certificates libproc2-dev libcurl4-openssl-dev libaio-dev libncurses-dev \
      libssl-dev libtool zlib1g-dev libgcrypt20-dev libev-dev lsb-release build-essential \
      rsync libdbd-mysql-perl libnuma1 socat librtmp-dev vim-common lz4 liblz4-dev zstd \
      libtirpc-dev rpcsvc-proto python3-docutils
    ```

    To install the man pages, install the `python3-sphinx` package first:

    ```shell
    sudo apt install python3-sphinx
    ```

=== "Ubuntu 22.04"

    ```shell
    sudo apt update
    sudo apt install git bison pkg-config cmake devscripts debconf debhelper automake \
      ca-certificates libprocps-dev libcurl4-openssl-dev libaio-dev libncurses-dev \
      libssl-dev libtool zlib1g-dev libgcrypt20-dev libev-dev lsb-release build-essential \
      rsync libdbd-mysql-perl libnuma1 socat librtmp-dev vim-common lz4 liblz4-dev zstd \
      libtirpc-dev rpcsvc-proto python3-docutils
    ```

    To install the man pages, install the `python3-sphinx` package first:

    ```shell
    sudo apt install python3-sphinx
    ```

## 2. Get the source code

Clone the repository, check out the release tag, and fetch the submodules:

```shell
git clone https://github.com/percona/percona-xtrabackup.git
cd percona-xtrabackup
git checkout percona-xtrabackup-{{release}}
git submodule update --init --recursive
```

The `percona-xtrabackup-{{release}}` tag is the Percona XtraBackup {{release}} release. The `{{vers}}` branch contains unreleased development changes, so check it out only if you need them.

## 3. Generate the build pipeline

At this step, you have `cmake` run the commands in the `CMakeList.txt`
file to generate the build pipeline, i.e., a native build environment that will
be used to compile the source code).
{.power-number}

1. Change to the directory where you cloned the Percona XtraBackup repository
 
    ```shell
    cd percona-xtrabackup
    ```

2. Create a directory to store the compiled files and then change to that
directory:

    ```shell
    mkdir build
    cd build
    ```

3. Run `cmake`:

!!! note
 
    You can build *Percona XtraBackup* with man pages but this requires
    `python-sphinx` package which isn’t available from that main repositories
    for every distribution. If you installed the `python-sphinx` package you
    need to remove the `-DWITH_MAN_PAGES=OFF` from the following command.

```shell
cmake -DBUILD_CONFIG=xtrabackup_release -DWITH_MAN_PAGES=OFF ..
```

<!--
If you use [Pro builds](./pxb-pro.md), run the following command

```shell
cmake -DPROBUILD=1 -DBUILD_CONFIG=xtrabackup_release -DWITH_MAN_PAGES=OFF ..
```
-->

### Parameter Information

| Parameter | Description |
|---------------|-----------------|
| `-DPROBUILD=1` | This option enables a Pro build. |
| `-DBUILD_CONFIG` | This option builds a release/optimized version of the xtrabackup binary. |
| `-DWITH_MAN_PAGES` | To build Percona XtraBackup man pages, use `ON` or remove this parameter from the command line (it is `ON` by default). To install the man pages, install the python3-sphinx package first. |

!!! important
 
    CMake Error at CMakeLists.txt:367 (MESSAGE): Please do not build in-source. Out-of source builds are highly recommended: you can have multiple builds for the same source, and there is an easy way to do cleanup, simply remove the build directory (note that ‘make clean’ or ‘make distclean’ does `not` work)
    
    You `can` force in-source build by invoking cmake with `-DFORCE_INSOURCE_BUILD=1`.

## 4. Compile the source code

To compile the source code in your `build` directory, use the `make` command.
{.power-number}

1. Change to the `build` directory (created in step 3).

2. Run the `make` command. This command may take a long time to complete.

    ```shell
    make
    ```
   
    To use all CPU threads and make compilation faster please use:

    ```shell
    make -j$(nproc --all)
    ```

## 5. Install on the target system

The following command installs all *Percona XtraBackup* binaries *xtrabackup*
and tests to default location on the target system: `/usr/local/xtrabackup`.

Run `make install` to install *Percona XtraBackup* to the default location.

```shell
sudo make install
```

### Install to a non-default location

You may use the `DESTDIR` parameter with `make install` to install *Percona
XtraBackup* to another location. Make sure that the effective user is able to
write to the destination you choose.

```shell
sudo make DESTDIR=<DIR_NAME> install
```

In fact, the destination directory is determined by the installation layout
(`-DINSTALL_LAYOUT`) that `cmake` applies (see
step 3). In addition to
the installation directory, this parameter controls a number of other
destinations that you can adjust for your system.

By default, this parameter is set to `STANDALONE`, which implies the
installation directory to be `/usr/local/xtrabackup`.

!!! admonition "See also"
 
    [MySQL Documentation: -DINSTALL_LAYOUT :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/source-configuration-options.html#option_cmake_install_layout)

## 6. Run Percona XtraBackup

After *Percona XtraBackup* is installed on your system, you may run it by using
the full path to the `xtrabackup` command:

```shell
/usr/local/xtrabackup/bin/xtrabackup
```

To run `xtrabackup` without the full path, add the `bin` directory to your `PATH` environment variable:

```shell
export PATH=$PATH:/usr/local/xtrabackup/bin
xtrabackup --version
```

Alternatively, you may consider placing a soft link (using `ln -s`) to one of
the locations listed in your `PATH` environment variable.

To view the documentation with `man`, update the `MANPATH` variable.

!!! note "Default socket"

    A binary built from source connects to the server through `/tmp/mysql.sock` by default. If your server uses a different socket, for example `/var/lib/mysql/mysql.sock`, pass it with the `--socket` option:

    ```shell
    xtrabackup --backup --socket=/var/lib/mysql/mysql.sock --target-dir=/data/backups/
    ```

    To change the default when you build, add `-DMYSQL_UNIX_ADDR=<path>` to the `cmake` command.

