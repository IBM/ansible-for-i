# enable-ansible-for-i

If your IBM i target system can connect to the internet, you can directly run the playbook `setup.yml`.

By running `setup.yml`, your IBM i system will be ready for being managed by Ansible for IBM i collections.

## What setup.yml installs

- **yum** (bootstrapped if not already present)
- **Python** interpreter (default: Python 3.13)
- **ibm-iaccess** package
- **python3.13-itoolkit** and **python3.13-pyodbc** (or the python39-prefixed equivalents when using Python 3.9)

## Basic usage

```bash
ansible-playbook -i hosts_ibmi.ini playbooks/enable-ansible-for-i/setup.yml
```

This installs **Python 3.13** by default.

## Selecting a Python version

The playbook exposes a single `python_level` variable that controls which Python version is installed.
Only one level is active at a time; selecting one automatically disables the other.

| `python_level` value | Python installed | Package prefix |
|---|---|---|
| `3.13` *(default)* | python3.13 | `python3.13-` |
| `3.9` | python39 | `python39-` |

Override `python_level` at runtime with the `-e` flag:

```bash
# Install Python 3.9 instead of the default 3.13
ansible-playbook -i hosts_ibmi.ini playbooks/enable-ansible-for-i/setup.yml -e python_level=3.9
```

## Prerequisites

- The IBM i target system must have network access to the IBM open-source package repositories.
- Licensed product **5770DG1** (IBM HTTP Server for i,) must be installed; the playbook will fail with a clear message if it is not.
- SSH must be enabled on the target IBM i system.
