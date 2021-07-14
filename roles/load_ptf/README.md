load_ptf
=========

Load a set of ptfs according to a given ptfs' list, and return ptfs' loaded status.

Role Variables
--------------

| Variable              | Type          | Description                                                            |
|-----------------------|---------------|------------------------------------------------------------------------|
| `to_be_loaded_list`   | list          | ptfs list will be loaded. ptf_id, product and file_name are required, others parameters are optional. |
| `remote_lib`          | str           | The remote lib stores ptfs' savf. The default value is QGPL.                     |

Return Variables
--------------

| Variable              | Type          | Description                                                       |
|-----------------------|---------------|-------------------------------------------------------------------|
| `load_success_list`   | list          | The list of the successful load.                                      |
| `load_fail_list`      | list          | The list of the failed load.                                          |
| `load_fail_dict`      | dict          | The dict of the failed load. The key is the ptf id, and the value is the ptf status.|

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
```
Example Returned Variables
----------------
```
"load_success_list": [
        {
            "file_name": "QSI73751.FILE",
            "product": "5733SC1",
            "ptf_id": "SI73751",
        }
]
"load_fail_list": [
        {
            "file_name": "QSI73962.FILE",
            "product": "5770JV1",
            "ptf_id": "SI73962",
        }
]
"load_fail_dict": {
        "SI73962": "OPTION_NOT_INSTALLED"
    }
```

License
-------

Apache-2.0
