download_individual_ptfs
=========

Call ibmi_download_fix module to download a list of individual ptfs, and return status.

Role Variables
--------------

| Variable               | Type          | Description                                                            |
|------------------------|---------------|------------------------------------------------------------------------|
| `to_be_downloaded_list`| list          | The list of the ptfs that will be downloaded. ptf_id is required.     |
| `order`| str          | Specifies if requisite PTFs should be included with the ordered PTFs. The default value is '*PTFID'.     |
| `download_server`| str          | Specifies the SNDPTFORD server used to download ptfs.     |

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
    download_server: 'downloadserver'

  tasks:
    - name: Include download_individual_ptfs role to download a list of individual ptfs
      include_role:
        name: download_individual_ptfs
```

License
-------

Apache-2.0
