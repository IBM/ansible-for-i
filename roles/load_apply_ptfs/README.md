load_apply_ptfs
=========

Call load_ptf role and apply_ptfs role to load and apply a list of individual ptfs, and return status.

Role Variables
--------------

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `to_be_loaded_ptf_list`   | list       | The not loaded ptfs' information list. ptf_id, product and file_name are required.|
| `remote_lib`          | str           | The remote lib stores ptfs' savf.  The default value is QGPL.                             |
| `loaded_list`              | list     | Already loaded but not applied ptfs' list. ptf_id and product are required.        |
| `apply_all_loaded_ptf`| bool          | Used by apply_ptf role. Controls whether all loaded ptf will be applied. When the value is true, 'to_be_applied_list' will be ignored. The default value is false.    |
| `temp_or_perm`        | str           | Used by apply_ptf role. Controls whether the target PTFs will be permanent applied or temporary applied. Value can be  '*TEMP' or '*PERM'. Default value is '*TEMP'.                     |
| `delayed_option`      | str           | Used by apply_ptf role. Controls whether the PTF is delayed apply or not. Value can be '*YES', '*NO' or '*IMMDLY'. Default value is '*IMMDLY'.                     |
| `auto_ipl`            | bool          | Used by apply_ptf role. Controls whether an immediate reboot will be launched automatically if at least one ptf requests an IPL for permanent applied or temporary applied. The default value is false. |

Return Variables
--------------

| Variable              | Type          | Description                   |
|-----------------------|---------------|-------------------------------|
| `load_success_list`   | list          | The list of the successful load.  |
| `load_fail_list`      | list          | The list of the failed load.      |
| `apply_success_list`  | list          | The list of the successful apply. |
| `apply_fail_list`     | list          | The list of the failed apply.     |

Example Playbook
----------------
```
- name: Load a list of individual ptfs on an ibm i system, then apply
  hosts: desthost

  vars:
    to_be_loaded_ptf_list:
      - {'ptf_id':'SI73543', 'product':'5770UME', 'file_name':'QSI73543.file'}
      - {'ptf_id':'SI73430', 'product':'5733SC1', 'file_name':'QSI73430.file'}
    loaded_list:
      - {'ptf_id':'SI63556', 'product':'5770UME'}
      - {'ptf_id':'SI71714', 'product':'5733SC1'}
    temp_or_perm: '*PERM'
    delayed_option: '*IMMDLY'
    auto_ipl: False

  tasks:
    - name: Include load_apply_ptfs role to Load and apply a list of single ptfs.
      include_role:
        name: load_apply_ptfs
      register: load_apply_result
```

License
-------

Apache-2.0
