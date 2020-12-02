download_individual_ptfs
=========

Call ibmi_download_fix module to download a list of individual ptfs, and return status.

Role Variables
--------------

| Variable               | Type          | Description                                                            |
|------------------------|---------------|------------------------------------------------------------------------|
| `to_be_downloaded_list`| list          | The list of ptfs that will be downloaded. Only ptf_id is required.     |

Return Variables
--------------

| Variable                | Type          | Description                                                       |
|-------------------------|---------------|-------------------------------------------------------------------|
| `download_success_list` | list          | The list of successful download.                                  |
| `download_fail_list`    | list          | The list of failed download.                                      |

Example Playbook
----------------
```
- name: IBM i download a list of individual PTFs
  hosts: testhost

  vars:
    to_be_downloaded_list:
      - {'ptf_id':'SI73543'}
      - {'ptf_id':'SI73430'}

  tasks:
    - name: Include download_individual_ptfs role to download a list of individual ptfs
      include_role:
        name: download_individual_ptfs
      register: download_result
```

License
-------

Apache-2.0
