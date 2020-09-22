apply_ptf
=========

Apply all loaded ptfs or apply a set of ptfs according to given ptfs list or apply all loaded ptfs, and return ptfs applied status. Then perform an IPL if auto_ipl is set to true and at least one PTF requests an IPL for permanent applied or temporary applied

Role Variables
--------------

| Variable              | Type          | Description                                                            |
|-----------------------|---------------|------------------------------------------------------------------------|
| `apply_all_loaded_ptfs`| bool          | Controls whether all loaded ptf will be applied. When its value is true, 'to_be_applied_list' will be ignored. Default value is false.    |
| `to_be_applied_list`  | list          | ptfs list will be applied. ptf_id and product are required. ptfs in the list will be applied one by one.          |
| `temp_or_perm`         | str          | Controls whether the target PTFs will be permanent applied or temporary applied. Value can be  '*TEMP' or '*PERM'. Default value is '*TEMP'.                     |
| `delayed_option`       | str          | Controls whether the PTF is delayed apply or not. Value can be '*YES', '*NO' or '*IMMDLY'. Default value is '*IMMDLY'.                      |
| `auto_ipl`             | bool           | Controls whether an immediate reboot will be launched automatically if at least one ptf requests an IPL for permanent applied or temporary applied. Default value is false. |


Return Variables
--------------

| Variable              | Type          | Description                                                       |
|-----------------------|---------------|-------------------------------------------------------------------|
| `apply_success_list`   | list          | The list of successful apply when to_be_applied_list is provided.                              |
| `apply_fail_list`      | list          | The list of failed apply when to_be_applied_list is provided.                                        |

Example Playbook
----------------
```
- name: IBM i apply a set of single PTFs one by one
  hosts: testhost

  vars:
    to_be_applied_list:
      - {'ptf_id':'SI73543', 'product':'5770UME'}
      - {'ptf_id':'SI73430', 'product':'5733SC1'}

  tasks:
    - name: apply a list of single ptfs
      include_role:
        name: apply_ptf
      register: load_result
```

```
- name: IBM i apply a set of single PTFs immediately, all those PTFs are applied permanently. 
  hosts: testhost

  vars:
    to_be_applied_list:
      - {'ptf_id':'SI73543', 'product':'5770UME'}
      - {'ptf_id':'SI73430', 'product':'5733SC1'}
    temp_or_perm: '*PERM'
    delayed_option: '*NO' 
    auto_ipl: false

  tasks:
    - name: apply a list of single ptfs
      include_role:
        name: apply_ptf
      register: load_result
```

```
- name: IBM i apply all loaded ptfs and IPL the system if at least one PTF requires an IPL for permanent applied or temporary applied. 
  hosts: ibmi 

  roles:
    - role: apply_ptf
      vars:
        apply_all_loaded_ptfs: true 
        temp_or_perm: '*PERM'
        delayed_option: '*NO' 
        auto_ipl: true
```

License
-------

Apache-2.0
