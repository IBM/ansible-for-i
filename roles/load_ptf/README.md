load_ptf
=========

Load a set of ptfs according to given ptfs list, and return ptfs loaded status.

Role Variables
--------------

| Variable              | Type          | Description                                                            |
|-----------------------|---------------|------------------------------------------------------------------------|
| `to_be_loaded_list`   | list          | ptfs list will be loaded. ptf_id, product and file_name are required.  |
| `remote_lib`          | str           | The remote lib stores ptfs' savf, default is QGPL.                     |

Return Variables
--------------

| Variable              | Type          | Description                                                       |
|-----------------------|---------------|-------------------------------------------------------------------|
| `load_success_list`   | list          | The list of successful load.                                      |
| `load_fail_list`      | list          | The list of failed load.                                          |

Example Playbook
----------------
```
- name: IBM i load a set of PTFs
  hosts: testhost

  vars:
    to_be_loaded_list:
      - {'ptf_id':'SI73543', 'product':'5770UME', 'file_name':'QSI73543'}
      - {'ptf_id':'SI73430', 'product':'5733SC1', 'file_name':'QSI73430'}

  tasks:
    - name: load ptfs
      include_role:
        name: load_ptf
      register: load_result
```

License
-------

Apache-2.0
