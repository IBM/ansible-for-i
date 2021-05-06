deploy_vm_via_powervc
=========
The ansible role for creating a VM via PowerVC.

Role Variables
--------------

| Variable              | Type          | Description                                      |
|-----------------------|---------------|--------------------------------------------------|
| `image_name_or_id`      | str          | Required. The name or id of the base image to boot.                   |
| `vm_name`      | str          | Required. Specifies the name of the deployed vm.                      |
| `flavor_name_or_id`      | str          | The name or id of the flavor in which the new instance has to be created. |
| `nic_list`      | str          | Required. A list of networks to which the instance's interface should be attached. |                      
| `deploy_timeout`      | str          | The amount of time the module should wait for the instance to get into active state..                   |
| `deploy_userdata`      | str          | Opaque blob of data which is made available to the instance.  |   
| `availability_zone_name`      | str          | The availability zone in which to create the server. |
| `key_name_shown_on_powervc`      | str          | The key pair name to be used when creating an instance. |

Example Playbooks
----------------
```
- name: Deploy a vm
  hosts: powervc 
  tasks:
    - include_role:
        name: deploy_vm_via_powervc
      vars:
        vm_name: 'Abc' 
        image_name_or_id: 'image1'
        nic_list: [{
                "fixed_ip": "9.5.163.102",
                "net-name": "net-163"
            }]

```

License
-------

Apache-2.0
