Overview For Fix Management Use Case
==============

The playbooks in this directory provide you the samples that you could directly use or do your own modifications.
Contents will be continuously added and enhanced.
Fix management system on IBM i can be used to manage PTFs on the IBM i system, including individual PTFs and PTF groups.
Currently, Fix Management use case is divided into three different levels of solution.
 - Level 1
   * Level 1 is a semi-automated solution.
   * Repository server can be setup on IBM i or Linux server. 
   * Customer needs to manually download PTF or PTF group install files and upload to repository server. 
   * Playbooks can be used to auto-transfer and apply the PTF or PTF group on target IBM i system.
 - Level 1 + Sqlite3 DB
   * On the basis of level 1 solution, this solution adds Sqlite3 DB to repository server. 
   * Sqlite3 DB contains the PTF and PTF group catalog, which stores all the useful information, including PTF and PTF group number, level, downloaded date and file directory, etc.
 - Level 2
   * Level 2 is a fully-automated solution.
   * Repository server must be setup on IBM i server. 
   * Level 2 solution depends on IBM i SNDPTFORD function which can auto-download the PTF and PTF group install files from IBM Fix Central to repository server.
   * In order to make sure that SNDPTFORD works, repository server must have the ability to connect to the extranet.
   * Sqlite3 DB contains the PTF and PTF group catalog, which stores all the useful information, including PTF and PTF group number, level, downloaded date and file directory, etc.
   * Playbooks can be used to auto-transfer and apply the PTF or PTF group on target IBM i system.

Introduction
--------------

Fix management system provides an infrastructure to manage PTF repository

 - Automatically check and download PTF groups from IBM fix center to local fix repository
   * SNDPTFORD needs to be enabled
 - Repository is managed to store SAVFs and images downloaded from IBM fix center
 - Catalog(SQLite database tables) to manage PTF and Group information
   * What has been downloaded
   * Detail PTF list in a specific group
   * Support individual PTF and PTF group
 - Support manual put and update PTF into the repository
 - Compare and send fixes from the repository to target IBM i systems
 - Install PTF and Group to IBM i endpoint systems
 - Compare PTF difference between endpoint IBM i systems and repository

Dependency
--------------

 - Initialize Ansible dependencies on IBM i node. Refer to <a href="https://ibm.github.io/ansible-for-i/index.html" target="_blank">Power IBM i collection for Ansible</a>
 - Python3 paramiko package must be installed on the repository server.
 - Make sure ssh passwordless login works from the repository server to every target IBM i server.

 - For Level 1 + Sqlite3 DB solution:
   * Sqlite3 package must be installed on the repository server.

 - For Level 2 solution:
   * Sqlite3 package must be installed on the repository server.
   * Make sure SNDPTFORD works on the repository server. Refer to <a href="https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/rzaji/rzaji_setup.htm" target="_blank">Setting up a connection to IBM</a>

Playbook Overview
--------------
 - Level 1:
   * configure_passwordless_ssh_login.yml
   * copy_individual_ptf_to_repo.yml
   * copy_ptf_group_to_repo.yml
   * ipl_system_to_conduct_ipl_action_of_ptfs.yml
   * run_ARE_template.yml
   * sync_apply_individual_ptf_using_filedir.yml
   * sync_apply_individual_ptf_using_ptfinfo.yml
   * sync_apply_ptf_group_using_filedir.yml
   * sync_apply_ptf_group_using_ptfinfo.yml

 - Level 1 + Sqlite3 DB:
   * configure_passwordless_ssh_login.yml
   * copy_individual_ptf_to_repo.yml
   * copy_ptf_group_to_repo.yml
   * ipl_system_to_conduct_ipl_action_of_ptfs.yml
   * run_ARE_template.yml
   * sync_apply_individual_ptfs_lv1.yml
   * sync_apply_ptf_group_lv1.yml

 - Level 2:
   * configure_passwordless_ssh_login.yml
   * check_download_individual_ptfs.yml
   * check_download_ptf_group.yml 
   * check_ptf_group_order_status.yml
   * download_apply_individual_ptfs.yml
   * extract_ptf_group_info.yml
   * ibmi_fix_group_compare.yml
   * ibmi_fix_product_compare.yml
   * ipl_system_to_conduct_ipl_action_of_ptfs.yml
   * run_ARE_template.yml
   * sync_apply_individual_ptfs.yml
   * sync_apply_ptf_group.yml
   * sync_apply_ptf_group_networkinstall.yml
   * migrate_repo_server.yml

Playbook Detailed Introduction
--------------

## configure_passwordless_ssh_login

The playbook file is to provide an example about how to configure passwordless ssh login.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `key_path`         | str           | Specifies the path of the private rsa key, if the key doesn't the playbook creates one.   |
| `source_system`           | str     | Specifies the system whose public key is added to authorized_keys of target_system. After that 
whose user which is authorized by target_system can log in target_system via ssh without providing password.   |
| `target_system`           | str     | Specifies the system which performs as a server in futher ssh connection.   |

### Example

```
ansible-playbook ./configure_passwordless_ssh_login.yml -e  "{'source_system': 'reposerver', 'target_system': 'ibmi'}"
```

## copy_individual_ptf_to_repo

This playbook will copy individual ptf files on Ansible server to repository server, and create dir on repository server named after the ptf.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `repo_server`           | str     | The IBM i/Linux server stores PTFs and PTF groups.   |
| `ptf_number`           | str     | Specifies the PTF number which needs to be copied to repository server.   |
| `file_path_dir`         | str       | The directory of PTF files on repository server.   |

### Example

```
ansible-playbook ./copy_individual_ptf_to_repo.yml -e "{'repo_server': 'systemB', 'ptf_number': 'SI63556', 'file_path_dir': '/tmp/SI63556'}"
```

## copy_ptf_group_to_repo

This playbook will copy PTF Group files on Ansible server to repository server, and create dir on repository server named after the ptf group.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `repo_server`           | str     | The IBM i/Linux server stores PTFs and PTF groups.   |
| `ptf_group_number`           | str     | Specifies the PTF Group number which needs to be copied to repository server.   |
| `ptf_group_level`           | str     | Specifies the PTF Group level.   |
| `file_path_dir`         | str       | The directory of PTF Group files on repository server.   |

### Example

```
ansible-playbook ./copy_ptf_group_to_repo.yml -e "{'repo_server': 'systemB', 'ptf_group_number': 'SF99740', 'ptf_group_level': '12', 'file_path_dir': '/tmp/2343456'"
```

## ipl_system_to_conduct_ipl_action_of_ptfs

The playbook file is to provide an example about how to query all PTFs requring IPL to  be applied or removed, then IPL system per required.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `auto_ipl`           | bool     | Specifies if an IPL is launched automatically when there is/are PTF(s) requiring IPL to be applied or removed.   |
| `target_system`           | str     | Specifies the target IBM i system name which is defined in hosts.ini.   |

### Example

```
ansible-playbook ./ipl_system_to_conduct_ipl_action_of_ptfs.yml -e "{'target_system': 'systemA'}"
```

## sync_apply_individual_ptf_using_filedir

The playbook file is to provide an example about how to query all PTFs requring IPL to  be applied or removed, then IPL system per required.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `repo_server`           | str     | The IBM i/Linux server stores PTFs and PTF groups.    |
| `target_system`           | str     | The target IBM i server that receives and applies the PTFs.   |
| `delete`           | bool     | Specifies whether or not to delete the file install dir on target server after apply. The default value is true.   |

### Example

```
ansible-playbook ./sync_apply_individual_ptf_using_filedir.yml -e "{'target_system': 'systemA', 'repo_server': 'systemB', 'ptf_dir': '/tmp/SI63556', 'delete': true}"
```

## sync_apply_individual_ptf_using_ptfinfo

This playbook will transfer the ptf files to the target system, and apply ptf.
Before use this playbook, make sure you have used the copy_individual_ptf_to_repo.yml to transfer files to repository server, then the ptf dir on repository server should be formatted as ~/PTF/ptf_number.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `repo_server`           | str     | The IBM i/Linux server stores PTFs and PTF groups.    |
| `target_system`           | str     | The target IBM i server that receives and applies the PTFs.   |
| `ptf_number`           | str     | Specifies the PTF number which needs to be applied on target IBM i system.   |
| `delete`           | bool     | Specifies whether or not to delete the file install dir on target server after apply. The default value is true.   |

### Example

```
ansible-playbook ./sync_apply_individual_ptf_using_ptfinfo.yml -e "{'target_system': 'systemA', 'repo_server': 'systemB','ptf_number': 'SI69385', 'delete': true}"
```

## sync_apply_ptf_group_using_filedir

This playbook will transfer the PTF Group files to the target system according to the giving ptf group directory, and apply the ptf group.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `repo_server`           | str     | The IBM i/Linux server stores PTFs and PTF groups.    |
| `target_system`           | str     | The target IBM i server that receives and applies the PTF group.   |
| `ptf_group_dir`           | str     | The directory of PTF group files on repository server.  |
| `ptf_omit_list`           | list     | The list of PTFs which will be omitted. The elements of the list are dict. The key of the dict should be the product ID of the fix that is omitted.   |
| `delete`           | bool     | Specifies whether or not to delete the file install dir on target server after apply. The default value is true.   |

### Example

```
ansible-playbook /sync_apply_ptf_group_using_filedir.yml -e "{'target_system': 'systemA', 'repo_server': 'systemB', 'ptf_group_dir': '/tmp/SF99729_125', 'delete': true, 'ptf_omit_list': [{'5770SS1': 'SI78582'}, {'5770ss1': 'SI78544'}]}"
```

## sync_apply_ptf_group_using_ptfinfo

This playbook will transfer the ptf group files to the target system, and apply ptf group.
Only supports bin format ptf group files.
Before use this playbook, make sure you have used the copy_ptf_group_to_repo.yml to transfer files to repository server, then the ptf group dir on repository server should be formatted as ptf_group_number_ptf_group_level under ~/PTF folder.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `repo_server`           | str     | The IBM i/Linux server stores PTFs and PTF groups.    |
| `target_system`           | str     | The target IBM i server that receives and applies the PTF group.   |
| `ptf_group_number`           | str     | Specifies the PTF Group number which needs to be applied on target IBM i system.  |
| `ptf_group_level`           | str     | Specifies the PTF Group level.  |
| `ptf_omit_list`           | list     | The list of PTFs which will be omitted. The elements of the list are dict. The key of the dict should be the product ID of the fix that is omitted.   |
| `delete`           | bool     | Specifies whether or not to delete the file install dir on target server after apply. The default value is true.   |

### Example

```
ansible-playbook ./sync_apply_ptf_group_using_ptfinfo.yml -e "{'target_system': 'systemA', 'repo_server': 'systemB', 'ptf_group_number': 'SF99729', 'ptf_group_level': '125', 'delete': true, 'ptf_omit_list': [{'5770SS1': 'SI78582'}, {'5770ss1': 'SI78544'}]}"
```

## sync_apply_individual_ptfs_lv1

This playbook is used for 1st level solution. It will get the individual ptfs' information in catalog. Then call check_ptf role to check which ptfs are not already applied or loaded on the target syste. Then call sync_apply_individual_ptfs_lv1 role to transfer the unloaded or unapplied ptfs to the target system. Then load and apply.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `repo_server`         | str     | The IBM i/Linux server stores PTFs and PTF groups.    |
| `target_system`       | str     | The target IBM i server that receives and applies the PTF group.   |
| `ptfs_list`           | list     | Specifies the PTFs' list.  |
| `delete`              | bool     | Specifies whether or not to delete the file install dir on target server after apply. The default value is true.  |
| `image_root`          | str     | Specifies the image files' dir on the repo_server. This should be the root dir of all the image files.   |
| `apply_all_loaded_ptfs` | bool    | Controls whether all loaded ptf will be applied. The default value is true.   |
| `temp_or_perm`         | str    | Controls whether the target PTFs will be permanent applied or temporary applied. Value can be  '*TEMP' or '*PERM'. Default value is '*TEMP'.|
| `delayed_option`       | str    | Controls whether the PTF is delayed apply or not. Value can be '*YES', '*NO' or '*IMMDLY'. Default value is '*IMMDLY'.    |
| `auto_ipl`             | bool    | Controls whether an immediate reboot will be launched automatically if at least one ptf requests an IPL for permanent applied or temporary applied. The default value is false.   |

### Example

```
ansible-playbook ./sync_apply_individual_ptfs_lv1.yml -e "{'target_system': 'systemA', 'repo_server': 'systemB', 'image_root': '/home/test/PTF', 'ptfs_list': ['SI67856', 'SI69375', 'SI73751'], 'apply_all_loaded_ptfs': true, 'temp_or_perm': '*TEMP', 'delayed_option': '*IMMDLY', 'auto_ipl': false, 'delete': true}"
```

## sync_apply_ptf_group_lv1

This playbook is used for 1st level solution. It will get the PTF group information in catalog. Then call sync_apply_ptf_group role to transfer the PTF group files to the target system, and apply.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `repo_server`         | str     | The IBM i/Linux server stores PTFs and PTF groups.    |
| `target_system`       | str     | The target IBM i server that receives and applies the PTF group.   |
| `ptf_group`           | dict     | Specifies the PTF Group number which needs to be applied on target IBM i system. The input group level can be omitted. If level is omitted, the latest downloaded PTF group will be used.  |
| `delete`              | bool     | Specifies whether or not to delete the file install dir on target server after apply. The default value is true.  |
| `image_root`          | str     | Specifies the image files' dir on the repo_server. This should be the root dir of all the image files.   |
| `ptf_omit_list`           | list     | The list of PTFs which will be omitted. The elements of the list are dict. The key of the dict should be the product ID of the fix that is omitted.   |

### Example

```
ansible-playbook ./sync_apply_ptf_group_lv1.yml -e "{'target_system': 'systemA', 'repo_server': 'reposerver', 'ptf_group': {'group':'SF99876', 'level': 19}, 'image_root': '/home/test/PTF', 'delete': true, 'ptf_omit_list': [{'5770SS1': 'SI78582'}, {'5770ss1': 'SI78544'}]}"
```

## check_download_ptf_group

This playbook is used for 2st level solution. It will get the latest PTF group information from the IBM PSP website, and check if the latest PTF group already in the repository server. If not, download the latest PTF group and write download information into the download_status table and part of the PTF group information into the ptf_group_image_info table in the PTF database.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `repo_server`         | str           | The IBM i server which can use SNDPTFORD to download and store PTF and PTF group install files.   |
| `ptf_group`           | str           | The PTF group number which needs be checked and downloaded.   |

### Example

```
ansible-playbook ./check_download_ptf_group.yml -e "{'repo_server': 'reposerver', 'ptf_group': 'SF99704'}"
```

## check_download_individual_ptfs

This playbook is used for 2st level solution. It will check if requested individual PTFs are already in the PTF database. If not, it will call download_individual_ptfs role to download non-existent PTFs and write individual PTFs' information into the PTF database.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `repo_server`         | str           | The IBM i server which can use SNDPTFORD to download and store PTF and PTF group install files.  |
| `ptfs_list`           | list          | The PTF number list which needs to be checked and downloaded.  |

### Example

```
ansible-playbook ./check_download_individual_ptfs.yml -e "{'repo_server': 'reposerver'，'ptfs_list':['SI67856', 'SI69375', 'SI73751']}"
```

## check_ptf_group_order_status

The playbook is to provide an example about how to check PTF group order status since the downloading may take several minutes to hours depends on the size of the package and the network condition. Waiting until the downloading completes may not always be a wise option. This playbook can be used as a scheduler job in your system, check the downloading status and update them as needed.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `repo_server`         | str           | The IBM i server which can use SNDPTFORD to download and store PTF and PTF group install files.  |

### Example

```
ansible-playbook ./check_ptf_group_order_status.yml -e "{'repo_server': 'reposerver'}"
```

## extract_ptf_group_info

extract_ptf_group_info playbook will call fix_repo_extract_ptf_group_info role to extract PTF group information and write into the PTF database.
Please call extract_ptf_group_info playbook after the order status becomes DOWNLOADED.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `repo_server`         | str           | The IBM i server which can use SNDPTFORD to download and store PTF and PTF group install files.   |
| `order_id`            | str           | order_id returned from the ibmi_download_fix module.  |

### Example

```
ansible-playbook ./extract_ptf_group_info.yml -e "{'repo_server': 'reposerver', 'order_id': '2025910369'}"
```

## sync_apply_ptf_group

```
sync_apply_ptf_group playbook does the following things:
  1. Get the PTF group information in the PTF database
  2. Call sync_apply_ptf_group role to transfer the PTF group files to the target system.
  3. Apply on the target.
```

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `target_system`       | str           | The target IBM i server that receives and applies the PTF groups.|
| `repo_server`         | str           | The IBM i server which can use SNDPTFORD to download PTF and PTF group, and stores PTFs and PTF groups.   |
| `ptf_group`           | dict          | The information of the PTF groups to be synced and applied on the target. ptf_group_number and ptf_group_level are required.  |
| `delete`              | bool     | Specifies whether or not to delete the file install dir on target server after apply. The default value is true.  |
| `ptf_omit_list`           | list     | The list of PTFs which will be omitted. The elements of the list are dict. The key of the dict should be the product ID of the fix that is omitted.   |

### Example

```
ansible-playbook ./sync_apply_ptf_group.yml -e "{'target_system': 'systemA', 'repo_server': 'reposerver', 'ptf_group': {'ptf_group_number':'SF99740', 'ptf_group_level':'20121'}, 'delete': true, 'ptf_omit_list': [{'5770SS1': 'SI78582'}, {'5770ss1': 'SI78544'}]}"
```

## sync_apply_individual_ptfs
```
sync_apply_individual_ptfs playbook does the following:
  1.  Get the individual PTFs' information from the PTF repository server.
  2.  Call check_ptf role to check which PTFs are not already applied or loaded on the target system.
  3.  Call sync_apply_individual_ptfs role to transfer the unloaded or unapplied PTFs to the target system.
  4.  Load and apply the PTFs on the target.
```
#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `target_system`       | str           | The target IBM i server that receives and applies the PTFs.|
| `repo_server`         | str           | The IBM i server which can use SNDPTFORD to download and store PTF and PTF group install files.     |
| `ptfs_list`           | list          | The list of PTFs to be processed.  |
| `apply_all_loaded_ptf`| bool          | Used by apply_ptf role. Controls whether all loaded ptf will be applied. When the value is true, 'to_be_applied_list' will be ignored. The default value is True.    |
| `temp_or_perm`        | str           | Used by apply_ptf role. Controls whether the target PTFs will be permanent applied or temporary applied. Value can be  '*TEMP' or '*PERM'. Default value is '*TEMP'.                     |
| `delayed_option`      | str           | Used by apply_ptf role. Controls whether the PTF is delayed apply or not. Value can be '*YES', '*NO' or '*IMMDLY'. Default value is '*IMMDLY'.                      |
| `auto_ipl`            | bool          | Used by apply_ptf role. Controls whether an immediate reboot will be launched automatically if at least one ptf requests an IPL for permanent applied or temporary applied. The default value is false. |

### Example

```
ansible-playbook ./sync_apply_individual_ptfs.yml -e "{'target_system': 'systemA', 'repo_server': 'systemB', 'ptfs_list': ['SI67856', 'SI69375', 'SI73751'], 'apply_all_loaded_ptfs': false, 'temp_or_perm': '*TEMP', 'delayed_option': '*IMMDLY', 'auto_ipl': false, 'delete': true}"
```

## download_apply_individual_ptfs
```
This playbook will Check if requested individual PTFs are already in catalog. If not, will download non-existent PTFs and write information into catalog. After that, will transfer savfs to target server, then load and apply PTFs.
```
#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `target_system`       | str           | The target IBM i server that receives and applies the PTFs.|
| `repo_server`| str          | The IBM i server which can use SNDPTFORD to download and store PTF and PTF group install files.      |
| `ptfs_list`| list          | The PTF number list which needs to be applied.     |

### Example

```
ansible-playbook ./download_apply_individual_ptfs.yml -e "{'target_system': 'systemA', 'repo_server': 'reposerver', 'ptfs_list': ['SI67856', 'SI69375', 'SI73751']}"
```

## ibmi_fix_group_compare
```
The sample file is to provide an example about how to compare the ptf groups between repository server and IBM i.
```
#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `target_system`       | str           | The target IBM i server which needs to be compared with repository server.     |
| `repo_server`| str          | The IBM i server which can use SNDPTFORD to download and store PTF and PTF group install files.      |
| `group_list`| list          | The PTF group list.     |

### Example

```
ansible-playbook ./ibmi_fix_group_compare.yml -e "{'group_list':['SF99xxx','SF99yyy'], 'target_system': 'target', 'repo_server': 'reposerver'}"
```

## ibmi_fix_product_compare
```
The sample file is to provide an example about how to compare the single ptf by product between repository server and IBM i.
```
#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `target_system`       | str           | The target IBM i server which needs to be compared with repository server.     |
| `repo_server`| str          | The IBM i server which can use SNDPTFORD to download and store PTF and PTF group install files.      |
| `product`| str          | Specifies the PTFs' product which needs to be compared.     |

### Example

```
ansible-playbook ./ibmi_fix_product_compare.yml -e "{'product': '5770SS1', 'repo_server': 'reposerver', 'target_system':'target'}"
```

## sync_apply_ptf_group_networkinstall
```
This playbook is used for 2nd level solution. It will get the PTF group information in catalog. Then call sync_apply_ptf_group_networkinstall role to install PTF group on the target system.
sync_apply_ptf_group_networkinstall role will setup network install env on repository server and use network install mechanism to install the PTF group on the target system.
```

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `target_system`       | str           | The target IBM i server that receives and applies the PTF groups.|
| `repo_server`         | str           | The IBM i server which can use SNDPTFORD to download PTF and PTF group, and stores PTFs and PTF groups.   |
| `ptf_group`           | dict          | The information of the PTF groups to be synced and applied on the target. ptf_group_number and ptf_group_level are required.  |
| `delete`              | bool     | Specifies whether or not to delete the file install dir on target server after apply. The default value is true.  |
| `ptf_omit_list`           | list     | The list of PTFs which will be omitted. The elements of the list are dict. The key of the dict should be the product ID of the fix that is omitted.   |

### Example

```
ansible-playbook ./sync_apply_ptf_group_networkinstall.yml -e "{'target_system': 'systemA', 'repo_server': 'reposerver', 'ptf_group': {'ptf_group_number':'SF99740', 'ptf_group_level':'20121'}, 'ptf_omit_list': [{'5770SS1': 'SI78582'}, {'5770ss1': 'SI78544'}]}"
```

## run_ARE_template
```
run_ARE_template playbook does the following:
  1.  Send ARE template file to the clients.
  2.  Run ARE template on the clients and print the content of the summary ARE result file. 5733ARE should be installed on the clients.
  3.  Transfer all the ARE results files back to the server.
```
#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `ARE_clients`       | str             | The target IBM i clients that receive ARE template and run it.|
| `template_server`       | str           | The target IBM i server that keep ARE template and receive ARE results from the clients.|
| `template_name`| str          | The template name on the server, i.e /tmp/PTF_SI71234.jar     |
| `template_dir_client`| str          | The directory on the client where ARE template will be located. The default value is '/etc/ibmi_ansible/fix_management/ARE/templates'.     |
| `ARE_results_dir_client`| str          | The directory on the client where ARE results files will be located. The default value is '/etc/ibmi_ansible/fix_management/ARE/results'.     |
| `ARE_results_name_client`| str          | The file name of ARE results on the client. The default value is the template name plus '.out'. For example, if the template name is 'SI71234.jar', the file name of ARE results will be 'SI71234.out'.    |
| `ARE_results_dir_server`| str          | The directory on the server where ARE results files will be located.    |
| `remove_ARE_template_client`| bool          | Whether ARE template file on the client will be removed after ARE results files are transferred to the server. The default value is true.   |

### Example

```
ansible-playbook ./run_ARE_template.yml -e "{'ARE_clients': 'systemA', 'template_server': 'templateserver', 'template_name': '/tmp/PTF_SI71234.jar', 'ARE_results_dir_on_server': '/tmp/results'}"
```

## migrate_repo_server
```
The IBM i system where the repository server is located should be at the higest OS level. This playbook is used for 2st level solution. It will package the repository server DB and files, then tranfer them to another IBM i system. Then setup the new repository enviornment.
```

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `target_system`       | str           | Specifies the new IBM i system which you want to migrate the repository server to.|
| `original_system`         | str           | Specifies the original repository server.   |
| `original_dir`           | str          | Specifies the repo.sqlite3 DB dir on the original IBM i system, the default value is /etc/ibmi_ansible/fix_management.  |
| `target_dir`              | str     | Specifies the repo.sqlite3 DB dir on the target IBM i system, the default value is /etc/ibmi_ansible/fix_management.  |

### Example

```
ansible-playbook ./migrate_repo_server.yml -e "{'target_system': 'systemA', 'original_system': 'systemB', 'repo_dir': '/etc/ibmi_ansible/fix_management', 'target_dir': '/etc/ibmi_ansible/fix_management'}"
```

License
-----------------------------------------

Apache-2.0


Reference
-------
For detail guides and reference, please visit the <a href="https://ibm.github.io/cloud-i-blog/archivers/2020-09-20-introduce_ansible_for_i_fix_management_function" target="_blank">Fix Management Documentation</a> site.
