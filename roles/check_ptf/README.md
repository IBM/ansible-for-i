check_ptf
=========

Check ptfs status according to given ptfs list, and returned all the ptfs info, status and a to-be-load ptfs list

Role Variables
--------------

| Variable              | Type          | Description                                               |
|-----------------------|---------------|-----------------------------------------------------------|
| `check_ptf_list`      | list          | ptfs list will be checked. ptf_number is required.        |

Return Variables
--------------

| Variable              | Type          | Description                                               |
|-----------------------|---------------|-----------------------------------------------------------|
| `ptfs_info`           | list          | The ptfs in check_ptf_list informations.                  |
| `ptfs_status`         | dict          | The ptfs PTF_LOADED_STATUS in ptfs_info.                  |
| `to-be-load`          | list          | To be loaded ptfs list that can be used by load_ptf role. |

Example Playbook
----------------
```
- name: IBM i check a set of PTFs
  hosts: testhost

  vars:
    check_ptf_list:
      - {'ptf_number':'SI73543', 'product_id':'5770UME', 'savf_name':'QSI73543'}
      - {'ptf_number':'SI73430', 'product_id':'5733SC1', 'savf_name':'QSI73430'}

  tasks:
    - name: check ptf status
      include_role:
        name: check_ptf

    - name: print ptfs status
      debug:
        msg: 'ptfs info: {{ ptfs_info }}'

    - name: print ptfs status
      debug:
        msg: 'ptfs status: {{ ptfs_status }}'

    - name: print to be loaded ptf list
      debug:
        msg: "to be loaded ptf list: {{ to_be_load }}"
```

License
-------

Apache-2.0
