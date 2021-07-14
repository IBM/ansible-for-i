Overview for Ansible CI/CD integration with Ansible Tower use case

**==============**



The playbooks in this directory provides you the samples do your own modifications.

This set of playbooks cannot be used directly since they are designed to be implemented to Ansible Tower automatically, some of the variables are inherited from
https://github.com/IBM/ansible-for-i/tree/dev/usecases/towerapi

Contents may be continuously added and enhanced.



Introduction

**--------------**

This set of playbooks demonstrate a full cycle of CI/CD process on IBM i.

1. Support applications built with either stream files or native objects.
2. Support building your applications on an existing IBM i or on a new IBM i by provisioning with PowerVC.



Playbooks

**--------------**

0. build_start.yml - kick off point of building process
1. provision_vm.yml - creating a compute instance for building each time by leveraging PowerVC.
2. add_build_system.yml - add the build system into in-memory inventory.
3. ibmi_install_dependencies.yml - install yum and git as needed
4. build.yml - invoke CL command or script to do build on build machine.
5. post_build_actions.yml - actions you may want to do after building completes, like verification, UT, FVT, etc.
6. cleanup.yml - cleanup local workspace, remote building directories, libraries, destroy compute instance on demand.
