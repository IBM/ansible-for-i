apply_all_loaded_ptfs
=========
Apply all loaded ptfs, then perform an IPL if auto_ipl is set to true and at least one PTF requests an IPL for permanent applied or temporary applied.

Role Variables
--------------

| Variable              | Type          | Description                                      |
|-----------------------|---------------|--------------------------------------------------|
| `temp_or_perm`      | str          | Controls whether the loaded PTFs will be permanent applied or temporary applied. Value can be  '*TEMP' or '*PERM'. Default value is '*TEMP'.                     |
| `delayed_option`      | str          | Controls whether the PTF is delayed apply or not. Value can be '*YES', '*NO' or '*IMMDLY'. Default value is '*IMMDLY'.                      |
| `auto_ipl`          | bool           | Controls whether an immediate reboot will be launched automatically if at least one ptf requests an IPL for permanent applied or temporary applied. Default value is false. |

Example Playbooks
----------------
```
- name: IBM i apply all loaded ptfs
  hosts: ibmi 

  roles:
    - role: apply_all_loaded_ptfs
```

```
- name: IBM i apply all loaded ptfs
  hosts: ibmi

  roles:
    - role: apply_all_loaded_ptfs
      vars:
        temp_or_perm: '*PERM'
        delayed_option: '*NO' 
        auto_ipl: true
```

License
-------

Apache-2.0
