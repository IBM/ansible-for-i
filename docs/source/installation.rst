..
.. SPDX-License-Identifier: Apache-2.0
..

Installation
============

There are three options for installing the IBM i collection for Ansible:

* Installing using Ansible Galaxy

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

In order to use this Ansible collection, you must have the following pre-requisite software installed and available:

**Python v3.7+**

    Python can be installed from a variety of sources, including the package manager for your operating system (apt, yum, etc).
    If you install Python from the package manager for your operating system, you must also install the development libraries (usually a package named ``python3-devel``), as these are required when installing modules through ``pip``.

    - The official Python website: https://www.python.org/downloads/
    - The unofficial Python version manager: https://github.com/pyenv/pyenv

**Ansible v2.8+**

    Python can be installed from a variety of sources, including the package manager for your operating system (apt, yum, etc). You can also install it using ``pip``, the package manager for Python:

    ::

        pip install ansible

Installing using Ansible Galaxy
-------------------------------

You can use the ``ansible-galaxy`` command to install a collection from Ansible Galaxy, the package manager for Ansible:

::

    ansible-galaxy collection install iibm.power_ibmi

Installing from source
----------------------

You can use the ``ansible-galaxy`` command to install a collection built from source. To build your own collection, follow these steps:

1. Clone the repository:

::

    git clone https://github.com/LiJunBJZhu/i_collection_core.git

2. Build the collection artifact:

::

    cd ansible-collection
    ansible-galaxy collection build

3. Install the collection, replacing ``x.y.z`` with the current version:

::

    ansible-galaxy collection install ibm-power_ibmi-x.y.z.tar.gz