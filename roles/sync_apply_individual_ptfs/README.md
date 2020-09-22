sync_apply_individual_ptfs
=========
Call ibmi_synchronize_files modules to tranfer a list of exists ptfs to an ibm i system, then call load_apply_ptfs role to load
and apply ptfs. And return the status.

Role Variables
--------------

| Variable              | Type          | Description                                                                      |
|-----------------------|---------------|----------------------------------------------------------------------------------|
| `ptfs_info_list`      | list          | The ptfs' information list. ptf_id, product, file_name and file_path are required.  |
| `src_host`            | str           | The system that has the src ptf savfs, which will be transferred to target system.|
| `dest`                | str           | The libray that savfs would be transferred to. Default is "/qsys.lib/qgpl.lib".  |
| `apply_all_loaded_ptf`| bool          | Used by apply_ptf role. Used by apply_ptf role. Controls whether all loaded ptf will be applied. When the value is true, 'to_be_applied_list' will be ignored. Default value is false.    |
| `to_be_applied_list`  | list          | ptfs list will be applied. ptf_id and product are required.           |
| `temp_or_perm`        | str           | Used by apply_ptf role. Controls whether the target PTFs will be permanent applied or temporary applied. Value can be  '*TEMP' or '*PERM'. Default value is '*TEMP'.                     |
| `delayed_option`      | str           | Used by apply_ptf role. Controls whether the PTF is delayed apply or not. Value can be '*YES', '*NO' or '*IMMDLY'. Default value is '*IMMDLY'.                      |
| `auto_ipl`            | bool          | Used by apply_ptf role. Controls whether an immediate reboot will be launched automatically if at least one ptf requests an IPL for permanent applied or temporary applied. Default value is false. |

Return Variables
--------------

| Variable              | Type          | Description                   |
|-----------------------|---------------|-------------------------------|
| `sync_success_list`   | list          | The list of successful sync.  |
| `sync_fail_list`      | list          | The list of failed sync.      |
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
    src_host: "srchost"
    ptfs_info_list:
      - {'ptf_id':'SI73543', 'product':'5770UME', 'file_name':'QSI73543.file', 'file_path': '/qsys.lib/qgpl.lib/QSI73543.FILE'}
      - {'ptf_id':'SI73430', 'product':'5733SC1', 'file_name':'QSI73430.file', 'file_path': '/qsys.lib/qgpl.lib/QSI73430.FILE'}
    temp_or_perm: '*PERM'
    delayed_option: '*IMMDLY'
    auto_ipl: False

  tasks:
    - name: Include sync_apply_individual_ptfs role to transfer a list of individual ptfs to target ibm i, then load and apply
      include_role:
        name: sync_apply_individual_ptfs
      register: sync_apply_result
```

License
-------

Apache-2.0
