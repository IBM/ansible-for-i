# Ansible-for-i


Ansible is a radically simple IT automation system. It handles configuration management, application deployment, cloud provisioning, ad-hoc task execution, network automation, and multi-node orchestration. Ansible makes complex changes like zero-downtime rolling updates with load balancers easy. 

IBM i systems can be managed nodes of Ansible. This project is to enrich IBM i support on Ansible, like providing more IBM i modules and examples to manage IBM i nodes. 

<b>Dependencies on IBM i node: </b>
1. 5733SC1 Base and Option 1
2. 5770DG1
3. Python
4. python itoolkit
5. python ibm_db

Note: 1) Use yum to install 3, 4, 5. About how to install yum on IBM i, refer to examples/ibmi/playbooks/ibmi-install-yum.yml.
2) Both python 2 and python 3 are supported. The python which is used by Ansible depends on value of  ansible_python_interpreter in the inventory file. For example, ansible_python_interpreter = "/QOpensys/pkgs/bin/python2" or ansible_python_interpreter = "/QOpensys/pkgs/bin/python3"

<b>How to enable ansible server and IBM i nodes? </b> <br>
1. Install ansible server. For example, run "yum install ansible" on a supported platform.
2. Clone this repository to your Ansible server.
3. Create your inventory file under examples/ibmi, an example can be found here "examples/ibmi/hosts_ibmi.ini"
4. Run "ansible-playbook -i your_inventory_file playbooks/enable-ansible-for-i/setup.yml"</br>

<b>Manage IBM i nodes by Ansible Tower? </b> <br>
1. Create your repository to fork this repository.
2. Create your playbook in the root directory, for example, the same directory of ibmi-try-tower-structure.yml
3. Create Project in Ansible Tower to point to your repository.
4. Create job template to run your own playbook

Note, you can create new pull request to merge the changes in this repository into yours.

<b>Directory structure: </b>

```
├── action_plugins - Only applicable to Ansible tower. In where copies of lib/ansible/plugins/action/ are kept.
├── examples - Ansible playbook examples.
├── lib - Source code of IBM i new modules and plugins. Copy the folder to the module path on ansible server.
├── library - Only applicable to Ansible tower. In where copies of lib/ansible/modules/ibmi/ are kept. 
├── module_utils - Only applicable to Ansible tower. In where copies of lib/ansible/module_utils/ are kept.  
├── test - Integration test code of IBM i new modules and plugins.
├── ibmi_try_tower_structure.yml. Only applicable to Ansible tower. 
```

<b>IBM i Module Index:</b><br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_at.py">ibmi_at</a><br>
Schedule a batch job on a remote IBMi node.<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_cl_command.py">ibmi_cl_command</a><br>
Executes a CL command.<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_copy.py">ibmi_copy</a><br>
Copy a save file from local to a remote IBMi node.<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_display_subsystem.py">ibmi_display_subsystem</a><br>
Display all currently active subsystems or currently active jobs in a subsystem.<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_end_subsystem.py">ibmi_end_subsystem</a><br>
End a subsystem.<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_fetch.py">ibmi_fetch</a><br>
Fetch objects or a library from a remote IBMi node and store on local.<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_install_product_from_savf.py">ibmi_install_product_from_savf</a><br>
Install the the licensed program(product) from a save file.<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_lib_restore.py">ibmi_lib_restore</a><br>
Restore one library on a remote IBMi node.<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_lib_save.py">ibmi_lib_save</a><br>
Save one libary on a remote IBMi node.<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_object_authority.py">ibmi_object_authority</a><br>
Grant, Revoke and Display the Object Authority.<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_object_restore.py">ibmi_object_restore</a><br>
Restore one or more objects on a remote IBMi node.<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_object_save.py">ibmi_object_save</a><br>
Save one or more objects on a remote IBMi node.<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_reboot.py">ibmi_reboot</a><br>
Reboot IBMi machine.<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_save_product_to_savf.py">ibmi_save_product_to_savf</a><br>
Save the the licensed program(product) to a save file.<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_script.py">ibmi_script</a><br>
Execute a local cl/sql script file on a remote ibm i node.<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_script_execute.py">ibmi_script_execute</a><br>
Execute a cl/sql script file on a remote ibm i node.<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_sql_execute.py">ibmi_sql_execute</a><br>
Executes a SQL non-DQL(Data Query Language) statement.<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_sql_query.py">ibmi_sql_query</a><br>
Executes a SQL DQL(Data Query Language) statement.<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_start_subsystem.py">ibmi_start_subsystem</a><br>
Start a subsystem.<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_sync.py">ibmi_sync</a><br>
Synchronize a save file from current ibm i node A to another ibm i node B.<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_synchronize.py">ibmi_synchronize</a><br>
Synchronize a save file from ibm i node A to another ibm i node B.<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_uninstall_product.py">ibmi_uninstall_product</a><br>
Delete the objects that make up the licensed program(product).<br>
<a href="https://github.ibm.com/IBMi-Cloud/ansible-for-i-development/blob/master/lib/ansible/modules/ibmi/ibmi_user_and_group.py">ibmi_user_and_group</a><br>
Create, Change and Display a user(or group) profile.<br>

<b>License: </b><br>

GNU General Public License v3.0 or later.


