# IBM Power IBM i collection
The IBM Power IBM i collection, also represented as power_ibmi in this document, includes modules, action plugins, sample playbooks to automate tasks on IBM i, such as executing CL commands, running SQL statements, submitting jobs, managing fixes, etc.

<b>Getting Started Articles: </b> 

You may want to check out below articles first if you are new to Ansible for IBM i support. <br>
https://developer.ibm.com/linuxonpower/2020/05/01/ansible-automation-for-ibm-power-systems/  <br>
https://ibm.github.io/cloud-i-blog/

<b>Dependencies on IBM i node: </b>
1. 5733SC1 Base and Option 1
2. 5770DG1
3. Python3
4. python3-itoolkit
5. python3-ibm_db

Note: 
1) Use yum to install 3, 4, 5. About how to install yum on IBM i, refer to examples/ibmi/playbooks/ibmi-install-yum.yml.

<b>How to enable IBM i nodes? </b> <br>
1. Install ansible server. For example, run "pip install ansible" on a supported platform.
2. Git clone the repostiory to local
3. Create your inventory file under examples/ibmi, an example can be found here "examples/ibmi/hosts_ibmi.ini"
6. Run "ansible-playbook -i examples/ibmi/your_inventory_file examples/ibmi/playbooks/enable-ansible-for-i/enable-ibmi.yml"</br>

<b>How to install the collection before it gets to be published to galaxy webesite?</b> <br>
1. Git clone the repostiory to local
2. Run "ansible-galaxy collection build ."
3. Run "ansible-galaxy collection install ibm-power_ibmi-x.y.z.tar.gz" (Note: replacing x.y.z with the current version)

<b>How to install the collection after it gets to be published to galaxy website </b> <br>
Run "ansible-galaxy collection install ibm.power_ibmi"
</br>
</br>
<b>Copyright</b>
</br>
© Copyright IBM Corporation 2020
</br>

<b>License</b>
</br>
Some portions of this collection are licensed under [GNU General Public
License, Version 3.0](https://opensource.org/licenses/GPL-3.0), and
other portions of this collection are licensed under [Apache License,
Version 2.0](https://opensource.org/licenses/Apache-2.0).

See individual files for applicable licenses