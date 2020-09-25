Overview for fix management use case
==============

The playbooks in this directory provides you the samples that you could directly use or do your own modifications.
Contents will be continuously added and enhanced.

Fix management system on IBM i can be used to manage fixs on IBM i system, including individual PTFs and PTF groups.

Introduction
--------------

Fix management system provides infrastructure to manage PTF repository

 - Automatically check and download PTF groups from IBM fix center to local fix repo
   * SNDPTFORD needs to be enabled
 - Repository is managed to store SAVFs and images downloaded from IBM fix center
 - Catalog(SQLite database tables) to manage PTF and Group information
   * What has been downloaded
   * Detail PTF list in a specific group
   * Support individual PTF and PTF group
 - Support manual put and update PTF into repository
 - Compare and send fixes from repository to target IBM i systems
 - Install PTF and Group to IBM i endpoint systems
 - Compare PTF difference between endpoint IBM i systems and repository

Playbook
--------------

## check_download_ptf_group

check_download_ptf_group playbook will get the latest PTF group information from IBM PSP website, and check if the latest PTF group already in repo server. If not, download the latest PTF group and write download information into download_status table and part of the PTF group information into ptf_group_image_info table in catalog.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `repo_server`         | str           | The fix repository IBM i server that can store and manage fixs.|
| `database`            | str           | The SQLite3 database that stores PTF and Group information.                             |
| `ptf_group`           | str           | The PTF group number which will be downloaded.   |

### Example

```
ansible-playbook /check_download_ptf_group.yml -e "{'repo_server': 'reposerver', 'database': '/ansible/repo.sqlite3', 'ptf_group': 'SF99704'}"
```

## check_download_individual_ptfs

check_download_individual_ptfs playbook will check if requested individual PTFs are already in catalog. If not, it will call download_individual_ptfs role to download non-existent ptfs and write ndividual PTFs' information into catalog.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `repo_server`         | str           | The fix repository IBM i server that can store and manage fixs.|
| `database`            | str           | The SQLite3 database that stores PTF and Group information.                             |
| `ptfs_list`           | list          | The to be downloaded PTFs' information list. ptf_id is required.  |

### Example

```
ansible-playbook /check_download_individual_ptfs.yml -e "{'repo_server': 'reposerver', 'database': '/ansible/repo.sqlite3', 'ptfs_list':[{'ptf_id':'SI67856'}, {'ptf_id':'SI69375'}, {'ptf_id':'SI73751'}]}"
```

## extract_ptf_group_info

extract_ptf_group_info playbook will call fix_repo_extract_ptf_group_info role to extract PTF group information and write into catalog.
Please call extract_ptf_group_info playbook after order becomes downloaded status.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `repo_server`         | str           | The fix repository IBM i server that can store and manage fixs.|
| `database`            | str           | The SQLite3 database that stores PTF and Group information.                             |
| `order_id`            | str           | The ibmi_download_fix module returned order_id.  |

### Example

```
ansible-playbook /extract_ptf_group_info.yml -e "{'repo_server': 'reposerver', 'order_id': '2025910369', 'database': '/ansible/repo.sqlite3'}"
```

## sync_apply_ptf_group

sync_apply_ptf_group playbook will get the PTF group information in catalog, then call sync_apply_ptf_group role to transfer the ptf group files to the target system. Then apply.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `repo_server`         | str           | The fix repository IBM i server that can store and manage fixs.|
| `target_system`       | str           | The target IBM i server that recieves and applies the PTF group.|
| `database`            | str           | The SQLite3 database that stores PTF and Group information.                             |
| `ptf_group`           | dict          | The to be applied PTF group' information. ptf_group_number and ptf_group_level are required.  |

### Example

```
ansible-playbook /sync_apply_ptf_group.yml -e "{'target_system': 'systemA', 'repo_server': 'reposerver', 'database': '/ansible/repo.sqlite3', 'ptf_group': {'ptf_group_number':'SF99740', 'ptf_group_level':'20121'}}"
```

## sync_apply_individual_ptfs

sync_apply_individual_ptfs playbook will get the individual ptfs' information in catalog. Then it will call check_ptf role to check which ptfs are not already applied or loaded on the target syste. After that, it will call sync_apply_individual_ptfs role to transfer the unloaded or unapplied ptfs to the target system. Finally load and apply.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `repo_server`         | str           | The fix repository IBM i server that can store and manage fixs.|
| `target_system`       | str           | The target IBM i server that recieves and applies the PTF group.|
| `database`            | str           | The SQLite3 database that stores PTF and Group information.                             |
| `ptf_group`           | dict          | The to be applied PTF group' information. ptf_group_number and ptf_group_level are required.  |

### Example

```
ansible-playbook /sync_apply_individual_ptfs.yml -e "{'target_system': 'systemA', 'repo_server': 'systemB', 'database': '/ansible/repo.sqlite3', 'ptfs_list': [{'ptf_id':'SI67856'}, {'ptf_id':'SI69375'}, {'ptf_id':'SI73751'}], 'apply_all_loaded_ptfs': false, 'temp_or_perm': '*TEMP', 'delayed_option': '*IMMDLY', 'auto_ipl': false}"
```

Reference
-------
For detail guides and reference, please visit the <a href="https://ibm.github.io/cloud-i-blog/archivers/2020-09-20-introduce_ansible_for_i_fix_management_function" target="_blank">Fix Management Documentation</a> site.
