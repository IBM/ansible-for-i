..
.. SPDX-License-Identifier: Apache-2.0
..

Installing IBM i collection to Ansible server
=============================================

There are two options to install IBM i collection for Ansible:

* Installing from Ansible Galaxy

  Ansible Galaxy is the package manager for Ansible. The collection is published to Ansible Galaxy on a regular basis: https://galaxy.ansible.com/ibm/power_ibmi

  In order to install using Ansible Galaxy, you must:

  1. Install all of the software listed in :ref:`Requirements`.
  2. Follow the instructions for :ref:`Installing using Ansible Galaxy`.

* Installing from source

  You may wish to install the collection from source if you cannot access Ansible Galaxy due to firewall or proxy issues, or if you need to install a version of the collection that has not yet been published.

  In order to install from source, you must:

  1. Install all of the software listed in :ref:`Requirements`.
  2. Follow the instructions for :ref:`Installing from source`.

Requirements
------------

In order to use this Ansible collection, you must have the following pre-requisite software installed and available on your Ansible server:

**Python v3.6+**

    Python can be installed from a variety of sources, including the package manager for your operating system (apt, yum, etc).
    If you install Python from the package manager for your operating system, you must also install the development libraries (usually a package named ``python3-devel``), as these are required when installing modules through ``pip``.

    - The official Python website: https://www.python.org/downloads/
    - The unofficial Python version manager: https://github.com/pyenv/pyenv

**Ansible v2.9+**

    Ansible can be installed from a variety of sources, including the package manager for your operating system (apt, yum, etc). You can also install it using ``pip``, the package manager for Python:

    ::

        pip install ansible

Installing using Ansible Galaxy
-------------------------------

You can use the ``ansible-galaxy`` command to install a collection from Ansible Galaxy, the package manager for Ansible:

::

    ansible-galaxy collection install ibm.power_ibmi

Installing from source
----------------------

You can use the ``ansible-galaxy`` command to install a collection built from source. To build your own collection, follow these steps:

1. Clone the repository:

::

    git clone https://github.com/IBM/ansible-for-i.git

2. Build the collection artifact:

::

    cd ansible-for-i
    ansible-galaxy collection build

3. Install the collection, replacing ``x.y.z`` with the current version:

::

    ansible-galaxy collection install ibm-power_ibmi-x.y.z.tar.gz

Enabling IBM i nodes
-------------------------------

Before IBM i systems can be managed-nodes of Ansible, a few dependencies have to be installed on IBM i.

 - 5733SC1 Base and Option 1
 - 5770DG1
 - python3
 - python3-itoolkit
 - python3-ibm_db

1. 5733SC1 and 5770DG1 are license programs, you can download them at
http://www-304.ibm.com/servers/eserver/ess/index.wss.

2. python3, python3-itoolkit, python3-ibm_db are open source packages. There are a few ways to install these packages and you could choose from one of them.

**Installing rpm packages manually**
    Rpm packages can be installed via 'yum' packages manager on IBM i. However, yum is not shipped by IBM i by default.
    Refer the guide here to install yum https://bitbucket.org/ibmi/opensource/src/master/docs/yum/. Then install these packages by below command:

::

    /Qopensys/pkgs/bin/yum install python3 python3-itoolkit python3-ibm_db 

**Installing rpm packages automatically onto IBM i systems which can access internet**

::

    1) Make sure you have IBM i collection installed on your Ansible server.
    2) Issue below command in order to use setup playbook to enable IBM i:
    cd ~/.ansible/collections/ansible_collections/ibm/power_ibmi/playbooks
    3) Input information of target IBM i in host_ibmi.ini in order to run playbooks.
    4) Run setup play book with below command:
    ansible-playbook -i host_ibmi.ini enable-ansible-for-i/setup.yml

**Installing rpm packages automatically onto IBM i systems which are offline**
    An 'Offline' IBM i means that the IBM i system cannot connect to the internet and is not able to access https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/repo/.
    Before installing them, you can download installation packages to Ansible server.

::

    1) Make sure you have IBM i collection installed on your Ansible server.
    2) Issue below command in order to use setup playbook to enable IBM i:
    cd ~/.ansible/collections/ansible_collections/ibm/power_ibmi/playbooks
    3) Input information of target IBM i in host_ibmi.ini in order to run playbooks.
    4) Follow the steps in ~/.ansible/collections/ansible_collections/ibm/power_ibmi/playbooks/enable_offline_ibmi/README.md
    5) Run playbook with below command. The command assumes that the installation packages are in /tmp/ibmi-packages directory of Ansible server.
    ansible-playbook -i path/to/inventory enable_offline_ibmi/main.yml -e 'package_path=/tmp/ibmi-packages'