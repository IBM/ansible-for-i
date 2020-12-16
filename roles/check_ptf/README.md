check_ptf
=========

Check ptfs status according to given ptfs list, and returned all the ptfs info, status, not loaded ptfs list and already loaded ptfs list

Role Variables
--------------

| Variable              | Type          | Description                                               |
|-----------------------|---------------|-----------------------------------------------------------|
| `check_ptf_list`      | list          | ptfs list will be checked. ptf_id is required. product and release are required if check_product is true.|
| `check_product`       | bool          | Specify if need to check product installed or not. The default value is True.        |

Return Variables
--------------

| Variable              | Type          | Description                                               |
|-----------------------|---------------|-----------------------------------------------------------|
| `ptfs_info`           | list          | The status of all ptfs defined in check_ptf_list. The type of element is the dictionary. Two keys in the dictionary are PTF_IDENTIFIER and PTF_LOAD_STATUS                   |
| `ptfs_status`         | dict          | Its keys are the value of ptf_id defined in check_ptf_list. Its values are the value of PTF_LOADED_STATUS.   |
| `not_loaded_ptfs_list` | list         | The sub-list of check_ptf_list. It includes PTFs don't exist and PTFs whose PTF_LOADED_STATUS is NOT_LOADED or PERMANENTLY REMOVED. |
| `loaded_ptfs_list` | list             | The sub-list of check_ptf_list. It includes the already loaded PTFs list. |
| `product_not_installed_ptfs` | list             | The sub-list of check_ptf_list. It includes the already loaded PTFs list. |

Example Playbook
----------------
```
- name: IBM i check a set of PTFs
  hosts: testhost

  vars:
    check_ptf_list:
      - {'ptf_id':'SI73543', 'product':'5770UME', 'release': 'V1R4M0'}
      - {'ptf_id':'SI73430', 'product':'5733SC1', 'release': 'V7R2M0'}
      - {'ptf_id':'SI73751', 'product':'5733SC1', 'release': 'V7R2M0'}
      - {'ptf_id':'SI63489', 'product':'5770UME', 'release': 'V1R4M0'}

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

    - name: print not_loaded_ptfs_list
      debug:
        msg: "to be loaded ptfs list: {{ not_loaded_ptfs_list }}"

    - name: print loaded_ptfs_list
      debug:
        msg: "Already loaded ptfs list: {{ loaded_ptfs_list }}"

    - name: print product_not_installed_ptfs
      debug:
        msg: "Product not installed ptfs list: {{ product_not_installed_ptfs }}"
```

Example Returned Variables
----------------
```
"ptfs_info"    [
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
    },
    {
        "PTF_ACTION_PENDING": "NO",
        "PTF_ACTION_REQUIRED": "NONE",
        "PTF_CREATION_TIMESTAMP": "2020-07-08T01:35:20",
        "PTF_IDENTIFIER": "SI73751",
        "PTF_IPL_ACTION": "NONE",
        "PTF_IPL_REQUIRED": "IMMEDIATE",
        "PTF_LOADED_STATUS": "LOADED",
        "PTF_PRODUCT_ID": "5733SC1",
        "PTF_SAVE_FILE": "NO",
        "PTF_STATUS_TIMESTAMP": "2020-11-02T14:14:48",
        "PTF_TEMPORARY_APPLY_TIMESTAMP": null
    },
    {
        "PTF_IDENTIFIER": "SI63489",
        "PTF_LOADED_STATUS": "PRODUCT_NOT_INSTALLED"
    }
    ]

"ptfs_status": {
    "SI73543": "APPLIED",
    "SI73430": "NON-EXISTENT"
    "SI73751": "LOADED"
    "SI63489": "PRODUCT_NOT_INSTALLED"
}

"not_loaded_ptfs_list": [
    {"ptf_id": "SI73430", "product": "5733SC1", "release": "V7R2M0"}
    ]

"loaded_ptfs_list": [
    {'ptf_id": "SI73751", "product":'5733SC1", "release": "V7R2M0"}
    ]

"product_not_installed_ptfs": [
    {"ptf_id": "SI63489", "product": "5770UME", "release": "V1R4M0"}
    ]
```

License
-------

Apache-2.0
