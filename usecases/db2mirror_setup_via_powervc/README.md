Overview for db2mirror_setup_via_powervc use case
-----------------------------------------

The playbooks in this directory provide samples that show how to set up a DB2Mirror pair via PowerVC. 

Pre-requisites
1. The source node is being managed by a PowerVC server where openstacksdk needs to be installed.
2. All required products have been installed on the source node. Refer to https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/db2mi/db2mplanningsoftware.htm
3. All IPs of the source node, which are associating with NRG links but have not been configured on the source node yet, must be attached to the source VM via PowerVC firstly. For example, assuming 11.11.11.11 is an IP defined in nrgLinkPairs as the internet_address of the source node, if 11.11.11.11 is not shown in the returned list of CFGTCP -> OPTION 1, then a user must attach a vNIC whose IP address is 11.11.11.11 on PowerVC manually before running main.yml.
4. SSH server must be started.

Playbook introduction
---------------------
main.yml - All other playbooks in this directory are included in main.yml. If you run this playbook, it actually will kick off the execution of all the other playbooks.

add_nrg_links.yml - Added all designated nrg link to NRG group.

check_lpps.yml - This playbook aims to check the license info of dependent licensed program product. 

configure_ip.yml - This playbook aims to make sure the IP interfaces assigned to NRG links be active on the source node.

Inventory introduction
---------------------
hosts.ini - This inventory defines the format of provided information of powervc server and the source node. Only the ansible_ssh_host, ansible_ssh_user and ansible_ssh_pass of powervc and source node need to be changed. 

Required Variables
--------------

| Variable              | Type          | Description                                                          |
|-----------------------|---------------|---------------------------------------------------------------------------------------------------------|
| `addNRGLinks`         | list          | The list of NRG links. Element in the list is a dictionary. One required key is 'copy_internet_address', and one is 'copy_network_name' and the last key is 'source_internet_address'.                        |
| `copyNodeTCPIP`    | dictionary    | Specifies the TCP IP info that will be configured on the copy node. There are two required keys 'copy_internet_address' and 'copy_network_name'. 'copy_network_name' must be picked up from the list of 'Network' on PowerVC.  |
| `sourceVmNameOnPowerVC`    | str    | The vm name of source node displayed on PowerVC             | 

Optional Variables
--------------

| Variable              | Type          |Default value | Description                            |
|-----------------------|---------------|--------------|-------------------------------------------------------------------------------------------------|
| `secondaryNode`    | str    | 'db2mcopy' | The name of copy node.  |
| `cloneType`    | str    | 'WARM'|Valid choices are 'WARM', 'COLD'             | 
| `timeServer`    | str    | 'TIME.COM' | The DNS name of the NTP server to be added to the configuration.             |
| `defaultInclusionState`    | str    | 'EXCLUDE'|The default inclusion state setting will be used.          | 
| `suspendTimeout`    | int    | 300 | Specifies the number of seconds timeout value to allow for the suspend operation to complete.             | 
| `verify_cert`    | bool    | true |Specifies if verifies the SSL certificate of PowerVC. If the value of verify_cert is false the SSL certificate of PowerVC won't be verified.         | 
| `flavor`    | str    | 'tiny' | Specifies the compute template which is used to deploy a new VM on PowerVC.|   
| `userdata`    | str    | '' | Specifies the user data which will be passed to cloud-init to customized the deployed VM.|  
| `availability_zone`    | str    | '' | Specifies the host group where the copy node will be deployed.| 

Examples:
--------------
ansible-playbook -i hosts.ini main.yml -vvv --extra-vars "{    
    'nrgLinkPairs': [{'copy_internet_address': '9.5.162.8', 
         'copy_network_name': 'net-163', 
         'source_internet_address': '9.5.163.102'},
      {'copy_internet_address': '9.5.163.21', 
         'copy_network_name': 'net-162', 
         'source_internet_address': '9.5.162.20',
        }],  
        'copyNodeTCPIP': {'copy_internet_address': '9.5.163.101', 'copy_network_name': 'net-163'},
        'sourceVmNameOnPowerVC': MIRRORS
        }"