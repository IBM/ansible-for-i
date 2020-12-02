fix_repo_check_download_individual_ptfs
=========

Check and downloading a list of individual ptfs into fix repository catalog, and return status.

Role Variables
--------------

| Variable               | Type          | Description                                                            |
|------------------------|---------------|------------------------------------------------------------------------|
| `ptfs_list`| list          | The list of ptfs that need to be checked and downloaded.     |
| `order`| str          | Specifies if requisite PTFs should be included with the ordered PTFs. Default value is '*PTFID'.     |
| `repo_server`| str          | Specifies the SNDPTFORD server used to download ptfs.     |

Return Variables
--------------

| Variable                | Type          | Description                                                       |
|-------------------------|---------------|-------------------------------------------------------------------|
| `check_fail_list` | list          | The list of ptfs which records are found in catalog with errors. |
| `RecordNotFound_list` | list          | The list of ptfs which records are not found in catalog.                                  |
| `download_success_list` | list          | The list of successful download.                                  |
| `download_fail_list`    | list          | The list of failed download.                                      |
| `final_find_result` | list          | The final information records in catalog of requested ptfs list.           |

Example Playbook
----------------
```
- name: IBM i download a list of individual PTFs
  hosts: repo_server

  vars:
    ptfs_list: ['SI67856', 'SI69375', 'SI73751']
    repo_server: systemA

  tasks:
    - name: Include fix_repo_check_download_individual_ptfs role to download a list of individual ptfs
      include_role:
        name: fix_repo_check_download_individual_ptfs
      register: check_download_result
```

License
-------

Apache-2.0
