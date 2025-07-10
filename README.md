# Ansible Content for IBM Power Systems - IBM i

## Description
The <b>Ansible Content for IBM Power Systems - IBM i</b> provides modules, action plugins, roles and sample playbooks to automate tasks on IBM i, such as command execution, system and application configuration, work management, fix management, application deployment, etc.

IBM Power Systems is a family of enterprise servers that helps transform your organization by delivering industry leading resilience, scalability and accelerated performance for the most sensitive, mission critical workloads and next-generation AI and edge solutions. The Power platform also leverages open source technologies that enable you to run these workloads in a hybrid cloud environment with consistent tools, processes and skills.

Ansible Content for IBM Power Systems - IBM i, as part of the broader offering of <b>Ansible Content for IBM Power Systems</b>, is available from Ansible Galaxy and Redhat Ansible Automation Plaform and has community support.

## Requirements
In order to use the Ansible collection for Power Systems on IBM i with <b>release 3.2.1</b> and beyond, you must have the following pre-requisite software installed and available on your Ansible server / control node and IBM i node:

- Dependencies on <b>non-IBM i Ansible server / control node</b>
  * <b>Python v3.10+</b>
    Python can be installed from a variety of sources, including the package manager for your operating system (apt, yum, etc). If you install Python from the package manager for your operating system, you must also install the development libraries (usually a package named python3-devel), as these are required when installing modules through pip.

    The official Python website: <a href="https://www.python.org/downloads/" target="_blank">official Python website</a>

    The unofficial Python version manager: <a href="https://github.com/pyenv/pyenv" target="_blank">unofficial Python version manager</a>

  * <b>Ansible core v2.16 to v2.18</b>
    - Ansible core v2.16 requires Python 3.10+ on the Ansible control node.
    - Ansible core v2.17 requires Python 3.10+ on the Ansible control node.
    - Ansible core v2.18 requires Python 3.11+ on the Ansible control node.

    Users of Ansible core 2.15 should remain at collection release 3.2.0 due to changes with the ibmi_reboot module that support the latest Ansible core versions.

    The full compatiblity or support matrix for Ansible core versions and Python levels for the control node and targets is provided <a href="https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html" target="_blank">here</a>.

    Ansible can be installed from a variety of sources, including the package manager for your operating system (apt, yum, etc). You can also install it using pip, the package manager for Python: pip3 install ansible

- Dependencies on <b>IBM i Ansible server / control node</b>
  * <b>Python v3.13</b>
    - This level of python is provided through the IBM i Open Source Software packages.

  * <b>Ansible core v2.18</b>
    - Ansible core v2.18 requires Python 3.13 on the Ansible control node.

    Users of Ansible core 2.15 should remain at collection release 3.2.0 due to changes in the ibmi_reboot module that support the latest Ansible core versions.

    The full compatiblity or support matrix for Ansible core versions and Python levels for the control node and targets is provided <a href="https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html" target="_blank">here</a>.

- Dependencies on <b>IBM i node</b>:
  * 5733SC1 Base and Option 1
  * 5770DG1
  * python3
  * python3-itoolkit
  * python3-ibm_db

  To ensure a specific Python level, e.g., Python 3.9, that is compatible with the version of Ansible core on the control node,
  the python package prefix should instead specifiy the full Python level, e.g., python39 instead of python3, for installation.

- Additional dependencies on <b>IBM i Ansible server / control node</b>:
  * Ansible v2.15+ is not available as a prepackaged rpm for IBM i, yet can be installed with python pip. In the documentation site noted below under "Resources" there are detailed instructions provided in the "Getting Started" section for setting up Ansible with pip.
  * Ansible v2.16 and v2.17 cannot be used on an IBM i control node with the currently available IBM i Python packages.

## Known Issues

- Currently IBM i target nodes must use the Python 3.9 level and cannot use Python 3.13 (the IBM i control node is fine at Python 3.13). The IBM i open source stack no longer supports the ibm_db package that the IBM i collection has been using, so the collection will shift to using ODBC instead in the future (<a href="https://github.com/IBM/ansible-for-i/issues/229" target="_blank">Github issue 229</a>).

## Installation

Detailed installation instructions are available at the <a href="https://ibm.github.io/ansible-for-i/installation.html" target="_blank">github installation site</a>. This site provides information on installing the collection and any necessary prerequisites.

## Use Cases

The primary use cases for the collection include: command execution, fix management, security compliance checking, systems checking
(health, work management, etc.), and application deployment using a continuous integration and continuous deployment (CICD) model.
Several of these collection use cases provide a set of playbooks that can be customized by the user and are located
in the <a href="https://github.com/IBM/ansible-for-i/tree/devel/usecases" target="_blank">github usecases directory</a>.
There are other playbook examples in the <a href="https://github.com/IBM/ansible-for-i/tree/devel/playbooks" target="_blank">github playbooks directory</a>.

## Testing

The collection testing consists of the executing the Ansible sanity test, applying the Ansible lint tool on all published YAML source, and applying the set of <a href="https://github.com/IBM/ansible-for-i/tree/devel/tests/integration/targets" target="_blank">integration tests</a> for the collection modules and roles.
The collection testing environment uses Ansible core 2.16 and various Python levels such as 3.10, 3.11, and 3.12 with the control node and Python level 3.9 on the IBM i target node.

## Contributing

Users may contribute to the collection by creating a <a href="https://github.com/IBM/ansible-for-i/issues" target="_blank">github issue</a> for an enhancement or bug fix and then creating a <a href="https://github.com/IBM/ansible-for-i/pulls" target="_blank">github pull request</a> for evaluation.

## Support

Users can open an issue for any suspected bugs (or enhancement requests, etc.) as a <a href="https://github.com/IBM/ansible-for-i/issues" target="_blank">github issue</a>. Github issues are addressed based on potential severity/impact of a problem, frequency of a problem, along with development availability. Collection issues can also be raised to IBM by users with formal support.

## Release Notes and Roadmap

The release notes are in the github repository <a href="https://github.com/IBM/ansible-for-i/blob/devel/CHANGELOG.md" target="_blank">CHANGELOG.md</a> file.

## Related Information

For detail guides and reference, please visit the github <a href="https://ibm.github.io/ansible-for-i/index.html" target="_blank">Documentation</a> site.

## License Information
Some portions of this collection are licensed under GNU General Public License, Version 3.0, and other portions of this collection are licensed under Apache License, Version 2.0.
See individual files for applicable licenses.

## Copyright
© Copyright IBM Corporation 2020
