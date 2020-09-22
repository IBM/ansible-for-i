fix_repo_extract_ptf_group_info
=========
Call ibmi_fix_repo module to get the order information in download_status table, then call ibmi_fix_repo module again to extract
and update ptf group's information into ptf_group_image_info table in catalog.

Role Variables
--------------

| Variable              | Type          | Description                                                          |
|-----------------------|---------------|----------------------------------------------------------------------|
| `order_id`    | str           | The ptf group number will be download.                               |
| `database`            | str           | The path of fix management sqlite3 database.                         |

Return Variables
--------------

| Variable                  | Type    | Description                                                                                    |
|---------------------------|---------|------------------------------------------------------------------------------------------------|
| `fix_repo_find_result`    | dict    | ibmi_fix_repo module returned result of added order's information in download_status table.        |
| `fix_repo_update_result`  | dict    | ibmi_fix_repo module returned result of updated ptf group's information in ptf_group_image_info table.|

Example Playbook
----------------
```
- name: Example of fix_repo_extract_ptf_group_info role
  hosts: testhost

  vars:
    order_id: "2376543543"
    database: "/tmp/repo.sqlite3"

    - name: Include fix_repo_extract_ptf_group_info role to extract PTF group information and update into catalog
      include_role:
        name: fix_repo_extract_ptf_group_info

```

License
-------

Apache-2.0
