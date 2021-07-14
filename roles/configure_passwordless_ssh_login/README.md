configure_passwordless_ssh_login
=========
Confgure passwordless ssh login.

Role Variables
--------------

| Variable              | Type          | Description                                      |
|-----------------------|---------------|--------------------------------------------------|
| `target_user`      | str          | Required. The username on the remote host whose authorized_keys file will be modified.                    |
| `public_key`      | str          | Required. The SSH public key, as a string.   |

Example Playbooks
----------------
```
- name: Add ssh public key to remote host
  hosts: ibmi 

  roles:
    - role: configure_passwordless_ssh_login
      vars: 
        target_user: "{{ansible_ssh_user}}"
        public_key: "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDMsx23avIaCwUIYHE+5mFSspzXIVphaWOVGU3+OxcYH11ijazhYW+DXv0tYIkcNn3rsLzFccbpQI3FJYwTFDAzTe6NBcLL9pI3EE4M+KQWxGNHOMWB+5zSbFP3qRd4sb+vzxqeas7ihVW/TtR3Z5448aTC4XYa86BeA1GM17xrTNXNYwU37Pu1G5IQrM3YY7dH+943LIDcrH86QgReEluwj5pppEmfGpqNaAH/2lvxzhX/14al8RbHxULF0qU1k+gs8yOpIfX9TqTn6qiielW6xVOrEr3TP4FspL+I/LWkLBxg0+vFrjH/RKWKc9B9EDI4Dm8wqW4MqAe8GXftOY/H ansiuser@localhost"
```

License
-------

Apache-2.0
