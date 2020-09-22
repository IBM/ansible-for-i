fix_repo_check_ptf_group
=========
Get the latest PTF group information from PSP(Preventive Service Planning) server, and check if the latest PTF group is already
in ptf_group_image table or already downloading.

Role Variables
--------------

| Variable              | Type          | Description                                                          |
|-----------------------|---------------|----------------------------------------------------------------------|
| `ptf_group`           | str           | The ptf group number will be checked.                                |
| `database`            | str           | The path of fix management sqlite3 database.                         |

Return Variables
--------------

| Variable                      | Type          | Description                                                                                   |
|-------------------------------|---------------|-----------------------------------------------------------------------------------------------|
| `fix_group_check_result`      | dict          | ibmi_fix_group_check module returned result of the latest ptf group's information.            |
| `ptf_group_find_result`       | dict          | ibmi_fix_repo module returned result of ptf group's information in ptf_group_image_info table.|
| `download_status_find_result` | dict          | ibmi_fix_repo module returned result of ptf group's information in download_status table.     |
| `check_ptf_group_fail` | bool          | The flag indicates whether fix_repo_check_ptf_group role ended successfully or failed.     |

Example Playbook
----------------
```
- name: IBM i check ptf group
  hosts: testhost

  vars:
    ptf_group: "SF99740"
    database: "/tmp/repo.sqlite3"

  tasks:
    - name: Include fix_repo_check_ptf_group role to check if the latest ptf group is already in catalog
      include_role:
        name: fix_repo_check_ptf_group

```

Returned variables example
--------------------------
```
"fix_group_check_result": {
    "changed": false,
    "count": 1,
    "elapsed_time": "0:00:01.819350",
    "end": "2020-09-21 08:56:17.880138",
    "failed": false,
    "group_info": [
        {
            "description": "SF99662 740 IBM HTTP Server for i",
            "ptf_group_level": 7,
            "ptf_group_number": "SF99662",
            "ptf_list": [
                {
                    "apar": "SE73811",
                    "date": "07/06/20",
                    "product": "5770SS1",
                    "ptf_id": "SI73528"
                },
                {
                    "apar": "SE73701",
                    "date": "07/02/20",
                    "product": "5770DG1",
                    "ptf_id": "SI73395"
                },
                {
                    "apar": "SE73735",
                    "date": "07/02/20",
                    "product": "5770DG1",
                    "ptf_id": "SI73500"
                },
                {
                    "apar": "SE73302",
                    "date": "07/02/20",
                    "product": "5770DG1",
                    "ptf_id": "SI73415"
                },
                {
                    "apar": "SE73574",
                    "date": "07/02/20",
                    "product": "5770SS1",
                    "ptf_id": "SI73223"
                },
                {
                    "apar": "SE72896",
                    "date": "07/02/20",
                    "product": "5770SS1",
                    "ptf_id": "SI73284"
                },
                {
                    "apar": "SE73610",
                    "date": "07/02/20",
                    "product": "5770SS1",
                    "ptf_id": "SI73280"
                },
                {
                    "apar": "SE73346",
                    "date": "07/02/20",
                    "product": "5770SS1",
                    "ptf_id": "SI73269"
                },
                {
                    "apar": "SE73779",
                    "date": "07/02/20",
                    "product": "5770SS1",
                    "ptf_id": "SI73492"
                },
                {
                    "apar": "SE73442",
                    "date": "07/02/20",
                    "product": "5770SS1",
                    "ptf_id": "SI73045"
                },
                {
                    "apar": "SE73780",
                    "date": "07/02/20",
                    "product": "5770SS1",
                    "ptf_id": "SI73491"
                },
                {
                    "apar": "SE73244",
                    "date": "04/29/20",
                    "product": "5770DG1",
                    "ptf_id": "SI73086"
                },
                {
                    "apar": "SE71837",
                    "date": "04/29/20",
                    "product": "5770DG1",
                    "ptf_id": "SI70669"
                },
                {
                    "apar": "SE73495",
                    "date": "04/29/20",
                    "product": "5770SS1",
                    "ptf_id": "SI73103"
                },
                {
                    "apar": "SE73245",
                    "date": "04/29/20",
                    "product": "5770SS1",
                    "ptf_id": "SI73087"
                },
                {
                    "apar": "SE73240",
                    "date": "04/11/20",
                    "product": "5770DG1",
                    "ptf_id": "SI72594"
                },
                {
                    "apar": "SE73064",
                    "date": "04/11/20",
                    "product": "5770DG1",
                    "ptf_id": "SI72301"
                },
                {
                    "apar": "SE72790",
                    "date": "04/11/20",
                    "product": "5770DG1",
                    "ptf_id": "SI71970"
                },
                {
                    "apar": "SE73109",
                    "date": "04/11/20",
                    "product": "5770SS1",
                    "ptf_id": "SI72347"
                },
                {
                    "apar": "SE72680",
                    "date": "01/13/20",
                    "product": "5770DG1",
                    "ptf_id": "SI71803"
                },
                {
                    "apar": "SE72318",
                    "date": "01/13/20",
                    "product": "5770DG1",
                    "ptf_id": "SI71704"
                },
                {
                    "apar": "SE72474",
                    "date": "01/13/20",
                    "product": "5770DG1",
                    "ptf_id": "SI71554"
                },
                {
                    "apar": "SE72428",
                    "date": "01/13/20",
                    "product": "5770DG1",
                    "ptf_id": "SI71619"
                },
                {
                    "apar": "SE72597",
                    "date": "01/13/20",
                    "product": "5770SS1",
                    "ptf_id": "SI71700"
                },
                {
                    "apar": "SE72482",
                    "date": "01/13/20",
                    "product": "5770SS1",
                    "ptf_id": "SI71589"
                },
                {
                    "apar": "SE72413",
                    "date": "01/13/20",
                    "product": "5770SS1",
                    "ptf_id": "SI71411"
                },
                {
                    "apar": "SE72111",
                    "date": "10/22/19",
                    "product": "5733ARE",
                    "ptf_id": "SI71027"
                },
                {
                    "apar": "SE71730",
                    "date": "10/22/19",
                    "product": "5770SS1",
                    "ptf_id": "SI70542"
                },
                {
                    "apar": "SE71884",
                    "date": "10/22/19",
                    "product": "5770SS1",
                    "ptf_id": "SI70827"
                },
                {
                    "apar": "SE71407",
                    "date": "06/19/19",
                    "product": "5770DG1",
                    "ptf_id": "SI70130"
                }
            ],
            "release": "R740",
            "release_date": "07/06/2020",
            "url": "https://www.ibm.com/support/pages/uid/nas4SF99662"
        }
    ],
    "rc": 0,
    "start": "2020-09-21 08:56:16.060788",
    "stderr": "",
    "stderr_lines": []
}

"ptf_group_find_result": {
    "action": "find",
    "changed": false,
    "checksum": false,
    "database": "/tmp/repo.sqlite3",
    "delta": "0:00:00.000866",
    "end": "2020-09-21 08:56:25.418431",
    "fail_list": [
        {
            "db_record": "RecordNotFound",
            "ptf_group_level": 7,
            "ptf_group_number": "SF99662",
            "release_date": "07/06/2020"
        }
    ],
    "failed": false,
    "parameters": [
        {
            "ptf_group_level": 7,
            "ptf_group_number": "SF99662",
            "release_date": "07/06/2020"
        }
    ],
    "row_changed": -1,
    "sql": "SELECT * FROM ptf_group_image_info WHERE ptf_group_number=:ptf_group_number AND ptf_group_level=:ptf_group_level AND release_date=:release_date ",
    "sqlite3Runtime": "3.32.3",
    "sqlite3Version": "2.6.0",
    "start": "2020-09-21 08:56:25.417565",
    "type": "ptf_group"
}

"download_status_find_result": {
    "action": "find",
    "changed": false,
    "checksum": false,
    "database": "/tmp/repo.sqlite3",
    "delta": "0:00:00.000863",
    "end": "2020-09-21 08:56:33.432791",
    "fail_list": [
        {
            "db_record": "RecordNotFound",
            "ptf_group_level": 7,
            "ptf_group_number": "SF99662",
            "release_date": "07/06/2020"
        }
    ],
    "failed": false,
    "parameters": [
        {
            "ptf_group_level": 7,
            "ptf_group_number": "SF99662",
            "release_date": "07/06/2020"
        }
    ],
    "row_changed": -1,
    "sql": "SELECT * FROM download_status WHERE ptf_group_number=:ptf_group_number AND ptf_group_level=:ptf_group_level AND release_date=:release_date ",
    "sqlite3Runtime": "3.32.3",
    "sqlite3Version": "2.6.0",
    "start": "2020-09-21 08:56:33.431928",
    "type": "download_status"
}

```
License
-------

Apache-2.0
