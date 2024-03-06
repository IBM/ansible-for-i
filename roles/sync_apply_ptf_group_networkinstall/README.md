sync_apply_ptf_group_networkinstall
=========
This role will setup network install env on repo server and use network install mechanism to install the PTF group on the target system.
*SRVLAN must be configured before use. Please refer to <a href="https://www.ibm.com/docs/en/i/7.5?topic=server-configuring-service-tools-dst" target="_blank">Configuring the service tools server for DST</a>

Role Variables
--------------

| Variable              | Type          | Description                                                        |
|-----------------------|---------------|--------------------------------------------------------------------|
| `ptf_group_info`      | dict          | The ptf group's information. file_path and file_name are required. file_path must be a folder, and all of this
ptf group's files should be in this folder. |
| `src_host`            | str           | The system that has the src ptf group's files, which will be transferred to the target system.|
| `delete`              | bool          | Whether or not to delete the PTF group install dir after apply. The default is True.  |
| `ptf_omit_list`       | list          | The list of PTFs which will be omitted. The elements of the list are dict. The key of the dict should be the product ID of the fix that is omitted.  |

Return Variables
--------------

| Variable              | Type          | Description                                               |
|-----------------------|---------------|-----------------------------------------------------------|
| `network_install_server_result`         | list          | ibmi_synchronize_files module returned result of transmission.               |
| `network_install_client_result`        | dict          | ibmi_fix_imgclg module returned result of apply ptf group.                 |

Example Playbook
----------------
```
- name: Example of sync_apply_ptf_group_networkinstall role
  hosts: testhost

  vars:
    ptf_group_info: { 'file_path': '/QIBM/UserData/OS/Service/ECS/PTF/2025910369', 'file_name': ['S8404V01.BIN'] }
    src_host: "{{ src_host }}"
    ptf_omit_list: [{'5770SS1': 'SI78582'}, {'5770ss1': 'SI78544'}]

  tasks:
    - name: Include sync_apply_ptf_group role to transfer PTF group files to target ibm i, and apply
      include_role:
        name: sync_apply_ptf_group_networkinstall

```
Example Returned Variables
----------------
```
"network_install_server_result": {
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

"network_install_client_result": {
        "changed": true,
        "delta": "0:00:59.082563",
        "end": "2020-09-22 16:31:32.095409",
        "failed": false,
        "job_log": [],
        "need_action_ptf_list": [],
        "rc": 0,
        "start": "2020-09-22 16:30:33.012846"
    }

```
License
-------

Apache-2.0
