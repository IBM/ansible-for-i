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

In order to use this Ansible collection at the latest release levels, you must have the following pre-requisite software installed and available on your Ansible server / control node:

**Python v3.10+**

    Python can be installed from a variety of sources, including the package manager for your operating system (apt, yum, etc).
    If you install Python from the package manager for your operating system, you must also install the development libraries (usually a package named ``python3-devel``), as these are required when installing modules through ``pip``.
    Note that Redhat customers using the Ansible Automation platform with the certified collection image should use Execution Environments instead of pip install.

    - The official Python website: https://www.python.org/downloads/
    - The unofficial Python version manager: https://github.com/pyenv/pyenv

**Ansible core v2.16 to v2.19**

    - Ansible core v2.16 requires Python 3.10+ on the Ansible control node.
    - Ansible core v2.17 requires Python 3.10+ on the Ansible control node.
    - Ansible core v2.18 requires Python 3.11+ on the Ansible control node.
    - Ansible core v2.19 requires Python 3.11+ on the Ansible control node.

Users of Ansible core 2.15 should remain at collection release 3.2.0 due to changes with the ibmi_reboot module that support the latest Ansible core versions.

The full compatibility or support matrix for Ansible Core versions and Python levels for the control node and targets is provided at https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html.

Ansible can be installed from a variety of sources, including the package manager for your operating system (apt, yum, etc). You can also install it using ``pip``, the package manager for Python:

    ::

        pip3 install ansible

Note that Redhat customers using the Ansible Automation platform with the certified collection image should use Execution Environments instead of pip install.

Requirements for IBM i Ansible Server / Control Node
-----------------------------------------------------

In order to use this Ansible collection at the latest release levels, you must have the following pre-requisite software installed and available on your Ansible server / control node:

**Python v3.13**

    This level of python is provided through the IBM i Open Source Software packages.

**Ansible core v2.18 to v2.19**

    - Ansible core v2.18 and v2.19 require Python 3.13 on the Ansible control node.

Users of Ansible core 2.15 should remain at collection release 3.2.0 due to changes in the ibmi_reboot module that support the latest Ansible core versions.

For an IBM i Ansible control node, the latest levels of Ansible should be installed with Python pip because there is not a pre-packaged Ansible rpm above version 2.9. Ansible may also be installed from the GitHub source with a stable ansible branch. The following steps should be executed in an SSH session to the IBM i when installing Ansible with pip. This requires the IBM i SSH daemon to be started with the ``STRTCPSVR *SSHD`` command if it is not already started.

**Note:** These commands should be run in bash shell for best results:
::

    /QOpenSys/pkgs/bin/bash

Then proceed with the installation steps.

**Important: Set PATH First**

Before running yum, python, or ansible commands, ensure that ``/QOpenSys/pkgs/bin`` is in your ``PATH``. You can verify your current path with:

::

    echo $PATH

If you are using a Python virtual environment, ensure that the virtual environment ``bin`` directory is first in your ``PATH``. For example:

::

    export PATH=/HOME/TESTER/ansible-venv/bin:/QOpenSys/pkgs/bin:$PATH

If you are not using a virtual environment, either:

a. Use full paths:
   ::

       /QOpenSys/pkgs/bin/yum install package-name

b. Or set PATH temporarily:
   ::

       export PATH=/QOpenSys/pkgs/bin:$PATH

c. Or add to ``~/.profile`` permanently:
   ::

       echo 'export PATH=/QOpenSys/pkgs/bin:$PATH' >> ~/.profile
       source ~/.profile

1. **Create a Python Virtual Environment (Recommended)**

   Using a virtual environment isolates your Ansible installation and prevents conflicts with system packages.

   ::

       # Create virtual environment with Python 3.13
       python3.13 -m venv ~/ansible-venv

       # Activate the virtual environment
       source ~/ansible-venv/bin/activate

       # Verify you're using the venv Python
       which python
       # Should show: /HOME/YOURUSERNAME/ansible-venv/bin/python

   **Note:** After activating the venv, your prompt will change to show ``(ansible-venv)`` at the beginning.

2. Use yum to install the following required open source packages if not already present.

   ::

       /QOpenSys/pkgs/bin/yum install git
       /QOpenSys/pkgs/bin/yum install python3.13-cryptography
       /QOpenSys/pkgs/bin/yum install python3.13-paramiko
       /QOpenSys/pkgs/bin/yum install pase-utf8-locale
       /QOpenSys/pkgs/bin/yum install sshpass   # allows specifying ssh password if desired

   **Note:** These packages are installed system-wide and will be available to your virtual environment.

2. Configure your ``~/.profile`` (or ``~/.bash_profile`` when using bash) or execute the following commands to set the language environment variables.

   ::

       LANG=en_US.UTF-8
       LC_ALL=en_US.UTF-8
       export LANG
       export LC_ALL

3. Verify the language environment with the ``locale`` command.

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

4. Install Ansible. Choose one installation method.


   a. **If using a Python virtual environment (Recommended):**

      Make sure your virtual environment is activated:

      ::

          source ~/ansible-venv/bin/activate

      Then install Ansible:

      ::

          # Install full Ansible package (includes ansible-core 2.18.1)
          pip install ansible==11.1

          # OR install ansible-core only (lighter weight)
          pip install ansible-core==2.18.1

      **Note:** When the venv is activated, you can use ``pip`` directly instead of specifying the full path.

   b. **If not using a virtual environment:**

      Install Ansible for the current user:

      ::

          # Install full Ansible package
          python3.13 -m pip install --user ansible==11.1

          # OR install ansible-core only
          python3.13 -m pip install --user ansible-core==2.18.1

   **Important:** Ansible core v2.16 and v2.17 cannot be used with the currently available IBM i Python rpm packages on an IBM i server / control node. Use v2.18 or v2.19.

5. Verify that the expected executables are being used.

   ::

       # Check Python version
       python --version
       # Should show: Python 3.13.x

       # Check Ansible location
       which ansible-playbook
       # If using venv: /HOME/YOURUSERNAME/ansible-venv/bin/ansible-playbook
       # If using --user: /HOME/YOURUSERNAME/.local/bin/ansible-playbook

       # Check Ansible version
       ansible --version
       # Should show: ansible [core 2.18.x] or ansible [core 2.19.x]

       # Verify locale is set correctly
       echo $LANG
       # Should show: en_US.UTF-8

6. Ensure dependent collections are installed if only using ansible-core. Perform the following collection install commands if ``ansible-galaxy collection list`` does not show these collections.

   ::

       ansible-galaxy collection install openstack.cloud
       ansible-galaxy collection install ansible.posix


**Complete Setup Verification**

After completing all installation steps, verify your environment is correctly configured:

::

    # 1. Check shell
    echo $BASH_VERSION
    # Should show: 5.2.x or similar

    # 2. Check PATH includes necessary directories
    echo $PATH
    # Should include: /HOME/YOURUSERNAME/ansible-venv/bin (if using venv)
    # Should include: /QOpenSys/pkgs/bin

    # 3. Check locale
    locale
    # LANG and LC_ALL should be en_US.UTF-8

    # 4. Check Python versions available
    which python3.13
    which python3.9
    # Both should be found in /QOpenSys/pkgs/bin

    # 5. Check Ansible
    ansible --version
    # Should show ansible-core 2.18.x or 2.19.x with Python 3.13

    # 6. Check YUM
    yum --version
    # Should show version 3.4.3 or similar

    # 7. Test Ansible connectivity (if managing itself)
    ansible localhost -m ping
    # Should return: localhost | SUCCESS => {"changed": false, "ping": "pong"}


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
 - ibm-iaccess (IBM i Access ODBC Driver)
 - python3-pyodbc (Python ODBC interface)

1. 5733SC1 and 5770DG1 are license programs, you can download them at https://www-304.ibm.com/servers/eserver/ess/index.wss.

2. python3, python3-itoolkit, ibm-iaccess, and python3-pyodbc are open source packages. There are a few ways to install these packages and you could choose from one of them.
   To ensure a specific Python level, e.g., Python 3.9 or Python 3.13, that is compatible with the version of Ansible core on the control node,
   the python package prefix should instead specify the full Python level, e.g., python39 or python3.13 instead of python3, for installation.

**Installing YUM on IBM i (Required First Step)**

Before you can install packages, YUM must be installed on IBM i.

**Automatically enable with Ansible playbook on IBM i systems that have internet**

1. **Create an inventory file** with your IBM i system information (e.g., ``host_ibmi.ini``):

   ::

       [ibmi]
       your-ibmi-hostname ansible_ssh_user=youruser ansible_ssh_pass=yourpassword

   Or use SSH keys instead of password for better security.

2. **Run the setup playbook:**

   ::

       cd ~/.ansible/collections/ansible_collections/ibm/power_ibmi/playbooks/enable-ansible-for-i
       ansible-playbook -i host_ibmi.ini setup.yml

   The playbook will automatically:
   
   - Download bootstrap files directly to the IBM i server (using Ansible's get_url module)
   - Check if YUM is already installed on IBM i
   - Run the bootstrap script on IBM i to install YUM
   - Install required Python packages (python3-itoolkit, ibm-iaccess, python3-pyodbc)
   - Configure the IBM i environment for Ansible

   **No manual download required** - the playbook handles everything automatically!


**Automatically enable with Ansible playbook on IBM i systems that are offline**

An 'Offline' IBM i means that the IBM i system cannot connect to the internet and is not able to access https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/repo/. Before installing them, you can download installation packages to Ansible server.

::

    1) Make sure you have IBM i collection installed on your Ansible server.
    2) Issue below command in order to use setup playbook to enable IBM i:
    cd ~/.ansible/collections/ansible_collections/ibm/power_ibmi/playbooks
    3) Input information of target IBM i in host_ibmi.ini in order to run playbooks.
    4) Follow the steps in ~/.ansible/collections/ansible_collections/ibm/power_ibmi/playbooks/enable_offline_ibmi/README.md
    5) Run playbook with below command. The command assumes that the installation packages are in /tmp/ibmi-packages directory of Ansible server.
    ansible-playbook -i path/to/inventory enable_offline_ibmi/main.yml -e 'package_path=/tmp/ibmi-packages'

**Installing YUM manually**

If you prefer to install YUM manually, follow these steps:

1. **SSH to your IBM i system:**

   ::

       ssh youruser@your-ibmi-system

2. **Download bootstrap files directly on IBM i using Python:**

   Since curl is not available before yum is installed, use Python's built-in HTTP capabilities:

   ::

       # Download bootstrap.sh
       python3 -c "import urllib.request; urllib.request.urlretrieve('https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/bootstrap.sh', '/tmp/bootstrap.sh')"
       
       # Download bootstrap.tar.Z
       python3 -c "import urllib.request; urllib.request.urlretrieve('https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/bootstrap.tar.Z', '/tmp/bootstrap.tar.Z')"

3. **Make bootstrap.sh executable:**

   ::

       chmod +x /tmp/bootstrap.sh

4. **Run the bootstrap installation:**

   You can run this from either SSH or a 5250 terminal:

   **From SSH (ksh shell):**

   ::

       cd /tmp
       /QOpenSys/usr/bin/ksh bootstrap.sh

   **From 5250 terminal:**

   ::

       QSH CMD('exec /QOpenSys/usr/bin/ksh -c "/QOpenSys/usr/bin/ksh /tmp/bootstrap.sh > /tmp/bootstrap.log 2>&1"')

5. **Verify YUM installation:**

   ::

       /QOpenSys/pkgs/bin/yum --version

   Expected output should show YUM version 3.4.3 or similar.

6. **Add YUM to your PATH:**

   ::

       export PATH=/QOpenSys/pkgs/bin:$PATH



**Installing rpm packages manually**
    Rpm packages can be installed via 'yum' packages manager on IBM i. However, yum is not shipped by IBM i by default.
    Refer the guide here to install yum https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/system_administrators_guide/ch-yum.
    Then install the required packages at the desired levels by the below command(s):

::

    /QOpenSys/pkgs/bin/yum install python39 python39-itoolkit ibm-iaccess python39-pyodbc
    # and/or
    /QOpenSys/pkgs/bin/yum install python3.13 python3.13-itoolkit ibm-iaccess python3.13-pyodbc

