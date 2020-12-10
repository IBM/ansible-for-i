sync_apply_individual_ptfs
=========
Call ibmi_synchronize_files modules to transfer a list of exists ptfs to an ibm i system, then call load_apply_ptfs role to load
and apply ptfs. And return the status.

Role Variables
--------------

| Variable              | Type          | Description                                                                      |
|-----------------------|---------------|----------------------------------------------------------------------------------|
| `not_loaded_list`      | list          | The not loaded ptfs' information list. ptf_id, product, file_name and file_path are required.  |
| `already_loaded_list`    | list        | The already loaded ptfs' information list. ptf_id and product are required.  |
| `src_host`            | str           | The system that has the src ptf savfs, which will be transferred to the target system.|
| `dest`                | str           | The library that savfs would be transferred to. The default is "/qsys.lib/qgpl.lib".  |
| `apply_all_loaded_ptf`| bool          | Used by apply_ptf role. Used by apply_ptf role. Controls whether all loaded ptf will be applied. When the value is true, 'to_be_applied_list' will be ignored. The default value is True.    |
| `temp_or_perm`        | str           | Used by apply_ptf role. Controls whether the target PTFs will be permanent applied or temporary applied. Value can be  '*TEMP' or '*PERM'. Default value is '*TEMP'.                     |
| `delayed_option`      | str           | Used by apply_ptf role. Controls whether the PTF is delayed apply or not. Value can be '*YES', '*NO' or '*IMMDLY'. Default value is '*IMMDLY'.                      |
| `auto_ipl`            | bool          | Used by apply_ptf role. Controls whether an immediate reboot will be launched automatically if at least one ptf requests an IPL for permanent applied or temporary applied. The default value is false. |

Return Variables
--------------

| Variable              | Type          | Description                   |
|-----------------------|---------------|-------------------------------|
| `sync_success_list`   | list          | The list of the successful sync.  |
| `sync_fail_list`      | list          | The list of the failed sync.      |
| `load_success_list`   | list          | The list of the successful load.  |
| `load_fail_list`      | list          | The list of the failed load.      |
| `load_fail_dict`      | dict          | The dict of the failed load. The key is the ptf id, and the value is the ptf status.|
| `apply_fail_with_requisite_list`      | list          | The list of failed apply when to_be_applied_list is provided.                                        |
| `apply_fail_dict`      | dict          | The list of failed apply when to_be_applied_list is provided.                                        |
| `requisite_list`      | list          | The list of failed apply when to_be_applied_list is provided.                                        |
| `apply_success_list`   | list          | The list of successful apply when to_be_applied_list is provided and apply_all_loaded_ptfs set to True.   |
| `apply_fail_list`      | list          | The list of failed apply when to_be_applied_list is provided and apply_all_loaded_ptfs set to True.   |

Example Playbook
----------------
```
- name: Tranfer a list of individual ptfs to an ibm i system, then load and apply
  hosts: desthost

  vars:
    src_host: "srchost"
    not_loaded_list:
      - {'ptf_id':'SI73543', 'product':'5770UME', 'file_name':'QSI73543.file', 'file_path': '/qsys.lib/qgpl.lib/QSI73543.FILE'}
      - {'ptf_id':'SI73430', 'product':'5733SC1', 'file_name':'QSI73430.file', 'file_path': '/qsys.lib/qgpl.lib/QSI73430.FILE'}
    already_loaded_list:
      - {'ptf_id':'SI63556', 'product':'5770UME'}
    temp_or_perm: '*PERM'
    delayed_option: '*IMMDLY'
    auto_ipl: False

  tasks:
    - name: Include sync_apply_individual_ptfs role to transfer a list of individual ptfs to target ibm i, then load and apply
      include_role:
        name: sync_apply_individual_ptfs
```

License
-------

Apache-2.0
