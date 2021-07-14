Overview
--------
These roles are part of IBM i collections which can be installed directly from Galaxy or Red Hat Automation Hub. 
The example below shows how to use playbook to invoke these roles. Please find details of each role by navigating into the subdirectories.  


Example Playbook
----------------
```
- name: IBM i check, load and apply a set of PTFs
  hosts: ibmi
  gather_facts: no
  collections:
    - ibm.power_ibmi

  vars:
    check_ptf_list:
      - {'ptf_number':'SI70544', 'product_id':'5770SS1', 'savf_name':'QSI70544'}
      - {'ptf_number':'SI70931', 'product_id':'5770SS1', 'savf_name':'QSI70931'}
      - {'ptf_number':'SI72305', 'product_id':'5770SS1', 'savf_name':'QSI72305'}
      - {'ptf_number':'SI71691', 'product_id':'5770SS1', 'savf_name':'QSI71691'}
    
  roles:
    - role: check_ptf
    - role: load_ptf
      vars: 
        to_be_loaded_list: '{{to_be_load}}'
  
  tasks:
    - include_role:
        name: apply_all_loaded_ptfs
      when: "'success' in excution_status.values() | join(' ')"
```

License
-------

Apache-2.0
