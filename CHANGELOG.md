# Change Log

## v2.0.0 (2023-11-22)

With this release the collection now requires ansible-core version 2.14 or 2.15 on the Ansible server / control node. This also requires having Python 3.9 on the Ansible server / control node. The IBM i target nodes may still run at a lower level of Python 3. These changes are necessary for continued Redhat certification of the collection and also for Ansible Galaxy.

### Bug Fixes

- Fixes for ansible 2.14 and 2.15 (primarily sanity test related).
- Fix present_ip_interface role which was broken due to some incorrect var names defined in defaults/main.yml.

### Miscellaneous

- Modifications for ansible-lint in production mode that are a work in progress for the collection (rest of changes in following release).
  - Completely clean up playbooks.
  - Extensive clean up of roles (but additional work required to change role variables / API for all roles).

### Documentation

- Document new requirements for ansible-core version 2.14+ and python version 3.9. Add new Ansible install instructions for an IBM i Ansible server.
- Add CHANGELOG file

## v1.9.2 (2023-11-21)

This is a patch release with code and documentation fixes.

### Bug Fixes

- Fix for github issue #153:  HTTP Error 403-Forbidden, being returned from IBM service web servers with the fix check modules http/https requests (<https://github.com/IBM/ansible-for-i/issues/153>).
- Fix for github issue #157: fix_group_check dead URL (<https://github.com/IBM/ansible-for-i/issues/157>).
- Fix in check_pfs role for incorrect reference to temporarily_applied_list.

### Miscellaneous

- Update checking for playbooks/ibmi-sysval-sample.yml.
- Update load_ptf return option in log_load_fail_info.yml (OPTION_NOT_INSTALLED_OR_ALREADY_INSTALLED).

### Documentation

- Document required configuration of *SRVLAN for network install (usecases/fix_management/sync_apply_ptf_group_networkinstall.yml, roles/sync_apply_ptf_group_networkinstall/README.md).
