# Ansible-for-i


Ansible is a radically simple IT automation system. It handles configuration management, application deployment, cloud provisioning, ad-hoc task execution, network automation, and multi-node orchestration. Ansible makes complex changes like zero-downtime rolling updates with load balancers easy. 

IBM i systems can be managed nodes of Ansible. This project is to enrich IBM i support on Ansible, like providing more IBM i modules and examples to manage IBM i nodes. 

<b>How to setup IBM i modules on Ansible server: </b> <br>

Copy the folder lib/ansible/modules/ibmi to the modules path of the Ansible server, for example, /usr/lib/python2.7/site-packages/ansible/modules.

<b>Dependencies on IBM i node: </b>
1. 5733SC1 Base and Option 1
2. 5770DG1
3. Python
4. itoolkit
5. ibm_db
Note: Use yum to install 3, 4, 5. About how to install yum on IBM i, refer to examples/ibmi/playbooks/ibmi-install-yum.yml.

<b>License: </b><br>

GNU General Public License v3.0 or later.


