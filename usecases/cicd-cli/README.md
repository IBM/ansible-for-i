Overview for Ansible CI/CD use case

**==============**



The playbooks in this directory provides you the samples that you could directly use or do your own modifications.

Contents may be continuously added and enhanced.



Introduction

**--------------**

This set of playbooks demonstrate a full cycle of CI/CD process on IBM i. 

1. Support applications built with either stream files or native objects.
2. Support building your applications on an existing IBM i or on a new IBM i by provisioning with PowerVC.



Playbooks

**--------------**

1. host.ini - define your existing build machine info or the compute  instance info you want to create in building
2. main.yml - starting point of the process.
3. git_clone.yml - clone source code to your local workspace.
4. provision_vars.yml - variables that are used for provisioning VM before building your application.
5. provision_vm.yml - creating a compute instance for building each time by leveraging PowerVC.
6. add_build_system.yml - add the build system into in-memory inventory
7. put_code.yml - transfer your source code to remote IBM i, aka build machine.
8. build.yml - invoke CL command or script to do build on build machine.
9. post_build_actions.yml - actions you may want to do after building completes, like verification, UT, FVT, etc.
10. cleanup.yml - cleanup local workspace, remote building directories, libraries, destroy compute instance on demand.



**### Example**



\```

ansible-playbook -i hosts.ini ./main.yml

\```

