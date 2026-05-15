# Change Log

## v3.4.0 (2026-05-15)

This release focuses on supporting Ansible core 2.19 and adding new download and install functionality for IBM Concert to perform CVE patching on IBM i.

The collection is verified on Ansible core 2.19 with this release (modules, roles, and high usage playbooks and use cases are tested).

### New modules

- ibmi_download_fix_from_cloud: download fixes to a Linux server (non-IBM i server) using the cloud API to Electronic Fix Delivery (EFD). Currently this only supports save files. Virtual image support is planned for later this year once the cloud API supports virtual images.

### New roles

- sync_apply_individual_ptfs_local: transfer PTF save files and cover letters from the local Ansible control node to an IBM i target system, then load and apply the PTFs. This role is designed to work with PTFs downloaded via ibmi_download_fix_from_cloud module.

### Changes for supporting Ansible core 2.19

- Fixed Ansible lint failures and sanity test failures for Ansible core 2.19.

- Corrected conditional expressions in roles and use cases to properly evaluate to boolean values instead of relying on integer values.

- Fixed integration test cases with proper conditional expressions to prevent runtime errors.

- Corrected Jinja2 template usage in integration tests to avoid "untrusted template" errors by removing nested template expressions and using inline expressions in assert statements.

- Added default empty lists where needed/missing in conditionals.

### Bug fixes

- Fixed ibmi_fix_group_check module to properly grab all associated PTF information (product, apar, date) when using XML group PTF information, not just PTF IDs. This resolves issues with the check_ptf_groups_against_fix_repo role.

- Recognized new PTF prefixes SJ and MJ in ibmi_fix_check module. Github issue 230: <https://github.com/IBM/ansible-for-i/issues/230>.

- Minor fixes for ibmi_sync and ibmi_sync_files modules discovered during test execution.

### Testing improvements

- Ensured integration tests target Python 3.9 on IBM i nodes (until Python 3.13 target issue is resolved).

- Added 7.6 PTFs for various integration tests.

- Updated integration test assertions to handle changing error messages.

- Fixed assertion conditionals with explicit type usage and proper Jinja2 template syntax.

### Documentation

- Updated documentation for new ibmi_download_fix_from_cloud module.

- Added new script to build and install collection.

### Other changes

- Updated sample playbooks and use cases that had issues.

- Various corrections to playbooks exercised in Ansible LUG workshop.

- Minor fixes for building and publishing the collection.

## v3.3.0 (2025-07-09)

This release focuses on minor improvements to make more collection modules idempotent.

### New modules

- ibmi_subsystem - manage a subsystem with various operations including display, start, end, and restart. Consolidate subsystem functionality to a single module and follow idempotency with the subsystem state (e.g., starting an active subsystem will return success and perform no action).

### Deprecated features

- ibmi_display_subsystem is deprecated and will be removed in a year. Use ibm.power_ibmi.ibmi_subsystem with 'display' operation instead.
- ibmi_end_subsystem is deprecated and will be removed in a year. Use ibm.power_ibmi.ibmi_subsystem with 'end' operation instead.
- ibmi_start_subsystem is deprecated and will be removed in a year. Use ibm.power_ibmi.ibmi_subsystem with 'start' operation instead.

### Bug fixes

- Changes to make ibmi_user_and_group module idempotent.
  Github issue 150: <https://github.com/IBM/ansible-for-i/issues/150>
- Fixes for some Ansible lint and Python lint errors.

### Documentation

- Note current issue with running Python 3.13 on an IBM i target node; Github issue 229: <https://github.com/IBM/ansible-for-i/issues/229>. Users must use Python 3.9 on IBM i target nodes for now.
- Note that users of Ansible core 2.15 should remain at collection version 3.2.0 due to changes with the ibmi_reboot module or else move to Ansible core 2.16 or higher.

## v3.2.1 (2025-04-08)

The collection is verified on Ansible core 2.17 and 2.18 with this release.

Ansible core 2.17 is only an option with a non IBM i control node
because of the jump in IBM i Python support to version 3.13 from version 3.9
without any intermediate levels. Ansible core 2.17 requires Python levels
from 3.10 to 3.12 on the control node.

Ansible core 2.18 requires Python levels from 3.11 to 3.13 on the control node,
which allows supporting an IBM i control node with python 3.13.

Please refer to the Ansible core support matrix at <https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html> for full
details on Ansible core and Python level compatibility with control and target nodes.

### Changes for supporting Ansible core 2.17 and 2.18

- Clean up Jinja2 spacing in numerous YAML files to remove ansible-lint warnings that Redhat asked to be cleaned up for next release.

- Remove use of yum module and instead use raw or command module to invoke yum because the yum module was removed from Ansible version 2.17.

- Fix ansible sanity test pylint failures with Ansible 2.18 (use before assignment).

### Changes to resolve testing issues

- Fix ibmi_reboot module current date/time calls to use a non-deprecated interface.

- Roll back ibmi_cl_command integration test to an older version that properly tests the ibmi_cl_command module instead of testing ibmi_copy module.

- Add new TC to ibmi_download_fix to exercise optional image catalog parameter. Also reduce timeout for a TC to ensure failure. Jinja 2 template error fixes.

- Fixing Jinja 2 template errors in various integration tests cases.

- Fixng TCs and skipping some broken TCs (fix later) in various integration tests.

- With the ibmi_at test, we now use an additional argument with RMVJOBSCDE to ensure full clean-up.

- Various fixes with ibmi_display_fix test that include new 7.4 PTFs.

### Bug fixes

- Fix ibmi_download fix module handling of optional image_catalog parameter.
  GitHub issue 221: <https://github.com/IBM/ansible-for-i/issues/221>.

- Fix incorrect FQCN in role fix_repo_lv1_find_individual_ptf reference to module ibmi_fix_repo_lv1.

- Fix typo for role variable example in role fix_repo_lv1_find_individual_ptf README.

## v3.2.0 (2024-12-06)

This release includes minor enhancements requested from github issues and/or provided in contributed code
from github PRs, along with bug fixes to resolve various github issues.

The modifications for this release include:

- Adding bash setup and OSS package install playbooks to the collection.
  - Contribution from github PR #215 (<https://github.com/IBM/ansible-for-i/pull/215>) with minor tweaks.

- Adding image catalog parameter to ibmi_download_fix module.
  - Incorporate github PR #214 (<https://github.com/IBM/ansible-for-i/pull/214>) to update ibmi_download_fix, and perform integration test corrections for ibmi_download_fix.

- Corrections to Ansible install documentation.
  - Update Ansible installation instructions from github PR #213 (<https://github.com/IBM/ansible-for-i/pull/213>) along with some additional tweaks.

- Fix for github issue #205 (<https://github.com/IBM/ansible-for-i/issues/205>) and test case clean up.
  - Adding fully qualified collection name for module references in various plugins to follow Ansible best practices.

- Adding delete option for fix_repo_download_apply_individual_ptfs.
  - Request from github issue #203 (<https://github.com/IBM/ansible-for-i/issues/203>).

- Enhancement for sync_apply_ptf_group role.
  - Github PRs #175 (<https://github.com/IBM/ansible-for-i/pull/175>) and #176 (<https://github.com/IBM/ansible-for-i/pull/176>).
  - Add additional role variable "apply_type" to the sync_apply_ptf_group role to allow control of when the group fix is applied.

- ibmi_cl_command module enhancement: github issue #165 (<https://github.com/IBM/ansible-for-i/issues/165>).
  - Allow more flexibility with the ibmi_cl_command to force the output to follow 5250 convention with a new input parameter "is_cmd5250".
  - Incorporates PR #184 (<https://github.com/IBM/ansible-for-i/pull/184>).

- Fix for issue #209 (<https://github.com/IBM/ansible-for-i/issues/209>) with role fix_repo_download_apply_individual_ptfs.
  - Incorporates PR #210 (<https://github.com/IBM/ansible-for-i/pull/210>).

- ibmi_fix_group_check module change to use PSP XML files with latest fix information.
  - Use XML files provided by PSP instead of scraping PSP html pages such as the PTF group landing page and any fix specific pages.
  - This resolves github issue #204 (<https://github.com/IBM/ansible-for-i/issues/204>).

## v3.1.0 (2024-07-24)

The collection is verified on Ansible core 2.16 with this release.
The collection now requires Ansible core levels 2.15 or 2.16 and drops Ansible level 2.14.

Note that the use of Ansible 2.16 requires Python 3.10 or higher on the Ansible
control node, while IBM i currently only includes python packages
up to version 3.9. This IBM i limitation requires staying with Ansible 2.15
if you are using an IBM i control node with the provided IBM i Python packages;
however, this does not impact IBM i target nodes which may run at lower levels of Python.
There should be a higher level of Python provided by IBM i later this year that will
resolve this limitation.

The Redhat AAP collection download image will now exclude some content that relies on
uncertified collection functionality as detailed below.
The Ansible Galaxy build image for download will continue to provide the entire collection.

The modifications for this release include:

### Changes for supporting Ansible 2.16 and dropping Ansible 2.14

- Changes to handle deprecated items in tests for Ansible 2.16 such as
  - Replacing the use of include with include_tasks / import_tasks.
  - Removing Jinja2 template usage in conditionals.

- Meta file updates to set the minimum Ansible level to 2.15 for the collection
  because Redhat has recently dropped Ansible 2.14 support.

- Update documentation.

- Adding in minor test fixes or work arounds to resolve test case issues.

- Updating the README with additional sections as required by Redhat.

### Updates to avoid uncertified collections due to Redhat requirements

- Remove reference to uncertified community.general.git_config
  module and use builtin command instead.

- Generate a separate collection build image for Redhat AAP download that avoids including
  references to the uncertified collection openstack.cloud by excluding the
  PowerVC related roles and the CICD use cases that rely on the PowerVC roles.

## v3.0.0 (2024-05-10)

This release includes the final changes to ensure continued compliance with the Redhat certification process.
This is a disruptive API change with the collection roles that impacts the naming of all the role variables and
role return variables. All user playbooks using roles must be updated in order to work with this release.
Each role README file fully documents the new role variable names and the naming convention used is noted below.

The following changes are included with this release:

- Ansible lint clean up for fix management use cases.
- Clean-up of role variables to use a global naming convention that prepends the role name to each role variable
  and role return variable.   For example, with the apply_ptf role, the variable "to_be_applied_list"
  is now "apply_ptf_to_be_applied_list". This convention is followed 99% of the time. This change with roles required
  updating all the use cases and also the role integration tests.
- Numerous fixes for the role integration tests along with updating PTFs used in the tests. This is still a work in progress.
- Various fixes for issues that became apparent with the global role variable naming.

## v2.0.2 (2024-04-24)

This release primarily addresses the fix check breakage from the recent PSP web site updates.

### Bug Fixes

- Fix for github issue 191: <https://github.com/IBM/ansible-for-i/issues/191>
  - Revise parsing of PSP group PTF web page for recent change that broke the fix check modules.
  - Future work is needed to properly account for individual PTF dependencies with new web page format
    along with other lower level information.

- Fix for github issue 194: <https://github.com/IBM/ansible-for-i/issues/194>
  - Increase timeout for fix check modules from 10 to 60 seconds to account for increased PSP web page access time
    that was causing false failures in roles that depend on fix check.

- Fix the level 1 fix management module ibmi_fix_repo_lv1
  - Revise parsing of sha256 file that is used for checksums when generating a new database fix entry for a refresh action.
    The file format has changed slightly and we were erroneously skipping valid fixes that were using the new format.

## v2.0.1 (2024-03-05)

This release includes a number of fixes along with code clean-up to continue the Redhat certification of the collection.

The plan for the next release is to complete the Redhat certification clean-up by modifying the role variables to follow the convention
of the role name prepended to the role variable, e.g., the role sync_apply_ptf_group with role variable src_host will rename the role variable to sync_apply_ptf_group_src_host. This future change with role variables will obviously impact user playbooks that utilize the collection roles.

### Bug Fixes

- Fix for github issue 163: <https://github.com/IBM/ansible-for-i/issues/163>
  - Binary dependency should reference python3 instead of python.
  - Add collection dependencies in requirements file.

- Fixes for github issue #177 for sync_apply_ptf_group: <https://github.com/IBM/ansible-for-i/issues/177>
  - Correct role documentation examples for sync_apply_ptf_group and sync_apply_ptf_group_networkinstall for the ptf information.
  - Fix a bug in sync_apply_ptf_group with incorrect server variable for delegation

- Fix for role sync_apply_individual_ptfs_lv1.
  - Found a common bug for role sync_apply_individual_ptfs_lv1 as previously found for the role sync_apply_ptf_group in github issue 177.

- Fix for github issue 146. Resolve deprecated warnings: <https://github.com/IBM/ansible-for-i/issues/146>
  - Remove use of deprecated call _remote_checksum and instead use _execute_remote_stat, which impacts a few modules.

### Code clean-up

- Ansible lint clean up for most of the uses cases
  - Cleaning up cicd-cli, ibmi_services, and security_management use cases.
  - Clean up use cases for cicd-tower, towerapi, and db2mirror_setup_via_powervc.

### Documentation

- Fix documentation for various modules (github issue 179): <https://github.com/IBM/ansible-for-i/issues/179>
  - Correct botched collection name in various module examples that are used in the module documentation.

- Documentation clean up for ibmi_tcp_server_service: <https://github.com/IBM/ansible-for-i/issues/164>
  - Clarify the example for restarting ssh server with ibmi_tcp_server_service to address github issue 164.

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
