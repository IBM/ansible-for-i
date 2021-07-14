..
.. SPDX-License-Identifier: Apache-2.0
..

Running Ansible to manage IBM i systems
=============================================

Ansible Basic Concepts
-------------------------------
Refer to Ansible community doc to learn Ansible Basic Concepts https://docs.ansible.com/ansible/latest/network/getting_started/basic_concepts.html

Configure your Ansible
-------------------------------

Refer to Ansible community doc to learn Ansible Configuration Settings https://docs.ansible.com/ansible/latest/reference_appendices/config.html

Here is an example of an ansible.cfg
::

    [defaults]
    library=~/.ansible/collections/ansible_collections/ibm/power_ibmi/plugins/modules
    action_plugins=~/.ansible/collections/ansible_collections/ibm/power_ibmi/plugins/action
    interpreter_python=/QOpenSys/pkgs/bin/python3

Build your inventory
------------------------

Refer to Ansible community doc to learn how to build your first inventory https://docs.ansible.com/ansible/latest/network/getting_started/first_inventory.html

Here is an example of the inventory file:

::

    [ibmi]
    your_ibmi_ip ansible_ssh_user=your_user ansible_ssh_pass=your_host_password

    [ibmi:vars]
    ansible_python_interpreter="/QOpensys/pkgs/bin/python3"
    ansible_ssh_common_args='-o StrictHostKeyChecking=no'

Run your first command or playbook
-----------------------------------

Refer to Ansible community doc to learn how to run Ansible command or playbook https://docs.ansible.com/ansible/latest/network/getting_started/first_playbook.html


Examples:
::

    ansible -i inventory.ini -m ibm.power_ibmi.ibmi_cl_command -a "cmd='crtlib lib(demo111)'"
    ansible -i inventory.ini db2mb1pa -m ibm.power_ibmi.ibmi_reboot