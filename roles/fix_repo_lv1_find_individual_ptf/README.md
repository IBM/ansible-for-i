fix_repo_lv1_find_individual_ptf
=========

Call ibmi_fix_repo_lv1 module to recursively find individual PTFs in catalog

Role Variables
--------------

| Variable              | Type          | Description                                               |
|-----------------------|---------------|-----------------------------------------------------------|
| `ptfs_list`      | list         | PTFs list will be found. |
| `src_host`       | str          | The system that has the ptf install files, which will be transferred to the target system.        |
| `image_root`     | str          | Specifies the image files' dir on the repo_server        |

Return Variables
--------------

| Variable              | Type          | Description                                               |
|-----------------------|---------------|-----------------------------------------------------------|
| `ptf_find_result`     | list          | The find success result  |
| `ptf_fail_list`       | list          | The find failed ptf number list  |
| `ptf_success_list`    | list          | The find success ptf number list  |

Example Playbook
----------------
```
- name: Recursively find individual ptfs in catalog
  hosts: testhost

  vars:
    ptfs_list: ['SI67856', 'SI69375', 'SI73751']

  tasks:
    - name: Call fix_repo_lv1_find_individual_ptf role
      include_role:
        name: fix_repo_lv1_find_individual_ptf

    - name: print ptf_find_result
      debug:
        var: ptf_find_result

    - name: print ptf_fail_list
      debug:
        var: ptf_fail_list

    - name: print ptf_success_list
      debug:
        var: ptf_success_list

```

Example Returned Variables
----------------
```
"ptf_find_result"    [
    {
            "download_date": "2021/08/29",
            "image_files": [
                {
                    "expected_chksum": "19ad34bf52c5586fec3dbc692a20211d36942d048413a580817cf90de98c942d",
                    "file": "SI75995_1.bin",
                    "file_chksum": "19ad34bf52c5586fec3dbc692a20211d36942d048413a580817cf90de98c942d",
                    "integrity": true
                }
            ],
            "image_path": "/home/pengzy/PTF/singleptf/SI75995",
            "query_ptf": "SI75995"
        },
        {
            "download_date": "2022/02/20",
            "image_files": [
                {
                    "expected_chksum": "672d1e85aa70a79c705bbe7fffd50aad9698428f83c5fae0f2e16f508df8cba8",
                    "file": "SI77271B_1.bin",
                    "file_chksum": "672d1e85aa70a79c705bbe7fffd50aad9698428f83c5fae0f2e16f508df8cba8",
                    "integrity": true
                }
            ],
            "image_path": "/home/pengzy/PTF/singleptf/SI77271SI77631",
            "query_ptf": "SI77631"
        }
    ]

"ptf_fail_list": ["SI67856"]

"ptf_success_list": ["SI75995", "SI77631"]

```

License
-------

Apache-2.0
