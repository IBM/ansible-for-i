sync_apply_individual_ptfs_lv1
=========
Call ibmi_synchronize_files modules to transfer a list of exists ptfs install files to an ibm i system(~/PTF/singleptf/), then call ibmi_fix and ibmi_fix_imgclg module to load and apply ptfs. And return the status. This role is only used for LV1 solution.

Role Variables
--------------

| Variable              | Type          | Description                                                                      |
|-----------------------|---------------|----------------------------------------------------------------------------------|
| `not_loaded_list`      | list          | The not loaded ptfs' information list. ptf_id, product, file_name and file_path are required.  |
| `already_loaded_list`    | list        | The already loaded ptfs' information list. ptf_id and product are required.  |
| `src_host`            | str           | The system that has the ptf install files, which will be transferred to the target system.|
| `delete`              | bool          | Whether or not to delete the PTF install files after apply. The default is True.  |

Return Variables
--------------

| Variable              | Type          | Description                   |
|-----------------------|---------------|-------------------------------|
| `apply_fail_list`   | list          | The list of the failed apply.  |
| `apply_success_list`      | list          | The list of the successful apply.      |

Example Playbook
----------------
```
- name: Transfer a list of individual ptfs install files to an ibm i system, then load and apply
  hosts: desthost

  vars:
    src_host: "srchost"
    not_loaded_list:
      - {'ptf_id':'SI75995', 'product':'5733SC1', 'release': 'V7R2M0', 'file_path': '/home/test/PTF/singleptf/SI75995'}
      - {'ptf_id':'SI63556', 'product':'5770UME', 'release': 'V1R4M0', 'file_path': '/home/test/PTF/singleptf/SI63556'}
    already_loaded_list:
      - {'ptf_id':'SI77217', 'product':'5770UME'}

  tasks:
    - name: Include sync_apply_individual_ptfs_lv1 role to transfer a list of individual ptfs to target ibm i, then load and apply
      include_role:
        name: sync_apply_individual_ptfs_lv1
```

Example Returned Variables
----------------
```

"apply_success_list": [
        "SI75995",
        "SI77217"
    ]

"apply_fail_list": [
        "SI63556"
    ]

License
-------

Apache-2.0
