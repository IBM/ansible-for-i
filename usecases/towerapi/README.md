# Overview for Ansible Tower API use case

The playbooks in this directory provide you the samples to set up a workflow in Ansible Tower for CI/CD process.

The implementation is still experimental and may be continuously updated.

## Input parameters

* **prefix**
  * **Type**: String
  * **Description**: Naming the Ansible Tower projects/templates to be created.
* **pre_cleanup**
  * **Type**: String
  * **Description**: When set to Yes, the existed projects/templates with the same names will be deleted before running.
* **tower_url**
  * **Type**: String
  * **Description**: The URL of your Ansible Tower server.
* **tower_username**
  * **Type**: String
  * **Description**: The user name of your Ansible Tower server.
* **tower_password**
  * **Type**: String
  * **Description**: The password of your Ansible Tower server.
* **git_url**
  * **Type**: String
  * **Description**: The URL of your github repository with CI/CD playbooks.
* **playbook_names**
  * **Type**: String
  * **Description**: The playbooks' names (use space as separator) of your github repository with CI/CD playbooks.
* **git_repo_url**
  * **Type**: String
  * **Description**: The URL of your github repository with building playbooks.
* **git_branch**
  * **Type**: String
  * **Description**: The branch of your github repository with building playbooks.
* **github_user_name**
  * **Type**: String
  * **Description**: The user name of your github repository with building playbooks.
* **github_access_token**
  * **Type**: String
  * **Description**: The [access token](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token) of your github repository with building playbooks.
* **build_with_stmfs**
  * **Type**: String
  * **Description**: Are you building your app with STMFs or PF members? Yes for SMTFs, No for PF members.
* **cleanup**
  * **Type**: String
  * **Description**: Do you want to clean up after each build (Yes/No)?
* **provision**
  * **Type**: String
  * **Description**: Do you want to provision a new VM for building (Yes/No)?
* **build_system_user**
  * **Type**: String
  * **Description**: Your IBM i build machine user name.
* **build_system_pass**
  * **Type**: String
  * **Description**: Your IBM i build machine user password.

Below input parameters are prompted only if you're going to build your application on an existing building system (`provision` is set to `No`).

* **host_name**
  * **Type**: String
  * **Description**: Your build machines' IP addresses (use space as separator for multiple hosts)

Below input parameters are only prompted when you're going to create a new compute instance for building. (`provision` is set to `Yes`).

* **powervc_host**
  * **Type**: String
  * **Description**: Your powervc host for provisioning.
* **powervc_admin**
  * **Type**: String
  * **Description**: Your powervc administrator's name for provisioning.
* **powervc_admin_password**
  * **Type**: String
  * **Description**: Your powervc administrator's password for provisioning.
* **powervc_project**
  * **Type**: String
  * **Description**: The project name in powervc host for provisioning.
* **project_domain**
  * **Type**: String
  * **Description**: The project domain in powervc host for provisioning.
* **user_domain**
  * **Type**: String
  * **Description**: The user domain in powervc host for provisioning.
* **verify_cert**
  * **Type**: String
  * **Description**: Do you want to verify cert in provisioning? (Yes/No)
* **network**
  * **Type**: String
  * **Description**: The name or ID of a network to attach this instance.
* **image_name_or_id**
  * **Type**: String
  * **Description**: The image name or ID in powervc host for provisioning.
* **flavor_name_or_id**
  * **Type**: String
  * **Description**: The flavor name or ID in powervc host for provisioning.
* **deploy_timeout**
  * **Type**: Interger
  * **Description**: The timeout(seconds) value of provisioning VM in the powervc host.

## Playbooks

1. main.yml - The entry point of the program.
2. login.yml - Login to the Ansible Tower server to get the access token.
3. add_inventory.yml - add an Ansible Tower inventory for building systems.
4. add_hosts.yml - add Ansible Tower hosts to the previously created inventory.
5. add_credential.yml - add Ansible Tower credentials to log in to the building systems.
6. add_github_token.yml - add Ansible Tower credentials to download building playbooks from github repository.
7. add_project.yml - add an Ansible Tower project defining the github repository and building playbooks.
8. add_workflow.yml - add an Ansible Tower workflow template and set some Ansible Tower survey specs.
9. add_job.yml - add Ansible Tower job templates to the previously created workflow.
10. run_workflow.yml - run the Ansible Tower workflow.
11. show_result.yml - show the running result of the Ansible Tower workflow.
12. cleanup.yml - revoke the Ansible Tower server access token.