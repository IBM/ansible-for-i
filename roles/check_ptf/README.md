check_ptf
=========

Check ptfs status according to given ptfs list, and returned all the ptfs info, status and a to-be-load ptfs list

Role Variables
--------------

| Variable              | Type          | Description                                               |
|-----------------------|---------------|-----------------------------------------------------------|
| `check_ptf_list`      | list          | ptfs list will be checked. ptf_id is required.        |

Return Variables
--------------

| Variable              | Type          | Description                                               |
|-----------------------|---------------|-----------------------------------------------------------|
| `ptfs_info`           | list          | The status of all ptfs defined in check+ptf_list. The type of element is dictionary. Two keys in the dictionary are PTF_IDENTIFIER and PTF_LOAD_STATUS                   |
| `ptfs_status`         | dict          | Its keys are the value of ptf_id defined in check_ptf_list. Its values are the value of PTF_LOADED_STATUS.             |
| `not_loaded_ptfs_list` | list          | The sub-list of check_ptf_list. It includes PTFs don't exist and PTFs whose PTF_LOADED_STATUS is NOT_LOADED or PERMANENTLY REMOVED. |

Example Playbook
----------------
```
- name: IBM i check a set of PTFs
  hosts: testhost

  vars:
    check_ptf_list:
      - {'ptf_id':'SI73543', 'product':'5770UME', 'file_name':'QSI73543'}
      - {'ptf_id':'SI73430', 'product':'5733SC1', 'file_name':'QSI73430'}

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

    - name: print to be not_loaded_ptfs_list
      debug:
        msg: "to be loaded ptf list: {{ not_loaded_ptfs_list }}"
```

Example Returned Variables
----------------
```
"ptfs_info"    {
    {
        "PTF_ACTION_PENDING": "NO",
        "PTF_ACTION_REQUIRED": "NONE",
        "PTF_CREATION_TIMESTAMP": "2019-08-27T15:54:01",
        "PTF_IDENTIFIER": "SI73430",
        "PTF_IPL_ACTION": "NONE",
        "PTF_IPL_REQUIRED": "IMMEDIATE",
        "PTF_LOADED_STATUS": "APPLIED",
        "PTF_PRODUCT_ID": "5770UME",
        "PTF_SAVE_FILE": "YES",
        "PTF_STATUS_TIMESTAMP": "2020-09-19T17:34:35",
        "PTF_TEMPORARY_APPLY_TIMESTAMP": "2020-09-19T17:34:35"
    },
    {
        "PTF_LOADED_STATUS": "NON-EXISTENT",
        "PTF_PRODUCT_ID": "5733SC1",
    }

"ptfs_status": {
    "SI73543": "APPLIED",
    "SI73430": "NON-EXISTENT"
}

"not_loaded_ptfs_list": [{'ptf_id':'SI73430', 'product':'5733SC1', 'file_name':'QSI73430'}]
```

License
-------

Apache-2.0
