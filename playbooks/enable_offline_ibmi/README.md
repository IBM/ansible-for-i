enable_offline_ibmi
=========
Online yum update doesn't work on 'offline' IBM i systems. This playbook sets up the required packages for Ansible on the system, such as yum, python, itoolkit, and pyodbc. An 'offline' IBM i means that the IBM i system cannot connect to the public network, for example, https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/repo/.

Pre-requisites:
-------------
<br>1. Create a directory on the Ansible server, for example, /tmp/ibmi-packages.</br>
<br>2. If yum is not installed on your IBM i systems, download these files and put them in the directory you just created:</br>
<br> bootstrap.sh
https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/bootstrap.sh
</br>
<br> bootstrap.tar.Z
https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/bootstrap.tar.Z
</br>
<br> python, libutil2, libncurses6, python-itoolkit, ibm-iaccess, python-pyodbc, update-alternatives, libreadline8
https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/repo/ppc64/
</br>
<br> python-six
https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/repo/noarch/
</br>

Variables
--------------
| Variable         | Type    | Description                                                                                      |
|------------------|---------|--------------------------------------------------------------------------------------------------|
| `package_path`   | str     | The directory containing the downloaded RPM packages, for example, `/tmp/ibmi-packages`.        |
| `python_level`   | str     | Python version to install. Accepted values: `3.13` (default) or `3.9`. Only one level is active at a time; selecting one automatically disables the other. |

### Python version and package prefix

| `python_level` value | Python installed | Package prefix |
|---|---|---|
| `3.13` *(default)* | python3.13 | `python3.13-` |
| `3.9` | python39 | `python39-` |

Example
----------------
```bash
# Default: installs Python 3.13
ansible-playbook -i path/to/inventory main.yml -e 'package_path=/tmp/ibmi-packages'

# Install Python 3.9 instead
ansible-playbook -i path/to/inventory main.yml -e 'package_path=/tmp/ibmi-packages' -e python_level=3.9
```

License
-------

Apache-2.0
