# power_ibmi
The IBM i collection includes modules. action plugins, sample playbooks to automate tasks on IBM i.


Ansible is a radically simple IT automation system. It handles configuration management, application deployment, cloud provisioning, ad-hoc task execution, network automation, and multi-node orchestration. Ansible makes complex changes like zero-downtime rolling updates with load balancers easy. 

IBM i systems can be managed nodes of Ansible. This project is to enrich IBM i support on Ansible, like providing more IBM i modules and examples to manage IBM i nodes. 

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

<b>How to install the collection before it gets to be published to galaxy webesite </b> <br>
1. Git clone the repostiory to local
2. Run "ansible-galaxy collection build ."
3. Run "ansible-galaxy collection install ibm-power_ibmi-x.y.z.tar.gz"
</br>

Note: replacing x.y.z with the current version

<b>How to install the collection after it gets to be published to galaxy website </b> <br>
1. Run "ansible-galaxy collection install ibm.power_ibmi"
</br>
