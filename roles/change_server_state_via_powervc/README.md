change_server_state_via_powervc
=========
Ansible role for starting, stopping a VM via PowerVC.

Role Variables
--------------

| Variable              | Type          | Description                                      |
|-----------------------|---------------|--------------------------------------------------|
| `vm_action`      | str          | Specifies Perform the given action. Valid choices are stop, start                   |
| `vm_name`      | str          | Specifies the vm name or id.                      |


Example Playbooks
----------------
```
- name: Stop a vm
  hosts: powervc 
  tasks:
    - include_role:
        name: change_server_state_via_powervc
      vars:
        vm_action: 'stop'
        vm_name: 'vm1'

```

```
- name: Start a vm 
  hosts: powervc

  roles:
    - role: change_server_state_via_powervc
      vars:
        vm_action: 'start'
        vm_name: 'vm1'
```

License
-------

Apache-2.0
