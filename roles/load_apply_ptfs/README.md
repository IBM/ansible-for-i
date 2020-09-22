load_apply_ptfs
=========

Call load_ptf role and apply_ptfs role to load and apply a list of individual ptfs, and retrun status.

Role Variables
--------------

| Variable              | Type          | Description                                                                    |
|-----------------------|---------------|--------------------------------------------------------------------------------|
| `required_ptf_list`   | list          | The ptfs' information list. ptf_id, product, file_name, file_path are required.|
| `remote_lib`          | str           | The remote lib stores ptfs' savf, default is QGPL.                             |
| `apply_all_loaded_ptf`| bool          | Used by apply_ptf role. Controls whether all loaded ptf will be applied. When the value is true, 'to_be_applied_list' will be ignored. Default value is false.    |
| `temp_or_perm`        | str           | Used by apply_ptf role. Controls whether the target PTFs will be permanent applied or temporary applied. Value can be  '*TEMP' or '*PERM'. Default value is '*TEMP'.                     |
| `delayed_option`      | str           | Used by apply_ptf role. Controls whether the PTF is delayed apply or not. Value can be '*YES', '*NO' or '*IMMDLY'. Default value is '*IMMDLY'.                     |
| `auto_ipl`            | bool          | Used by apply_ptf role. Controls whether an immediate reboot will be launched automatically if at least one ptf requests an IPL for permanent applied or temporary applied. Default value is false. |

Return Variables
--------------

| Variable              | Type          | Description                   |
|-----------------------|---------------|-------------------------------|
| `load_success_list`   | list          | The list of successful load.  |
| `load_fail_list`      | list          | The list of failed load.      |
| `apply_success_list`  | list          | The list of successful apply. |
| `apply_fail_list`     | list          | The list of failed apply.     |

Example Playbook
----------------
```
- name: Tranfer a list of individual ptfs to an ibm i system, then load and apply
  hosts: desthost

  vars:
    required_ptf_list:
      - {'ptf_id':'SI73543', 'product':'5770UME', 'file_name':'QSI73543.file', 'file_path': '/qsys.lib/qgpl.lib/QSI73543.FILE'}
      - {'ptf_id':'SI73430', 'product':'5733SC1', 'file_name':'QSI73430.file', 'file_path': '/qsys.lib/qgpl.lib/QSI73430.FILE'}
    temp_or_perm: '*PERM'
    delayed_option: '*IMMDLY'
    auto_ipl: False

  tasks:
    - name: Include sync_apply_single_ptf role to Load and apply a list of single ptfs, and retrun load and apply status.
      include_role:
        name: load_apply_ptfs
      register: load_apply_result
```

License
-------

Apache-2.0
