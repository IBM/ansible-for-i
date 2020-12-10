fix_repo_check_download_individual_ptfs
=========

Check if requested individual PTFs are already in catalog. If not, will call download_individual_ptfs role to download non-existent
ptfs and write the information into catalog.

Role Variables
--------------

| Variable               | Type          | Description                                                            |
|------------------------|---------------|------------------------------------------------------------------------|
| `ptfs_list_parm`| list          | The list of ptfs that need to be checked and downloaded.     |
| `order`| str          | Specifies if requisite PTFs should be included with the ordered PTFs. The default value is '*PTFID'.     |
| `repo_server`| str          | Specifies the SNDPTFORD server used to download ptfs.     |

Return Variables
--------------

| Variable                | Type          | Description                                                       |
|-------------------------|---------------|-------------------------------------------------------------------|
| `check_fail_list` | list          | The list of ptfs which records are found in catalog with errors. |
| `RecordNotFound_list` | list          | The list of ptfs which records are not found in the catalog.                                  |
| `download_success_list` | list          | The list of successful download.                                  |
| `download_fail_list`    | list          | The list of failed download.                                      |
| `final_find_result` | list          | The final information records in the catalog of requested ptfs list.           |

Example Playbook
----------------
```
- name: IBM i download a list of individual PTFs
  hosts: repo_server

  vars:
    ptfs_list_parm: ['SI67856', 'SI69375', 'SI73751']
    repo_server: systemA

  tasks:
    - name: Include fix_repo_check_download_individual_ptfs role to download a list of individual ptfs
      include_role:
        name: fix_repo_check_download_individual_ptfs
```

Example Returned Variables
----------------
```
"download_success_list": [
        {
            "download_time": "2020-12-02T23:55:16.626231",
            "file_name": "QSI74136",
            "file_path": "/qsys.lib/qgpl.lib/QSI74136.FILE",
            "order_id": "2033782086",
            "product": "5770ST1",
            "ptf_id": "SI74136",
            "release": "V7R3M0"
        },
]
"download_fail_list": [
        {
            "fail_reason": "Submit job failed.",
            "ptf_id": "123456"
        }
]
"check_fail_list": [
        {
            "add_time": "2020-11-23 09:01:03",
            "checksum": "d7d8d4787e2a1d858f3523f2ec963f7dbc9f78ff",
            "db_record": "MATCH_NOT_READABLE",
            "description": null,
            "download_time": "2020-12-01T23:55:06.731331",
            "file_name": "QSI74136.FILE",
            "file_path": "/qsys.lib/qgpl.lib/QSI74136.FILE",
            "id": 33,
            "msg": "Target image file [/qsys.lib/qgpl.lib/QSI74136.FILE] not readable",
            "order_id": "2033682044",
            "product": "5770ST1",
            "ptf_id": "SI74136",
            "ptf_status": null,
            "rc": -4,
            "release": "V7R3M0"
        }

]
"RecordNotFound_list": [
        {
            "add_time": "2020-11-23 09:01:03",
            "checksum": "d7d8d4787e2a1d858f3523f2ec963f7dbc9f78ff",
            "db_record": "MATCH_NOT_FOUND",
            "description": null,
            "download_time": "2020-12-01T23:55:06.731331",
            "file_name": "QSI74136.FILE",
            "file_path": "/qsys.lib/qgpl.lib/QSI74136.FILE",
            "id": 33,
            "msg": "Target image file [/qsys.lib/qgpl.lib/QSI74136.FILE] not found",
            "order_id": "2033682044",
            "product": "5770ST1",
            "ptf_id": "SI74136",
            "ptf_status": null,
            "rc": -4,
            "release": "V7R3M0"
        },
        {
            "add_time": "2020-11-23 09:01:03",
            "checksum": "8c80ab7211926fdb98ffa03e3b11120c4746431c",
            "db_record": "MATCH_NOT_FOUND",
            "description": null,
            "download_time": "2020-12-01T23:53:36.876014",
            "file_name": "QSI74612.FILE",
            "file_path": "/qsys.lib/qgpl.lib/QSI74612.FILE",
            "id": 32,
            "msg": "Target image file [/qsys.lib/qgpl.lib/QSI74612.FILE] not found",
            "order_id": "2033681997",
            "product": "5770WDS",
            "ptf_id": "SI74612",
            "ptf_status": null,
            "rc": -4,
            "release": "V7R3M0"
        }
    ]
"final_find_result": {
        "action": "find",
        "changed": false,
        "checksum": true,
        "database": "/etc/ibmi_ansible/fix_management/repo.sqlite3",
        "delta": "0:00:00.106584",
        "end": "2020-12-02 23:56:22.664672",
        "failed": false,
        "parameters": [
            {
                "ptf_id": "SI74136"
            },
            {
                "ptf_id": "SI74612"
            }
        ],
        "row_changed": -1,
        "sql": "SELECT * FROM single_ptf_info WHERE ptf_id=:ptf_id ",
        "sqlite3Runtime": "3.32.3",
        "sqlite3Version": "2.6.0",
        "start": "2020-12-02 23:56:22.558088",
        "success_list": [
            {
                "add_time": "2020-11-23 09:01:03",
                "checksum": "d7d8d4787e2a1d858f3523f2ec963f7dbc9f78ff",
                "db_record": "MATCH",
                "description": null,
                "download_time": "2020-12-02T23:55:16.626231",
                "file_name": "QSI74136.FILE",
                "file_path": "/qsys.lib/qgpl.lib/QSI74136.FILE",
                "id": 33,
                "order_id": "2033782086",
                "product": "5770ST1",
                "ptf_id": "SI74136",
                "ptf_status": null,
                "release": "V7R3M0"
            },
            {
                "add_time": "2020-11-23 09:01:03",
                "checksum": "8c80ab7211926fdb98ffa03e3b11120c4746431c",
                "db_record": "MATCH",
                "description": null,
                "download_time": "2020-12-02T23:56:01.724063",
                "file_name": "QSI74612.FILE",
                "file_path": "/qsys.lib/qgpl.lib/QSI74612.FILE",
                "id": 32,
                "order_id": "2033782139",
                "product": "5770WDS",
                "ptf_id": "SI74612",
                "ptf_status": null,
                "release": "V7R3M0"
            }
        ],
        "type": "single_ptf"
    }
```

License
-------

Apache-2.0
