display_vm_info_via_powervc
=========
An Ansible role for displaying a VM via PowerVC.

Role Variables
--------------

| Variable              | Type          | Description                                      |
|-----------------------|---------------|--------------------------------------------------|
| `vm_name`      | str          | Required. Specifies the name of deployed vm.                      |

Example Playbooks
----------------
```
- name: Retrieve vm information a vm
  hosts: powervc 
  tasks:
    - include_role:
        name: display_vm_info_via_powervc
      vars:
        vm_name: 'Abc' 

```

License
-------

Apache-2.0
