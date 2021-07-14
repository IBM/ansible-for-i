fix_repo_download_add_ptf_group
=========
Call ibmi_download_fix module to download ptf group, then call ibmi_fix_repo module to add information into download_status table in catalog.

Role Variables
--------------

| Variable              | Type          | Description                                                          |
|-----------------------|---------------|----------------------------------------------------------------------|
| `ptf_group_info`    | str           | The ptf group information. ptf_group_number, ptf_group_level, release, release_date, ptf_list and description are required.        |

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
    ptf_group_info: {
        "description": "SF99704 740 DB2 for IBM i",
        "ptf_group_level": 11,
        "ptf_group_number": "SF99704",
        "ptf_list": [
                    {
                        "apar": "SE71038",
                        "date": "06/19/19",
                        "product": "5770SS1",
                        "ptf_id": "SI69673"
                    },
                    {
                        "apar": "SE70956",
                        "date": "06/19/19",
                        "product": "5770SS1",
                        "ptf_id": "SI69805"
                    },
                    {
                        "apar": "SE71415",
                        "date": "06/19/19",
                        "product": "5770SS1",
                        "ptf_id": "SI70136"
                    },
                    {
                        "apar": "SE71420",
                        "date": "06/19/19",
                        "product": "5770SS1",
                        "ptf_id": "SI70149"
                    }
                ],
        "release": "R740",
        "release_date": "01/26/2021",
    }

    - name: Include fix_repo_download_add_ptf_group role to download the ptf group and add information into catalog download_status table
      include_role:
        name: fix_repo_download_add_ptf_group

```

License
-------

Apache-2.0