Overview for security management use case
-----------------------------------------

The playbooks in this directory provides you the samples that you could directly use or do your own modifications. 
Contents will be continuously added and enhanced. 

These playbooks focus on security compliance checks. Right now they are just simple examples. More contents will be provided in recent months basing on the security compliance checking suggestions from CIS IBM i Benchmark documentation. Please regularly check this directory under devel branch.

Playbook introduction
---------------------
main.yml - All other playbooks in this directory are included in main.yml. If you run this playbook, it actually will kick off the execution of all the other playbooks.

manage_network_settings.yml - This playbook checks one network attribute setting by calling retrieve network attribute command. More checkings will be added into this playbook in the future.

manage_object_authorities.yml - This playbook aims to check object authorities. Currently there is just one simple example of leveraging ibmi_object_authority module. More stuffs will be added in the future.

manage_system_values.yml - This playbook aims to check security related system values. The checks in the playbook all pick the suggestion from CIS IBM i Benchmark documentation about system value settings. More stuffs will be added in the future.

manage_user_profiles.yml - This playbook provides user profile setting check leveraging ibmi_user_compliance_check module and ibmi_sql_query module. More stuffs will be added in the future.  