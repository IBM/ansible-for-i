Overview for fix management use case
==============

The playbooks in this directory provides you the samples that you could directly use or do your own modifications.
Contents will be continuously added and enhanced.

Fix management system on IBM i can be used to manage PTFs on IBM i system, including individual PTFs and PTF groups.

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

Playbook
--------------

## check_download_ptf_group

check_download_ptf_group playbook will get the latest PTF group information from the IBM PSP website, and check if the latest PTF group already in the repository server. If not, download the latest PTF group and write download information into the download_status table and part of the PTF group information into the ptf_group_image_info table in the PTF database.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `ptf_group`           | str           | The PTF group number which will be downloaded.   |

### Example

```
ansible-playbook ./check_download_ptf_group.yml -e "{'ptf_group': 'SF99704'}"
```

## check_download_individual_ptfs

check_download_individual_ptfs playbook will check if requested individual PTFs are already in the PTF database. If not, it will call download_individual_ptfs role to download non-existent PTFs and write individual PTFs' information into the PTF database.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `ptfs_list`           | list          | The to be downloaded PTFs' ID list.  |

### Example

```
ansible-playbook ./check_download_individual_ptfs.yml -e "{'ptfs_list':['SI67856', 'SI69375', 'SI73751']}"
```

## extract_ptf_group_info

extract_ptf_group_info playbook will call fix_repo_extract_ptf_group_info role to extract PTF group information and write into the PTF database.
Please call extract_ptf_group_info playbook after the order status becomes DOWNLOADED.

#### Variables

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `order_id`            | str           | order_id returned from the ibmi_download_fix module.  |

### Example

```
ansible-playbook ./extract_ptf_group_info.yml -e "{'order_id': '2025910369'}"
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
| `repo_server`         | str           | The IBM i server where PTFs stored and managed.                    |
| `ptf_group`           | dict          | The information of the PTF groups to be synced and applied on the target. ptf_group_number and ptf_group_level are required.  |

### Example

```
ansible-playbook ./sync_apply_ptf_group.yml -e "{'repo_server': 'my.repo.server.com', 'ptf_group': {'ptf_group_number':'SF99740', 'ptf_group_level':'20121'}}"

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
| `repo_server`         | str           | The IBM i server where PTFs stored and managed.     |
| `ptfs_list`           | list          | The list of PTFs to be processed.  |

### Example

```
ansible-playbook ./sync_apply_individual_ptfs.yml -e "{'repo_server': 'my.repo.server.com', 'ptfs_list': ['SI67856', 'SI69375', 'SI73751'], 'apply_all_loaded_ptfs': false, 'temp_or_perm': '*TEMP', 'delayed_option': '*IMMDLY', 'auto_ipl': false}"

```

Reference
-------
For detail guides and reference, please visit the <a href="https://ibm.github.io/cloud-i-blog/archivers/2020-09-20-introduce_ansible_for_i_fix_management_function" target="_blank">Fix Management Documentation</a> site.
