load_ptf
=========

Load a set of ptfs according to given ptfs list, and returned ptfs loaded status.

Role Variables
--------------

| Variable              | Type          | Description                                                       |
|-----------------------|---------------|-------------------------------------------------------------------|
| `to_be_loaded_list`   | list          | ptfs list will be loaded. ptf_number and savf_name are required.  |
| `remote_lib`          | str           | The remote lib stores ptfs' savf, default is QGPL.                |

Return Variables
--------------

| Variable              | Type          | Description                                                       |
|-----------------------|---------------|-------------------------------------------------------------------|
| `excution_status`     | dict          | The ptfs' load excution status. Status can be 'fail' or 'success'.|

Example Playbook
----------------
```
- name: IBM i load a set of PTFs
  hosts: testhost

  vars:
    to_be_loaded_list:
      - {'ptf_number':'SI73543', 'product_id':'5770UME', 'savf_name':'QSI73543'}
      - {'ptf_number':'SI73430', 'product_id':'5733SC1', 'savf_name':'QSI73430'}

  tasks:
    - name: load ptfs
      include_role:
        name: load_ptf
      register: load_result

    - name: summarize the load ptfs excution status
      debug:
        msg: 'load ptfs excution status: {{ excution_status }}'
```

License
-------

Apache-2.0
