<br>This folder is to store sample playbooks for IBM i and a sample inventory file named hosts_ibmi.ini. </br>

In all sample playbooks, the target hosts point to an inventory group named ibmi. Before you try those sample playbooks, you have to input information of your IBM i systems in [ibmi] section of your inventory file, which you create by yourself or just use the sample inventory file hosts_ibmi.ini in the folder.

## Variables of hosts_ibmi.ini

The following variables are set by the user:
* `your_ibm_ip` (str): IP or host name of your IBM i
* `your_user` (str): The user profile of the IBM i
* `your_host_password` (str): The password of the user profile. 

BTW, if the python version of your IBM i is python 3, please change the value of ansible_python_interpreter from “/QOpensys/pkgs/bin/python2” to “/QOpensys/pkgs/bin/python3"



