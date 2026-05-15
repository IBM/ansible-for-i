sync_apply_individual_ptfs_local
=========
Call ibmi_copy and ibmi_synchronize_files modules to transfer a list of PTFs and their coverletters to an IBM i system,
then call load_apply_ptfs role to load and apply PTFs and return the status.
This role assumes the PTF files reside on the local node / Ansible control node.

Unloaded PTFs to apply are specified as dict entries in the not loaded list with the keys
- ptf_id
- product
- file_name (refers to save file which should be defined as "Q<ptf_id>.FILE).
- file_path (directory where the save file and cover letter are both located)
The cover letter file should be defined as 'Q<ptf_id>.MBR'.

Already loaded PTFs to apply are specified as dict entries in the already loaded list with the keys:
- ptf_id
- product

The download_list returned by the module ibmi_download_fix_from_cloud can be used to directly populate the not loaded list.

Role Variables
--------------

| Variable                                           | Type          | Description                                                                      |
|----------------------------------------------------|---------------|----------------------------------------------------------------------------------|
| `sync_apply_individual_ptfs_local_not_loaded_list`       | list          | The not loaded ptfs' information list. ptf_id, product, file_name and file_path are required.  |
| `sync_apply_individual_ptfs_local_already_loaded_list`   | list          | The already loaded ptfs' information list. ptf_id and product are required.  |
| `sync_apply_individual_ptfs_local_dest`                  | str           | The library that savfs would be transferred to. The default is "/qsys.lib/qgpl.lib".  |
| `sync_apply_individual_ptfs_local_delete`                | bool          | Whether or not to delete the PTF install savf after apply. The default is True.  |
| `sync_apply_individual_ptfs_local_apply_all_loaded_ptf`  | bool          | Used by apply_ptf role. Used by apply_ptf role. Controls whether all loaded ptf will be applied. When the value is true, 'to_be_applied_list' will be ignored. The default value is True.    |
| `sync_apply_individual_ptfs_local_temp_or_perm`          | str           | Used by apply_ptf role. Controls whether the target PTFs will be permanent applied or temporary applied. Value can be  '*TEMP' or '*PERM'. Default value is '*TEMP'.                     |
| `sync_apply_individual_ptfs_local_delayed_option`        | str           | Used by apply_ptf role. Controls whether the PTF is delayed apply or not. Value can be '*YES', '*NO' or '*IMMDLY'. Default value is '*IMMDLY'.                      |
| `sync_apply_individual_ptfs_local_auto_ipl`              | bool          | Used by apply_ptf role. Controls whether an immediate reboot will be launched automatically if at least one ptf requests an IPL for permanent applied or temporary applied. The default value is false. |

Return Variables
--------------

| Variable                                                     | Type          | Description                   |
|--------------------------------------------------------------|---------------|-------------------------------|
| `sync_apply_individual_ptfs_local_sync_success_list`   | list          | The list of the successful sync.  |
| `sync_apply_individual_ptfs_local_sync_fail_list`      | list          | The list of the failed sync.      |
| `sync_apply_individual_ptfs_local_load_success_list`   | list          | The list of the successful load.  |
| `sync_apply_individual_ptfs_local_load_fail_list`      | list          | The list of the failed load.      |
| `sync_apply_individual_ptfs_local_load_fail_dict`      | dict          | The dict of the failed load. The key is the ptf id, and the value is the ptf status.|
| `sync_apply_individual_ptfs_local_apply_fail_with_requisite_list`      | list          | The list of failed apply when to_be_applied_list is provided.                                        |
| `sync_apply_individual_ptfs_local_apply_fail_dict`     | dict          | The list of failed apply when to_be_applied_list is provided.                                        |
| `sync_apply_individual_ptfs_local_requisite_list`      | list          | The list of failed apply when to_be_applied_list is provided.                                        |
| `sync_apply_individual_ptfs_local_apply_success_list`   | list          | The list of successful apply when to_be_applied_list is provided and sync_apply_individual_ptfs_local_apply_all_loaded_ptf set to True.   |
| `sync_apply_individual_ptfs_local_apply_fail_list`      | list          | The list of failed apply when to_be_applied_list is provided and sync_apply_individual_ptfs_local_apply_all_loaded_ptf set to True.   |

Example Playbook
----------------
```
- name: Tranfer a list of individual ptfs to an ibm i system, then load and apply
  hosts: all

  vars:
    sync_apply_individual_ptfs_local_not_loaded_list:
      - {'ptf_id':'SI73543', 'product':'5770UME', 'file_name':'QSI73543.FILE', 'file_path': '/home/ansible/ptf/SI73543'}
      - {'ptf_id':'SI73430', 'product':'5733SC1', 'file_name':'QSI73430.FILE', 'file_path': '/home/ansible/ptf/SI73430'}
    sync_apply_individual_ptfs_local_already_loaded_list:
      - {'ptf_id':'SI63556', 'product':'5770UME'}
    sync_apply_individual_ptfs_local_temp_or_perm: '*PERM'
    sync_apply_individual_ptfs_local_delayed_option: '*IMMDLY'
    sync_apply_individual_ptfs_local_auto_ipl: False

  tasks:
    - name: Include sync_apply_individual_ptfs_local role to transfer a list of individual ptfs to target ibm i, then load and apply
      include_role:
        name: sync_apply_individual_ptfs_local
```

License
-------

Apache-2.0
