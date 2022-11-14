# Working with SELinux

*Percona XtraBackup* is installed as an unconfined process running in an undefined domain. SELinux allows unconfined processes almost all access and the processes only use Discretionary Access Control (DAC) rules.

You find the current state of the *Percona XtraBackup* file with the following command:

```shell
$ ls -Z /usr/bin | grep xtrabackup
```
The results should be similar to the following:

```text
-rwxr-xr-x. root root   system_u:object_r:bin_t:s0       xtrabackup
```

The SELinux context is the following:

* user (root)

* role (object_r)

* type (bin_t)

* level (s0)

The unconfined domain supports the network-facing services, which are protected by SELinux. These domains are not exposed. In this configuration, SELinux protects against remote intrusions but local intrusions, which require local access, are not confined.

*Percona XtraBackup* works locally. The service is not network-facing and cannot be exploited externally. The service interacts only with the local user, who provides the parameters. *Percona XtraBackup* requires access to the `target-dir` location.

## Confine XtraBackup

You can modify your security configuration to confine *Percona XtraBackup*. The first question is where to store the backup files. The service requires read and write access to the selected location.

You can use either of the following methods:


* Allow *Percona XtraBackup* to write to any location. The user provides any path to the `target-dir` parameter.


* Allow *Percona XtraBackup* to write to a specific location, such as /backups or the user’s home directory.

The first option opens the entire system to read and write. Select the second option to harden your security.

## Install SELinux tools

To work with policies, you must install the SELinux tools. To find which package provides the `semanage` command and install the package. The following is an example on CentOS 7.

> ```shell
> $ yum provides *bin/semanage
```
The result should list the packages.

```text
> ...
> policycoreutils-python-2.5-34.el7.x86_64 : SELinux policy core python utilities
> ...
```
To install missing packages, run the following:

```shell
> $ sudo yum install -y policycoreutils-python
> ```

The following is an example on CentOS 8:

> ```shell
> $ yum provides *bin/semanage
```
The result should list the missing packages.

```text
> ...
> policycoreutils-python-utils-2.8-16.1.el8.noarch : SELinux policy core python utilities
```
Run the following to install the missing packages: 

`` shell
> $ sudo yum install -y policycoreutils-python-utils
> ```

## Create a policy

Use a modular approach to create an SELinux policy. Create a policy module to manage XtraBackup. You must create a `.te` file for type enforcement, and an optional `.fc` file for the file contexts.

Use <code>$ ps -efZ | grep xtrabackup</code> to verify the service is not confined by SELinux.

Create the `xtrabackup.fc` file and add content. This file defines the security contexts.

> ```text
> /usr/bin/xtrabackup    -- gen_context(system_u:object_r:xtrabackup_exec_t,s0)
> /usr/bin/xbcrypt    -- gen_context(system_u:object_r:xtrabackup_exec_t,s0)
> /usr/bin/xbstream    -- gen_context(system_u:object_r:xtrabackup_exec_t,s0)
> /usr/bin/xbcloud    -- gen_context(system_u:object_r:xtrabackup_exec_t,s0)
> /backups(/.*)?       system_u:object_r:xtrabackup_data_t:s0
> ```

!!! note
 
    If you are using the `/backups` directory you must have the last line. If you are storing the backups in the user’s home directory, you can omit this line.

Download the `xtrabackup.te` file from the following location:

[https://github.com/percona/percona-xtrabackup/tree/8.0/packaging/percona/selinx](https://github.com/percona/percona-xtrabackup/tree/8.0/packaging/percona/selinx)

!!! note
 
    In the file, the sections in bold should be modified for your system. The fc file can also be downloaded from the same location.

Compile the policy module:

> ```shell
> $ make -f /usr/share/selinux/devel/Makefile xtrabackup.pp
> ```

Install the module:

> ```shell
> $ semodule -i xtrabackup.pp
> ```

Tag the PXB binaries with the proper SELinux tags, such as `xtrabackup_exec_t`.

> ```shell
> $ restorecon -v /usr/bin/*
> ```

If you store your backups at `/backups`, restore the tag in that location:

> ```shell
> $ restorecon -v /backups
> ```

!!! note
 
    Remember to add the standard Linux DAC permissions for this directory.

Perform the backup in the standard way.
