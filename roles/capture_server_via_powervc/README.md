capture_server_via_powervc
=========
Capture a virtual server via PowerVC to generate a deployable image.

Role Variables
--------------

| Variable              | Type          | Description                                      |
|-----------------------|---------------|--------------------------------------------------|
| `image_name`      | str          | Specifies the prefix of the new generated image. The final image name is composed by image_name + '_' + a random number. So that the image name can be unique.                   |
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
        image_name: 'ibmi-image'
        vm_name: 'vm-to-be-captured'

```

```
- name: IBM i apply all loaded ptfs
  hosts: powervc

  roles:
    - role: capture_server_via_powervc
      vars:
        image_name: 'ibmi-image'
        vm_name: 'vm-to-be-captured'
```

Returned Variables
----------------
```
"openstack_image": {
    "architecture": "ppc64",
    "checksum": null,
    "container_format": null,
    "created": "2020-12-24T09:57:13Z",
    "created_at": "2020-12-24T09:57:13Z",
    "decision_id": "31",
    "direct_url": null,
    "disk_format": null,
    "endianness": "big-endian",
    "file": "/v2/images/c7dbfd5a-d893-4960-8dff-e48d1aac4cd6/file",
    "hypervisor_type": "phyp",
    "id": "c7dbfd5a-d893-4960-8dff-e48d1aac4cd6",
    "image_type": "snapshot",
    "instance_uuid": "5c6d55e9-9242-4e3b-88fa-85c51c74d6a5",
    "is_protected": false,
    "is_public": false,
    "location": {
        "cloud": "",
        "project": {
            "domain_id": null,
            "domain_name": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
            "id": "a38cb70f74404c79939592d7f2739474",
            "name": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"
        },
        "region_name": "",
        "zone": null
    },
    "locations": [],
    "memory_mb": "2048",
    "metadata": {
        "architecture": "ppc64",
        "decision_id": "31",
        "endianness": "big-endian",
        "hypervisor_type": "phyp",
        "image_type": "snapshot",
        "instance_uuid": "5c6d55e9-9242-4e3b-88fa-85c51c74d6a5",
        "memory_mb": "2048",
        "os_distro": "ibmi",
        "os_hidden": false,
        "schema": "/v2/schemas/image",
        "storage_connectivity_group_id": "3ddc30e8-4fac-4b73-8286-3b784ef00c36",
        "user_id": "0688b01e6439ca32d698d20789d52169126fb41fb1a4ddafcebb97d854e836c9",
        "vcpus": "0.5"
    },
    "minDisk": 0,
    "minRam": 0,
    "min_disk": 0,
    "min_ram": 0,
    "name": "ibmi-image_5983592",
    "os_distro": "ibmi",
    "os_hidden": false,
    "owner": "a38cb70f74404c79939592d7f2739474",
    "properties": {
        "architecture": "ppc64",
        "decision_id": "31",
        "endianness": "big-endian",
        "hypervisor_type": "phyp",
        "image_type": "snapshot",
        "instance_uuid": "5c6d55e9-9242-4e3b-88fa-85c51c74d6a5",
        "memory_mb": "2048",
        "os_distro": "ibmi",
        "os_hidden": false,
        "schema": "/v2/schemas/image",
        "storage_connectivity_group_id": "3ddc30e8-4fac-4b73-8286-3b784ef00c36",
        "user_id": "0688b01e6439ca32d698d20789d52169126fb41fb1a4ddafcebb97d854e836c9",
        "vcpus": "0.5"
    },
    "protected": false,
    "schema": "/v2/schemas/image",
    "size": 0,
    "status": "queued",
    "storage_connectivity_group_id": "3ddc30e8-4fac-4b73-8286-3b784ef00c36",
    "tags": [],
    "updated": "2020-12-24T09:57:13Z",
    "updated_at": "2020-12-24T09:57:13Z",
    "user_id": "0688b01e6439ca32d698d20789d52169126fb41fb1a4ddafcebb97d854e836c9",
    "vcpus": "0.5",
    "virtual_size": 0,
    "visibility": "private"
}
```
License
-------

Apache-2.0