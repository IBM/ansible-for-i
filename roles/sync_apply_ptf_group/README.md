sync_apply_ptf_group
=========
Call ibmi_synchronize_files to tranfer the exists ptf group files to an ibm i system, then call ibmi_fix_imgclg to apply this
ptf group. And return the result.

Role Variables
--------------

| Variable              | Type          | Description                                                        |
|-----------------------|---------------|--------------------------------------------------------------------|
| `ptf_group_info`      | dict          | The ptf group's information. Only file_path is required. file_path must be a folder, and all of this
ptf group's files should be in this folder. |
| `src_host`            | str           | The system that has the src ptf group's files, which will be transferred to target system.|
| `dest`                | str           | The path that ptf group files would be transferred to. Default is "/ansible/image".  |

Return Variables
--------------

| Variable              | Type          | Description                                               |
|-----------------------|---------------|-----------------------------------------------------------|
| `sync_result`         | list          | ibmi_synchronize_files module returned result of transmission.               |
| `apply_result`        | dict          | ibmi_fix_imgclg module returned result of apply ptf group.                 |
| `sync_apply_fail`     | bool          | The flag indicates whether sync_apply_ptf_group role ended successfully or failed. |

Example Playbook
----------------
```
- name: Example of sync_apply_ptf_group role
  hosts: testhost

  vars:
    ptf_group_info: "{ 'file_path': '/QIBM/UserData/OS/Service/ECS/PTF/2025910369' }"
    src_host: "{{ src_host }}"

  tasks:
    - name: Include sync_apply_ptf_group role to transfer PTF group files to target ibm i, and apply
      include_role:
        name: sync_apply_ptf_group

```
Return Value Example
----------------
```
"sync_result": {
    "changed": false,
    "delta": "0:00:16.935896",
    "fail_list": [],
    "failed": 0,
    "msg": "Complete synchronize file list to remote host testhost",
    "rc": 0,
    "stderr": "",
    "stderr_lines": [],
    "stdout": "",
    "stdout_lines": [],
    "success_list": [
        {
            "src": "/QIBM/UserData/OS/Service/ECS/PTF/2026173258/S8404V01.BIN"
        }
    ]
}

"apply_result": {
        "changed": true,
        "delta": "0:00:59.082563",
        "end": "2020-09-22 16:31:32.095409",
        "failed": false,
        "job_log": [],
        "need_action_ptf_list": [],
        "rc": 0,
        "start": "2020-09-22 16:30:33.012846"
    }

"sync_apply_fail": True
```
License
-------

Apache-2.0
