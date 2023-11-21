# Ansible Content for IBM Power Systems - IBM i
The <b>Ansible Content for IBM Power Systems - IBM i</b> provides modules, action plugins, roles and sample playbooks to automate tasks on IBM i, such as command execution, system and application configuration, work management, fix management, application deployment, etc.

# Ansible Content for IBM Power Systems
IBM Power Systems is a family of enterprise servers that helps transform your organization by delivering industry leading resilience, scalability and accelerated performance for the most sensitive, mission critical workloads and next-generation AI and edge solutions. The Power platform also leverages open source technologies that enable you to run these workloads in a hybrid cloud environment with consistent tools, processes and skills.

Ansible Content for IBM Power Systems - IBM i, as part of the broader offering of <b>Ansible Content for IBM Power Systems</b>, is available from Ansible Galaxy and has community support.

# Requirements
In order to use this Ansible Content for IBM Power Systems, you must have the following pre-requisite software installed and available on your Ansible server and IBM i node:

- Dependencies on Ansible server
  * Python v3.9+
    Python can be installed from a variety of sources, including the package manager for your operating system (apt, yum, etc). If you install Python from the package manager for your operating system, you must also install the development libraries (usually a package named python3-devel), as these are required when installing modules through pip.

    The official Python website: <a href="https://www.python.org/downloads/" target="_blank">official Python website</a>

    The unofficial Python version manager: <a href="https://github.com/pyenv/pyenv" target="_blank">unofficial Python version manager</a>

  * Ansible v2.14+

    Ansible can be installed from a variety of sources, including the package manager for your operating system (apt, yum, etc). You can also install it using pip, the package manager for Python: pip3 install ansible

- Dependencies on IBM i node:
  * 5733SC1 Base and Option 1
  * 5770DG1
  * python3
  * python3-itoolkit
  * python3-ibm_db

- Dependencies on IBM i Ansible server:
  * Ansible v2.14+ is not available as a prepackaged rpm for IBM i, yet can be installed with python pip. In the documentation site noted below under "Resources" there are detailed instructions provided in the "Getting Started" section for setting up Ansible with pip.

# Resources
For detail guides and reference, please visit the <a href="https://ibm.github.io/ansible-for-i/index.html" target="_blank">Documentation</a> site.

# License
Some portions of this collection are licensed under GNU General Public License, Version 3.0, and other portions of this collection are licensed under Apache License, Version 2.0.
See individual files for applicable licenses.

# Copyright
© Copyright IBM Corporation 2020
