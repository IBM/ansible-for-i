capture_server_via_powervc
=========
Capture a virtual server via PowerVC to generate a deployable image.

Role Variables
--------------

| Variable              | Type          | Description                                      |
|-----------------------|---------------|--------------------------------------------------|
| `image_name`      | str          | Specifies name of new generated image.                     |
| `vm_name`      | str          | Specifies the vm name or id which is to be captured.                      |


Example Playbooks
----------------
```
- name: Capture a vm
  hosts: powervc 
  tasks:
    - name: Capture source node to get an image
      include_role: 
        name: capture_server_via_powervc
      vars:
        image_name: 'New-image'
        vm_name: 'vm-to-be-captured'

```

```
- name: IBM i apply all loaded ptfs
  hosts: powervc

  roles:
    - role: capture_server_via_powervc
      vars:
        image_name: 'New-image'
        vm_name: 'vm-to-be-captured'
```

License
-------

Apache-2.0
