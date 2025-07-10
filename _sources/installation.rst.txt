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

Requirements for non-IBM i Ansible Server / Control Node
---------------------------------------------------------

In order to use this Ansible collection at **release 3.2.1** and beyond, you must have the following pre-requisite software installed and available on your Ansible server / control node:

**Python v3.10+**

    Python can be installed from a variety of sources, including the package manager for your operating system (apt, yum, etc).
    If you install Python from the package manager for your operating system, you must also install the development libraries (usually a package named ``python3-devel``), as these are required when installing modules through ``pip``.

    - The official Python website: https://www.python.org/downloads/
    - The unofficial Python version manager: https://github.com/pyenv/pyenv

**Ansible core v2.16 to v2.18**

    - Ansible core v2.16 requires Python 3.10+ on the Ansible control node.
    - Ansible core v2.17 requires Python 3.10+ on the Ansible control node.
    - Ansible core v2.18 requires Python 3.11+ on the Ansible control node.

Users of Ansible core 2.15 should remain at collection release 3.2.0 due to changes with the ibmi_reboot module that support the latest Ansible core versions.

The full compatiblity or support matrix for Ansible Core versions and Python levels for the control node and targets is provided at https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html.

Ansible can be installed from a variety of sources, including the package manager for your operating system (apt, yum, etc). You can also install it using ``pip``, the package manager for Python:

    ::

        pip3 install ansible

Requirements for IBM i Ansible Server / Control Node
-----------------------------------------------------

In order to use this Ansible collection at **release 3.2.1** and beyond, you must have the following pre-requisite software installed and available on your Ansible server / control node:

**Python v3.13**

    This level of python is provided through the IBM i Open Source Software packages.

**v2.18**

    - Ansible core v2.18 requires Python 3.13 on the Ansible control node.

Users of Ansible core 2.15 should remain at collection release 3.2.0 due to changes in the ibmi_reboot module that support the latest Ansible core versions.

For an IBM i Ansible control node, the latest levels of Ansible should be installed with python pip because there is not a pre-packaged Ansible rpm
above version 2.9. Ansible may also be installed from the github source with a stable ansible branch. The following steps should be executed
in an SSH session to the IBM i when installing Ansible with pip. This will require the IBM i SSH Daemon to be started with the ''STRTCPSVR *SSHD'' command
if it is not already started.

1. Use Yum to install the following required open source packages if not already present.

    ::

        yum install git
        yum install python3.13-cryptography
        yum install python3.13-paramiko
        yum install pase-utf8-locale
        yum install sshpass   # allows specifying ssh password if desired

2. Configure your ~/.profile (~/.bash_profile with bash) or execute the following commands to set the language environment variables.

    ::

        LANG=en_US.UTF-8
        LC_ALL=en_US.UTF-8
        export LANG
        export LC_ALL

3. Verify the language environment with the ''locale'' command.

    ::

        locale

        LANG=en_US.UTF-8
        LC_COLLATE="C"
        LC_CTYPE="C"
        LC_MONETARY="C"
        LC_NUMERIC="C"
        LC_TIME="C"
        LC_MESSAGES="C"
        LC_ALL=en_US.UTF-8

4. Install Ansible. Either full ansible (a) or ansible-core (b).

   a. Install Ansible at 11.X level (v2.18 core) with pip (skip step 3b). For example, to install level 11.1 that includes v2.18.1 ansible-core use the following:

      ::

          python3 -m pip install --user ansible==11.1

   b. Alternatively ansible-core may be installed instead of full ansible, but some additional ibmi dependent collections may need to be installed via ansible-galaxy. For example, to install ansible core v2.18.1 use the following command:

      ::

          python3 -m pip install --user ansible-core==2.18.1

   Note that Ansible core v2.16 and v2.17 cannot be used with the currently available IBM i Python rpm packages on an IBM i server / control node.
   
   The pip command may also be used directly for installing Ansible. An alternative command for 4(b) is

      ::

          pip3 install ansible-core==2.18.1

5. Add the following commands to your ~/.profile or execute them to include the ansible executables in your PATH.

   ::

       PATH=~/.local/bin:$PATH
       export PATH

6. Ensure dependent collections are installed if only using ansible-core. Perform the following collection install commands if
''ansible-galaxy collection list'' doesn't show these collections.

   ::

       ansible-galaxy collection install openstack.cloud

       ansible-galaxy collection install ansible.posix

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

1. 5733SC1 and 5770DG1 are license programs, you can download them at http://www-304.ibm.com/servers/eserver/ess/index.wss.

2. python3, python3-itoolkit, python3-ibm_db are open source packages. There are a few ways to install these packages and you could choose from one of them.
   To ensure a specific Python level, e.g., Python 3.9, that is compatible with the version of Ansible core on the control node,
   the python package prefix should instead specifiy the full Python level, e.g., python39 instead of python3, for installation.

**Installing rpm packages manually**
    Rpm packages can be installed via 'yum' packages manager on IBM i. However, yum is not shipped by IBM i by default.
    Refer the guide here to install yum https://bitbucket.org/ibmi/opensource/src/master/docs/yum/. Then install these packages by below command:

::

    /QOpenSys/pkgs/bin/yum install python3 python3-itoolkit python3-ibm_db 

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