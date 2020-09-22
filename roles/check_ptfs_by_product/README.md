check_ptfs_by_product
=========

Compare the PTF status with specific product id on IBM i against fix repository, and returned the PTFs' status list

Role Variables
--------------

| Variable              | Type          | Description                                               |
|-----------------------|---------------|-----------------------------------------------------------|
| `product`             | string        | the product of PTFs will be checked.                      |
| `repo_server`         | string        | repository server name registered in inventory.           |
| `database`            | string        | database name of repository server.                       |

Return Variables
--------------

| Variable              | Type          | Description                                               |
|-----------------------|---------------|-----------------------------------------------------------|
| `ptf_status`          | list          | The list of PTF status.                                   |

Example Playbook
----------------
```
- name: check the ptfs by product on IBM i against fix repository
  hosts: ibmi

  vars:
    product: "5770SS1"
    repo_server: "repo_server_name"
    database: "/tmp/testdb.sqlite3"

  tasks:
    - name: check product ptf
      include_role:
        name: check_ptfs_by_product

    - name: print ptfs status
      debug:
        var: ptf_status

```

Return Value Example
----------------
```
"ptf_status": [
    {
        "PRODUCT": "5770SS1",
        "PRODUCT_STATUS": "OK",
        "PTF_LIST": [
            {
                "PTF_IDENTIFIER": "SI69340",
                "PTF_STATUS": "NON-EXISTENT"
            },
            {
                "PTF_IDENTIFIER": "SI69764",
                "PTF_STATUS": "NON-EXISTENT"
            },
            {
                "PTF_IDENTIFIER": "SI70544",
                "PTF_LOADED_STATUS": "APPLIED"
            }
        ]
    }
]
```

License
-------

Apache-2.0
