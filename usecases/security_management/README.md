# Overview for security management use case

**-----------------------------------------**



The playbooks in this directory provide you the samples that you could directly use or do your modifications.

Contents will be continuously added and enhanced.



These playbooks focus on security compliance checks. Right now, they are just simple examples. More contents will be provided in recent months basing on the security compliance checking suggestions from CIS IBM i Benchmark documentation. Please regularly check this directory under devel branch.



# Playbook introduction

**---------------------**

**main.yml** - All other playbooks in this directory are included in main.yml. If you run this playbook, it actually will kick off the execution of all the other playbooks.



**manage_system_values.yml** - This playbook aims to check security-related system values. The checks in the playbook all pick the suggestion from CIS IBM i Benchmark documentation about system value settings.  Two separate yaml files for checking and remediating, three modes provided.

- system_value_check.yml - does system value check, compared with expected values.

- system_value_remediation.yml - does remediation base on user input.



|        Mode         |                         Instructions                         |
| :-----------------: | :----------------------------------------------------------: |
|     Check only      | This mode only does compliance check. No change occurs.  Report saved to host under /tmp. |
|   Remediate only    | This mode provides a separate way to do remediation. It allows the user to do remediation after a comprehensive understanding of the report.  The path to the report is needed. |
| Check and Remediate | This mode does compliance check first, then remediate immediately base on the check report. |

**manage_user_profiles.yml** - This playbook provides user profile setting check leveraging ibmi_user_compliance_check module and ibmi_sql_query module.

- user_profile_check.yml - does user profile compliance check.

- user_profile_remediation.yml - gives remediation suggestions and does remediation base on user input.



|        Mode         |                         Instructions                         |
| :-----------------: | :----------------------------------------------------------: |
|     Check only      | This mode only does compliance check. No change occurs.  Report saved to host under /tmp. |
|   Remediate only    | This mode provides a separate way to do remediation. It allows the user to do remediation after a comprehensive understanding of the report.  The path to the report is needed. |
| Check and Remediate | This mode does compliance check first, then remediate immediately base on the check report. |

**manage_network_settings.yml** - This playbook checks one network attribute setting by calling "Retrieve Network Attributes (RTVNETA)" command.

**manage_object_authorities.yml** - This playbook aims to check object authorities. Currently, this is just a simple example of leveraging ibmi_object_authority module.

*More features or enhancements may be added in the future.*



# Usage

**---------------------**

ansible-playbook ./main.yml



Note: to turn off displaying skipped task/host entries in a task in the default callback, you can run "ANSIBLE_DISPLAY_SKIPPED_HOSTS=false ansible-playbook ./main.yml" instead.
