fix_repo_download_apply_individual_ptfs
=========

Check if requested individual PTFs are already in catalog. If not, will download non-existent PTFs and write information into catalog.
After that, will transfer savfs to target server, then load and apply PTFs.

Role Variables
--------------

| Variable               | Type          | Description                                                            |
|------------------------|---------------|------------------------------------------------------------------------|
| `ptfs_list_parm`| list          | The list of PTFs that need to be applied.     |
| `repo_server`| str          | Specifies the SNDPTFORD server used to download ptfs.     |

Return Variables
--------------

| Variable                | Type          | Description                                                       |
|-------------------------|---------------|-------------------------------------------------------------------|
| `final_ptfs_status_with_requisite` | dict          | The dict of all the PTFs' status including requisite PTFs. |
| `original_ptfs_status`          | dict          | The dict of the original requested PTFs' status.     |
| `requisite_ptfs_status`         | dict          | The dict of the requisite PTFs' status.   |

Example Playbook
----------------
```
- name: IBM i download a list of individual PTFs
  hosts: testhost

  vars:
    ptfs_list_parm: ["SI73751", "SI74612", "SI74136"]
    repo_server: systemA

  tasks:
    - name: Include download_individual_ptfs role to download a list of individual ptfs
      include_role:
        name: download_individual_ptfs
```

Example Returned Variables
----------------
```
"final_ptfs_status_with_requisite": {
        "SI70936": "APPLIED",
        "SI74136": "APPLIED",
        "SI74612": "APPLIED",
        "SI73751": "APPLIED"
    }
"original_ptfs_status": {
        "SI74136": "APPLIED",
        "SI74612": "APPLIED"
    }
"requisite_ptfs_status": {
        "SI70936": "APPLIED"
    }
```

License
-------

Apache-2.0
