Overview for fix management use case
==============

The playbooks in this directory provide you the samples that you could directly use or do your own modifications.
Contents will be continuously added and enhanced.

Fix management system on IBM i can be used to manage PTFs on the IBM i system, including individual PTFs and PTF groups.

Introduction
--------------

Fix management system provides an infrastructure to manage PTF repository

 - Automatically check and download PTF groups from IBM fix center to local fix repo
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
 - Sqlite3 package must be installed on the repository server.
 - Make sure ssh passwordless login works from the repository server to every target IBM i server.
 - Make sure SNDPTFORD works on the repository server. Refer to <a href="https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/rzaji/rzaji_setup.htm" target="_blank">Setting up a connection to IBM</a>

Playbook
--------------

## check_download_ptf_group

check_download_ptf_group playbook will get the latest PTF group information from the IBM PSP website, and check if the latest PTF group already in the repository server. If not, download the latest PTF group and write download information into the download_status table and part of the PTF group information into the ptf_group_image_info table in the PTF database.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `repo_server`         | str           | The IBM i server which can use SNDPTFORD to download PTF and PTF group, and stores PTFs and PTF groups.   |
| `ptf_group`           | str           | The PTF group number which will be downloaded.   |

### Example

```
ansible-playbook ./check_download_ptf_group.yml -e "{'repo_server': 'reposerver', 'ptf_group': 'SF99704'}"
```

## check_download_individual_ptfs

check_download_individual_ptfs playbook will check if requested individual PTFs are already in the PTF database. If not, it will call download_individual_ptfs role to download non-existent PTFs and write individual PTFs' information into the PTF database.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `repo_server`         | str           | The IBM i server which can use SNDPTFORD to download PTF and PTF group, and stores PTFs and PTF groups.   |
| `ptfs_list`           | list          | The to be downloaded PTFs' ID list.  |

### Example

```
ansible-playbook ./check_download_individual_ptfs.yml -e "{'repo_server': 'reposerver'，'ptfs_list':['SI67856', 'SI69375', 'SI73751']}"
```

## extract_ptf_group_info

extract_ptf_group_info playbook will call fix_repo_extract_ptf_group_info role to extract PTF group information and write into the PTF database.
Please call extract_ptf_group_info playbook after the order status becomes DOWNLOADED.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `repo_server`         | str           | The IBM i server which can use SNDPTFORD to download PTF and PTF group, and stores PTFs and PTF groups.   |
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

### Example

```
ansible-playbook ./sync_apply_ptf_group.yml -e "{'target_system': 'systemA', 'repo_server': 'reposerver', 'ptf_group': {'ptf_group_number':'SF99740', 'ptf_group_level':'20121'}}"
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
| `repo_server`         | str           | The IBM i server which can use SNDPTFORD to download PTF and PTF group, and stores PTFs and PTF groups.     |
| `ptfs_list`           | list          | The list of PTFs to be processed.  |
| `apply_all_loaded_ptf`| bool          | Used by apply_ptf role. Used by apply_ptf role. Controls whether all loaded ptf will be applied. When the value is true, 'to_be_applied_list' will be ignored. The default value is True.    |
| `temp_or_perm`        | str           | Used by apply_ptf role. Controls whether the target PTFs will be permanent applied or temporary applied. Value can be  '*TEMP' or '*PERM'. Default value is '*TEMP'.                     |
| `delayed_option`      | str           | Used by apply_ptf role. Controls whether the PTF is delayed apply or not. Value can be '*YES', '*NO' or '*IMMDLY'. Default value is '*IMMDLY'.                      |
| `auto_ipl`            | bool          | Used by apply_ptf role. Controls whether an immediate reboot will be launched automatically if at least one ptf requests an IPL for permanent applied or temporary applied. The default value is false. |

### Example

```
ansible-playbook ./sync_apply_individual_ptfs.yml -e "{'target_system': 'systemA', 'repo_server': 'my.repo.server.com', 'ptfs_list': ['SI67856', 'SI69375', 'SI73751'], 'apply_all_loaded_ptfs': false, 'temp_or_perm': '*TEMP', 'delayed_option': '*IMMDLY', 'auto_ipl': false}"
```

## download_apply_individual_ptfs
```
download_apply_individual_ptfs playbook does the following:
  1.  Check if requested individual PTFs are already in the catalog. If not, will download non-existent PTFs and write information into the catalog.
  2.  Transfer savfs to the target server.
  3.  Load and apply PTFs.
```
#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `target_system`       | str           | The target IBM i server that receives and applies the PTFs.|
| `repo_server`| str          | The IBM i server which can use SNDPTFORD to download PTF and PTF group, and stores PTFs and PTF groups.      |
| `ptfs_list_parm`| list          | The list of PTFs that need to be applied.     |

### Example

```
ansible-playbook /check_download_individual_ptfs.yml -e "{'target_system': 'systemA', 'repo_server': 'reposerver', 'ptfs_list': ['SI67856', 'SI69375', 'SI73751']}"
```

Reference
-------
For detail guides and reference, please visit the <a href="https://ibm.github.io/cloud-i-blog/archivers/2020-09-20-introduce_ansible_for_i_fix_management_function" target="_blank">Fix Management Documentation</a> site.
