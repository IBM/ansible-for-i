# Ansible-for-i


Ansible is a radically simple IT automation system. It handles configuration management, application deployment, cloud provisioning, ad-hoc task execution, network automation, and multi-node orchestration. Ansible makes complex changes like zero-downtime rolling updates with load balancers easy. 

IBM i systems can be managed nodes of Ansible. This project is to enrich IBM i support on Ansible, like providing more IBM i modules and examples to manage IBM i nodes. 

<b>How to enable ansible server and IBM i nodes? </b> <br>
1. Install ansible server. For example, run "yum install ansible" on a supported platform.
2. Clone this repository to your Ansible server.
3. Create your inventory file under examples/ibmi, an example can be found here "examples/ibmi/hosts_ibmi.ini"
4. Run "ansible-playbook -i your_inventory_file playbooks/enable-ansible-for-i/setup.yml"</br>

<b>Dependencies on IBM i node: </b>
1. 5733SC1 Base and Option 1
2. 5770DG1
3. Python
4. itoolkit
5. ibm_db

Note: 1) Use yum to install 3, 4, 5. About how to install yum on IBM i, refer to examples/ibmi/playbooks/ibmi-install-yum.yml.
2) Both python 2 and python 3 are supported. The python which is used by Ansible depends on value of  ansible_python_interpreter in the inventory file. For example, ansible_python_interpreter = "/QOpensys/pkgs/bin/python2" or ansible_python_interpreter = "/QOpensys/pkgs/bin/python3"
<b>License: </b><br>

GNU General Public License v3.0 or later.


