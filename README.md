# Ansible Content for IBM Power Systems - IBM i

## Description
The <b>Ansible Content for IBM Power Systems - IBM i</b> provides modules, action plugins, roles and sample playbooks to automate tasks on IBM i, such as command execution, system and application configuration, work management, fix management, application deployment, etc.

IBM Power Systems is a family of enterprise servers that helps transform your organization by delivering industry leading resilience, scalability and accelerated performance for the most sensitive, mission critical workloads and next-generation AI and edge solutions. The Power platform also leverages open source technologies that enable you to run these workloads in a hybrid cloud environment with consistent tools, processes and skills.

Ansible Content for IBM Power Systems - IBM i, as part of the broader offering of <b>Ansible Content for IBM Power Systems</b>, is available from Ansible Galaxy and Redhat Ansible Automation Plaform and has community support.

## Requirements
In order to use the Ansible collection for Power Systems on IBM i with the latest release levels, you must have the following pre-requisite software installed and available on your Ansible server / control node and IBM i node:

- Dependencies on <b>non-IBM i Ansible server / control node</b>
  * <b>Python v3.10+</b>
    Python can be installed from a variety of sources, including the package manager for your operating system (apt, yum, etc). If you install Python from the package manager for your operating system, you must also install the development libraries (usually a package named python3-devel), as these are required when installing modules through pip. Note that Redhat customers using the Ansible Automation platform with the certified collection image should use Execution Environments instead of pip.

    The official Python website: [official Python website](https://www.python.org/downloads/)

    The unofficial Python version manager: [unofficial Python version manager](https://github.com/pyenv/pyenv)

  * <b>Ansible core v2.16 to v2.19</b>
    - Ansible core v2.16 requires Python 3.10+ on the Ansible control node.
    - Ansible core v2.17 requires Python 3.10+ on the Ansible control node.
    - Ansible core v2.18 requires Python 3.11+ on the Ansible control node.
    - Ansible core v2.19 requires Python 3.11+ on the Ansible control node.

    Users of Ansible core 2.15 should remain at collection release 3.2.0 due to changes with the ibmi_reboot module that support the latest Ansible core versions.

    The full compatiblity or support matrix for Ansible core versions and Python levels for the control node and targets is provided [here](https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html).

    Ansible can be installed from a variety of sources, including the package manager for your operating system (apt, yum, etc). You can also install it using pip, the package manager for Python: pip3 install ansible. Note that Redhat customers using the Ansible Automation platform with the certified collection image should use Execution Environments instead of pip install.

- Dependencies on <b>IBM i Ansible server / control node</b>
  * <b>Python v3.13</b>
    - This level of python is provided through the IBM i Open Source Software packages.

  * <b>Ansible core v2.18 to v2.19</b>
    - Ansible core v2.18 and v2.19 require Python 3.13 on the Ansible control node.

    Users of Ansible core 2.15 should remain at collection release 3.2.0 due to changes in the ibmi_reboot module that support the latest Ansible core versions.

    The full compatiblity or support matrix for Ansible core versions and Python levels for the control node and targets is provided [here](https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html).

- Dependencies on <b>IBM i node</b>:
  * 5733SC1 Base and Option 1
  * 5770DG1
  * python3
  * python3-itoolkit
  * ibm-iaccess (IBM i Access ODBC Driver)
  * python3-pyodbc (Python ODBC interface)

  To ensure a specific Python level, e.g., Python 3.9 or Python 3.13, that is compatible with the version of Ansible core on the control node,
  the python package prefix should instead specify the full Python level, e.g., python39 or python3.13 instead of python3, for installation.

  The IBM i collection has migrated from using the ibm_db package to using pyodbc with the IBM i Access ODBC Driver. This change was necessary because the IBM i open source stack no longer supports the ibm_db package ([Github issue 229](https://github.com/IBM/ansible-for-i/issues/229)) with Python 3.13, so Python 3.9 was only available for managed nodes. By using ODBC, IBM i managed nodes may now use Python 3.13.

- Additional dependencies on <b>IBM i Ansible server / control node</b>:
  * Ansible v2.15+ is not available as a prepackaged rpm for IBM i, yet can be installed with python pip. In the documentation site noted below under "Resources" there are detailed instructions provided in the "Getting Started" section for setting up Ansible with pip.
  * Ansible v2.16 and v2.17 cannot be used on an IBM i control node with the currently available IBM i Python packages.

## Known Issues

- An IBM i managed or target node at release 7.6 uses a newer version of ssh (OpenSSH 9.6) that has RSA requirements that are incompatible with the default IBM i OSS paramiko level 2.7.2 that is currently provided for IBM i python 3.9. Users should manually update paramiko to 2.9.0 or 2.12.0 levels such as with the command "<b>pip3.9 install paramiko==2.9.0</b>" until the default OSS paramiko package is updated, otherwise an authenticaion error during connect will occur between the paramiko client and the remote ssh server at the 7.6 OS release level.

## Limitations

- The shift to ODBC from ibm_db for database operations has introduced a dependency
on the database host server (*DATABASE) being online for full functionality due to the local TCP/IP connection with the ODBC driver (instead of using IPC such as with ibm_db). What this means is that modules that require SQL operations will error off when the database server is offline with a clear message indicating this condition; this state also impacts become_user functionality. However, modules only dependent on CL commands, such as ibmi_cl_command, will still function due to failback to the iToolkit DirectTransport from the primary iToolkit DatabaseTransport, albeit with limitations such as unavailable joblog information and iCmd5250 output is not captured. The *DATABASE host server can still be stopped and started without issue using the ibmi_host_server_service module (sans become_user).

## Installation

Detailed installation instructions are available at the [github installation site](https://ibm.github.io/ansible-for-i/installation.html). This site provides information on installing the collection and any necessary prerequisites.

## Use Cases

The primary use cases for the collection include: command execution, fix management, security compliance checking, systems checking
(health, work management, etc.), and application deployment using a continuous integration and continuous deployment (CICD) model.
Several of these collection use cases provide a set of playbooks that can be customized by the user and are located
in the [github usecases directory](https://github.com/IBM/ansible-for-i/tree/devel/usecases).
There are other playbook examples in the [github playbooks directory](https://github.com/IBM/ansible-for-i/tree/devel/playbooks).

## Testing

The collection testing consists of the executing the Ansible sanity test, applying the Ansible lint tool on all published YAML source, and applying the set of [integration tests](https://github.com/IBM/ansible-for-i/tree/devel/tests/integration/targets) for the collection modules and roles.
The collection testing environment uses Ansible core 2.19 and various Python levels such as 3.11 to 3.13 with the control node and Python level 3.9 or 3.13 on the IBM i target node.

## Contributing

Users may contribute to the collection by creating a [github issue](https://github.com/IBM/ansible-for-i/issues) for an enhancement or bug fix and then creating a [github pull request](https://github.com/IBM/ansible-for-i/pulls) for evaluation.

## Support

As Red Hat Ansible Certified Content, this collection is entitled to support through the Red Hat Ansible Automation Platform (AAP) for Redhat AAP customers using the **Create issue** button on the top right corner.

If the collection has been obtained either from Galaxy or GitHub, then
users can open an issue for any suspected bugs (or enhancement requests, etc.) as a [Github issue](https://github.com/IBM/ansible-for-i/issues) with the ansible-for-i Github project. Github issues are addressed by IBM based on potential severity/impact of a problem, frequency of a problem, and developer resource availability. Other community members (non-IBM) may also help with Github issues.

## Release Notes and Roadmap

The release notes are in the github repository [CHANGELOG.md](https://github.com/IBM/ansible-for-i/blob/devel/CHANGELOG.md) file.

## Related Information

For detail guides and reference, please visit the github [Documentation](https://ibm.github.io/ansible-for-i/index.html) site.

## License Information
Some portions of this collection are licensed under GNU General Public License, Version 3.0, and other portions of this collection are licensed under Apache License, Version 2.0.
See individual files for applicable licenses.

## Copyright
© Copyright IBM Corporation 2020
