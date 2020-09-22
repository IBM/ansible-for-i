fix_repo_download_add_ptf_group
=========
Call ibmi_download_fix module to download ptf group, then call ibmi_fix_repo module to add information into download_status table in catalog.

Role Variables
--------------

| Variable              | Type          | Description                                                          |
|-----------------------|---------------|----------------------------------------------------------------------|
| `ptf_group_number`    | str           | The ptf group number will be download.                               |
| `ptf_group_level`     | str           | The ptf group level of the ptf group.                                |
| `release_date`        | str           | The release date of the ptf group.                                   |
| `database`            | str           | The path of fix management sqlite3 database.                         |

Return Variables
--------------

| Variable                      | Type          | Description                                                                                    |
|-------------------------------|---------------|------------------------------------------------------------------------------------------------|
| `download_fix_result`         | dict          | ibmi_download_fix module returned result                                                       |
| `download_status_add_result`  | dict          | ibmi_fix_repo module returned result of added ptf group's information in download_status table.|

Example Playbook
----------------
```
- name: Example of fix_repo_download_add_ptf_group role
  hosts: testhost

  vars:
    ptf_group_number: "SF99740"
    ptf_group_level: "7"
    release_date: "5/14/20"
    database: "/tmp/repo.sqlite3"

    - name: Include fix_repo_download_add_ptf_group role to download the ptf group and add information into catalog download_status table
      include_role:
        name: fix_repo_download_add_ptf_group

```

License
-------

Apache-2.0