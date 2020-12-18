present_ip_interface
=========
The role is to present an ip interface and make it active. The workflow is that:
1. If the internet_address does exist, make it active.
2. If the internet_address doesn't exist, create it based on the given line_description. 
3. If the given line_description doesn't exist, create it
4. If the next_hop is provided, create a router based on it.

Role Variables
--------------

| Variable              | Type          | Required  | Default Value | Description                                      |
|-----------------------|---------------|-----------|----------------|-----------------------|
| `ip_address`      | str          | True  |     |The internet address that will be added. |
| `line_description`      | str          | False |     |The name of the line description associated with the new interface.  If the value is not provided but an IP interface need to be created, then a default line description 'DEF + Resource name of Ethernet Port', for example, DEFCMN03 is used.                      |
| `vlanid`               | str          | False |  *NONE   |The virtual LAN identifier of the associated line. |
| `netmask`           | str          | False |     |Defines the subnet mask. |
| `associatedLocalInterface` | str          | False |  *NONE   | Use this parameter to associate the IPv4 interface being added with an existing local IPv4 TCP/IP interface.                      |
| `typeOfService`       | str          | False | *NORMAL    |The type of service specifies how the internet hosts and routers should make trade-offs. |
| `maxTransmissionUnit` | str          | False | *LIND    | Specifies the maximum size (in bytes) of IP datagrams that can be transmitted through this interface. |
| `autoStart`            | str          | False | *YES    | Specifies whether the interface is automatically started. Default                     |
| `preferredInterface`   | str           | False |  *NONE   | A list of preferred IPv4 interfaces that are to be used with the IPv4 interface being added for proxy. |
| `textDescription`            | False |     | *BLANK         | Specifies text that briefly describes the interface. |
| `secToWait`      | int          | False |  0   | The number of seconds that the module waits after executing the task before returning the information of the internet address..                      |
| `extraParams`          | str           | False | ''  |  The extra parameters that the user wants to pass into ibmi_tcp_interface module. |
| `location_code_of_ethernet_port`      | str          | False |  ''    |The location code of the ethernet port that will be used to find or create line description. |
| `resource_name_of_ethernet_port`      | str          | False |  ''   |The resouce name of the ethernet port that will be used to find or create line description.                      |
| `mac_address_of_ethernet_port`      | str          | False |  ''   |The mac address of the ethernet port that will be used to find or create line description.                      |
| `addition_options_for_CRTLINETH`     | str          | False |  　''   |Addtion options for CRTLINETH. |
| `route_destination`      | str          | False  |  *DFTROUTE   |Specifies the route destination being added. |
| `next_hop`      | str          | False |     |Specifies the internet address of the next system (gateway) on the route.                          .                      |
| `addition_options_for_ADDTCPRTE`               | str          | False |  ''  |Addtion options for ADDTCPRTE. |

Example Playbooks
----------------
```
- name: To acitive an existing IP interface
  hosts: ibmi 

  roles:
    - role: present_ip_interface
      vars:
        ip_address: '10.10.10.10'
```

```
- name: To activate an IP interface, if it doesn't exist, create one interface then activate it using line description DEFCMN03. If DEFCMN03 doesn't exist, create it based on CMN03 firstly. 
  hosts: ibmi

  roles:
    - role: present_ip_interface
      vars:
        ip_address: '10.10.10.10'
        netmask: '255.255.255.0'
        resource_name_of_ethernet_port: 'CMN03'
```

```
- name: To activate an IP interface, if it doesn't exist, create one interface then activate it using line description ETHLINE1. If ETHLINE1 doesn't exist, create it based on CMN03 firstly.  
  hosts: ibmi

  roles:
    - role: present_ip_interface
      vars:
        ip_address: '10.10.10.10'
        netmask: '255.255.255.0'
        line_description: 'ETHLINE1'
        resource_name_of_ethernet_port: 'CMN03'
```

```
- name: To activate an IP interface, if it doesn't exist, create one interface then activate it using line description DEFCMN03. If DEFCMN03 doesn't exist, create it based on CMN03 firstly. Create a new router whose description is '*DFTROUTE' and next hop is '10.10.10.1'
  hosts: ibmi

  roles:
    - role: present_ip_interface
      vars:
        ip_address: '10.10.10.10'
        netmask: '255.255.255.0'
        resource_name_of_ethernet_port: 'CMN03'
        next_hop: '10.10.10.1'
```

License
-------

Apache-2.0
