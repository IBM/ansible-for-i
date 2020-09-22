check_ptf_groups
=========

Compare the installed PTF groups on IBM i against the fix repository by the method of "current" or "latest" level, and returned the PTF group status and a ptf_not_installed list.

Role Variables
--------------

| Variable              | Type          | Description                                               |
|-----------------------|---------------|-----------------------------------------------------------|
| `group_list`          | list          | groups will be checked.                                   |
| `type`                | string        | compare the ptf groups by level. Value can be 'current' or 'latest'. Default value is 'latest'.|
| `repo_server`         | string        | repository server name registered in inventory.           |
| `database`            | string        | database name of repository server.                       |

Return Variables
--------------

| Variable              | Type          | Description                                               |
|-----------------------|---------------|-----------------------------------------------------------|
| `group_status`        | list          | The list of group status information.                     |

Example Playbook
----------------
```
- name: IBM i check a set of groups
  hosts: ibmi

  vars:
    group_list:
      - "SF99740"
      - "SF99665"
      - "SF99722"
      - "SF99704"
    type: "current"
    repo_server: "repo_server_name"
    database: "/tmp/testdb.sqlite3"

  tasks:
    - name: check ptf groups
      include_role:
        name: check_ptf_groups

    - name: print groups status
      debug:
        var: group_status

```

Return Value Example
----------------
```
The "latest" method contains the attributes of "LATEST_PTF_GROUP_LEVEL" and "CURRENT_PTF_GROUP_LEVEL".
The "current" method only contains the attribute "CURRENT_PTF_GROUP_LEVEL".

Example for type "latest":
"group_status": [
    # PTF group does not exist in fix repository
    {
        "PTF_GROUP_NUMBER": "SF99740",
        "PTF_GROUP_STATUS": "Record not found in repository DB"
    },
    # PTF group does not exist on target system
    {
        "PTF_GROUP_NUMBER": "SF99704",
        "PTF_GROUP_STATUS": "NON-EXISTENT"
    },
    # PTF group level does not match.
    {
        "CURRENT_PTF_GROUP_LEVEL": 30,
        "LATEST_PTF_GROUP_LEVEL": 31,
        "PTF_GROUP_NUMBER": "SF99722",
        "PTF_GROUP_STATUS": "INSTALLED",
    },
    # PTF group level is latest, while status is not installed.
    {
        "CURRENT_PTF_GROUP_LEVEL": 7,
        "LATEST_PTF_GROUP_LEVEL": 7,
        "PTF_GROUP_NUMBER": "SF99665",
        "PTF_GROUP_STATUS": "NOT INSTALLED",
        "PTF_NOT_INSTALLED": [
            {
                "PTF_IDENTIFIER": "SI69781",
                "PTF_LOADED_STATUS": "NON-EXISTENT"
            },
            {
                "PTF_IDENTIFIER": "SI69765",
                "PTF_LOADED_STATUS": "NON-EXISTENT"
            },
            {
                "PTF_IDENTIFIER": "SI73382",
                "PTF_LOADED_STATUS": "PERMANENTLY REMOVED"
            },
            {
                "PTF_IDENTIFIER": "SI73425",
                "PTF_LOADED_STATUS": "PERMANENTLY REMOVED"
            }
        ]
    }
]

Example for type "current":
"group_status": [
    # PTF group with specific level does not exist in fix repository
    {
        "CURRENT_PTF_GROUP_LEVEL": 19340
        "PTF_GROUP_NUMBER": "SF99740",
        "PTF_GROUP_STATUS": "Record not found in repository DB"
    },
    # PTF group does not exist on target system
    {
        "PTF_GROUP_NUMBER": "SF99704",
        "PTF_GROUP_STATUS": "NON-EXISTENT"
    },
    # PTF group is installed on target system
    {
        "CURRENT_PTF_GROUP_LEVEL": 30,
        "PTF_GROUP_NUMBER": "SF99722",
        "PTF_GROUP_STATUS": "INSTALLED",
    },
    # PTF group with specific level is not installed.
    {
        "CURRENT_PTF_GROUP_LEVEL": 7,
        "PTF_GROUP_NUMBER": "SF99665",
        "PTF_GROUP_STATUS": "NOT INSTALLED",
        "PTF_NOT_INSTALLED": [
            {
                "PTF_IDENTIFIER": "SI69781",
                "PTF_LOADED_STATUS": "NON-EXISTENT"
            },
            {
                "PTF_IDENTIFIER": "SI69765",
                "PTF_LOADED_STATUS": "NON-EXISTENT"
            },
            {
                "PTF_IDENTIFIER": "SI73382",
                "PTF_LOADED_STATUS": "PERMANENTLY REMOVED"
            },
            {
                "PTF_IDENTIFIER": "SI73425",
                "PTF_LOADED_STATUS": "PERMANENTLY REMOVED"
            }
        ]
    }
]
```

License
-------

Apache-2.0
