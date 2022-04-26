enable_offline_ibmi
=========
 So online yum update doesn't work on 'offline' IBM i systems. The playbook is to setup required packages by Ansible on the system, such as yum, python, itoolkit, ibmi-db. An 'Offline' IBM i means that the IBM i system can't connect to the public network, for example, https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/repo/.

Pre-requisites:
-------------
<br>1. Create a directory on the Ansible server, for example, /tmp/ibmi-packages.</br>
<br>2. If yum is not installed on you IBM i systems, download those files and put them in the directory you just created </br>
<br> bootstrap.sh
https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/bootstrap.sh
</br>
<br> bootstrap.tar.Z
https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/bootstrap.tar.Z
</br>
<br> python, libutil2, libncurses6, python-itoolkit, python-ibm_db, update-alternatives, libreadline8
https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/repo/ppc64/
</br>
<br> python-six
https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/repo/noarch/
</br>

Variables
--------------
| Variable              | Type          | Description                                      |
|-----------------------|---------------|--------------------------------------------------|
| `package_path`      | str          | The directory you just created, for example,  /tmp/ibmi-packages                  |
| `is_python39_to_be_installed`      | boolean          | Python 39 is going to be enabled by default. Specify it to false it you would like to enable python39.                |

Example 
----------------
```
ansible-playbook -i path/to/inventory main.yml -e 'package_path=/tmp/ibmi-packages'
ansible-playbook -i path/to/inventory main.yml -e "{'package_path':'/tmp/ibmi-packages', 'is_python39_to_be_installed':false}
```

License
-------

Apache-2.0
