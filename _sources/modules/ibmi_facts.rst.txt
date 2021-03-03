
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_facts.py

.. _ibmi_facts_module:


ibmi_facts -- Gathering ibmi facts
==================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Gathering the target ibmi system facts.





Parameters
----------


     
filter
  If supplied, only return facts that match this shell-style (fnmatch) wildcard.


  | **required**: false
  | **type**: str
  | **default**: \*




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Return ibmi_facts
     ibm.power_ibmi.ibmi_facts:








  

Return Values
-------------


   
                              
       ansible_facts
        | ibmi specific facts to add to ansible_facts.
      
        | **returned**: always
        | **type**: dict
              
   
                              
        system_name
          | Contains information about the current system name.
      
          | **returned**: when operating system answer fact is present
          | **type**: str
          | **sample**: DB2MB1PA

            
      
      
                              
        version_release
          | Contains information about the operating system version and release.
      
          | **returned**: when operating system answer fact is present
          | **type**: float      
          | **sample**:

              .. code-block::

                       7.4
            
      
      
                              
        system_info
          | Contains information about the current server.
      
          | **returned**: when operating system answer fact is present
          | **type**: dict      
          | **sample**:

              .. code-block::

                       {"CONFIGURED_CPUS": 4, "CONFIGURED_MEMORY": 10240, "HOST_NAME": "DB2MB1PA.RCH.STGLABS.IBM.COM", "OS_NAME": "IBM i", "OS_RELEASE": "4", "OS_VERSION": "7", "TOTAL_CPUS": 24, "TOTAL_MEMORY": 24576}
            
      
      
                              
        system_values
          | Contains information about system values.
      
          | **returned**: when operating system fact is present
          | **type**: dict      
          | **sample**:

              .. code-block::

                       {"QADLTOTJ": 30}
            
      
      
                              
        system_catalogs
          | Contains one row for each relational database that a user can connect to.
      
          | **returned**: when operating system fact is present
          | **type**: list      
          | **sample**:

              .. code-block::

                       [{"CATALOG_ASPGRP": "", "CATALOG_ASPNUM": "", "CATALOG_NAME": "J106F917", "CATALOG_STATUS": "AVAILABLE ", "CATALOG_TEXT": "Entry added by system", "CATALOG_TYPE": "LOCAL  "}]
            
      
      
                              
        system_status
          | Returns a single row containing details about the current partition.
      
          | **returned**: when operating system fact is present
          | **type**: dict      
          | **sample**:

              .. code-block::

                       {"ACTIVE_JOBS_IN_SYSTEM": 233, "ACTIVE_JOB_TABLE_ENTRIES": 233, "ACTIVE_THREADS_IN_SYSTEM": 1695, "ATTENTION_LIGHT": "OFF", "AVAILABLE_JOB_TABLE_ENTRIES": 63, "AVERAGE_CPU_RATE": 100.0, "AVERAGE_CPU_UTILIZATION": 0.1, "BOUND_HARDWARE_THREADS": "YES", "CONFIGURED_CPUS": 4, "CPU_SHARING_ATTRIBUTE": "UNCAPPED", "CURRENT_CPU_CAPACITY": 1.8, "CURRENT_TEMPORARY_STORAGE": 5883, "DEDICATED_PROCESSORS": "NO", "DEFINED_INTERACTIVE_CAPACITY": 0.0, "DEFINED_MEMORY": 10240, "DEFINED_PROCESSING_CAPACITY": 1.8, "DEFINED_VARIABLE_CAPACITY_WEIGHT": 128, "DEFINED_VIRTUAL_PROCESSORS": 4, "DISPATCH_LATENCY": 11000000.0, "DISPATCH_WHEEL_ROTATION_TIME": 10000000.0, "ELAPSED_CPU_SHARED": "", "ELAPSED_CPU_UNCAPPED_CAPACITY": 0.0, "ELAPSED_CPU_USED": 0.1, "ELAPSED_TIME": 1, "HARDWARE_MULTITHREADING": "YES", "HOST_NAME": "DB2MB1PA", "INTERACTIVE_CAPACITY": 0.0, "INTERACTIVE_CPU_TIME": 86000000.0, "INTERACTIVE_CPU_TIME_ABOVE_THRESHOLD": 0.0, "INTERACTIVE_JOBS_IN_SYSTEM": 0.0, "INTERACTIVE_THRESHOLD": 100.0, "IN_USE_JOB_TABLE_ENTRIES": 1590, "IPL_MODE": "NORMAL", "IPL_TYPE": "B", "JOBLOG_PENDING_JOB_TABLE_ENTRIES": 79, "JOBQ_JOB_TABLE_ENTRIES": 0, "JOURNAL_CACHE_WAIT_TIME": 30, "JOURNAL_RECOVERY_COUNT": 250000, "MACHINE_MODEL": " MME", "MACHINE_TYPE": "9119", "MAIN_STORAGE_SIZE": 10269696, "MAXIMUM_CPU_UTILIZATION": 0.41, "MAXIMUM_INTERACTIVE_CAPACITY": 0.0, "MAXIMUM_JOBS_IN_SYSTEM": 163520, "MAXIMUM_LICENSED_PROCESSING_CAPACITY": 128.0, "MAXIMUM_MEMORY": 24576, "MAXIMUM_PHYSICAL_PROCESSORS": 128, "MAXIMUM_PROCESSING_CAPACITY": 12.0, "MAXIMUM_TEMPORARY_STORAGE_USED": 6005, "MAXIMUM_VIRTUAL_PROCESSORS": 24, "MEMORY_INCREMENT": 256, "MINIMUM_CPU_UTILIZATION": 0.0, "MINIMUM_INTERACTIVE_CAPACITY": 0.0, "MINIMUM_MEMORY": 10240, "MINIMUM_PROCESSING_CAPACITY": 0.05, "MINIMUM_REQUIRED_PROCESSING_CAPACITY": 0.05, "MINIMUM_VIRTUAL_PROCESSORS": 1, "NUMBER_OF_PARTITIONS": 38, "OUTQ_JOB_TABLE_ENTRIES": 1278, "PARTITION_GROUP_ID": 32778, "PARTITION_ID": 10, "PARTITION_NAME": "db2mb1pA", "PERMANENT_256MB_SEGMENTS": 0.0, "PERMANENT_4GB_SEGMENTS": 0.0, "PERMANENT_ADDRESS_RATE": 0.007, "PERMANENT_JOB_STRUCTURES_AVAILABLE": 63, "PHYSICAL_PROCESSORS": 128, "PHYSICAL_PROCESSORS_SHARED_POOL": 64, "PROCESSING_CAPACITY": 1.8, "PROCESSING_CAPACITY_INCREMENT": 0.01, "RESTRICTED_STATE": "NO", "SERIAL_NUMBER": " 106F917", "SHARED_PROCESSOR_POOL_ID": 0, "SQL_CPU_UTILIZATION": "", "SYSTEM_ASP_STORAGE": 104988, "SYSTEM_ASP_USED": 37.52, "TEMPORARY_256MB_SEGMENTS": 0.0, "TEMPORARY_4GB_SEGMENTS": 0.0, "TEMPORARY_ADDRESS_RATE": 0.007, "TEMPORARY_JOB_STRUCTURES_AVAILABLE": 26, "THREADS_PER_PROCESSOR": 8, "TOTAL_AUXILIARY_STORAGE": 104988, "TOTAL_CPU_TIME": 1202739000000.0, "TOTAL_JOBS_IN_SYSTEM": 1591, "TOTAL_JOB_TABLE_ENTRIES": 1654, "UNALLOCATED_INTERACTIVE_CAPACITY": 0.0, "UNALLOCATED_PROCESSING_CAPACITY": 0.0, "UNALLOCATED_VARIABLE_CAPACITY_WEIGHT": 0, "UNUSED_CPU_TIME_SHARED_POOL": "", "VARIABLE_CAPACITY_WEIGHT": 128, "VIRTUAL_PROCESSORS": 4}
            
      
      
                              
        tcpip_info
          | Contains TCP/IP information for the current host connection.
      
          | **returned**: when operating system fact is present
          | **type**: list      
          | **sample**:

              .. code-block::

                       [{"AUTOSTART": "YES", "CHANGE_STATUS": "START", "CONFIGURED_MAXIMUM_TRANSMISSION_UNIT": "576", "CONNECTION_TYPE": "IPV4", "CURRENT_PROXY_AGENT_LINE": "", "CURRENT_PROXY_AGENT_LINE_VIRTUAL_LAN_ID": "", "DAD_MAX_TRANSMITS": "", "DHCP_CREATED": "NO", "DHCP_DYNAMIC_DNS_UPDATES": "", "DHCP_LEASE_EXPIRATION": "", "DHCP_LEASE_OBTAINED": "", "DHCP_SERVER_ADDRESS": "", "DHCP_SERVER_UNIQUE_ID": "", "DHCP_USE_UNIQUE_ID": "", "DIRECTED_BROADCAST_ADDRESS": "", "HOST_ADDRESS": "0.0.0.1", "INTERFACE_FULL_NAME": "", "INTERFACE_LINE_TYPE": "NONE", "INTERFACE_SOURCE": "", "INTERFACE_STATUS": "ACTIVE", "INTERFACE_TEXT": "", "INTERFACE_TYPE": "NONBROADCAST", "INTERNET_ADDRESS": "127.0.0.1", "LAST_CHANGE_TIMESTAMP": "2021-01-14 09:22:18", "LINE_DESCRIPTION": "*LOOPBACK", "MAXIMUM_TRANSMISSION_UNIT": "576", "NETWORK_ADDRESS": "127.0.0.0", "NETWORK_FULL_NAME": "", "ON_LINK": "", "PACKET_RULES": "NONE", "PREFERRED_INTERFACE_DEFAULT_ROUTE": "NO", "PREFERRED_INTERFACE_LIST": "", "PREFERRED_PHYSICAL_LINE_LIST": "", "PREFIX_LENGTH": "", "PROXY_ARP_ALLOWED": "", "PROXY_ARP_ENABLED": "NO", "SERVICE_TYPE": "NORMAL", "SUBNET_MASK": "255.0.0.0", "VIRTUAL_LAN_ID": "NONE"}]
            
      
      
                              
        group_ptf_info
          | Contains information about the group PTFs for the server.
      
          | **returned**: when operating system fact is present
          | **type**: list      
          | **sample**:

              .. code-block::

                       [{"COLLECTED_TIME": "2021-01-20 00:55:37.446951", "PTF_GROUP_DESCRIPTION": "HIGH AVAILABILITY FOR IBM I", "PTF_GROUP_LEVEL": 4, "PTF_GROUP_NAME": "SF99666", "PTF_GROUP_STATUS": "INSTALLED", "PTF_GROUP_TARGET_RELEASE": "V7R4M0"}, {"COLLECTED_TIME": "2021-01-20 00:55:37.446951", "PTF_GROUP_DESCRIPTION": "CUMULATIVE PTF PACKAGE C0121740", "PTF_GROUP_LEVEL": 20121, "PTF_GROUP_NAME": "SF99740", "PTF_GROUP_STATUS": "NOT INSTALLED", "PTF_GROUP_TARGET_RELEASE": "V7R4M0"}]
            
      
      
                              
        dns_info
          | Contains information about doamin net server(DNS).
      
          | **returned**: when operating system fact is present
          | **type**: list      
          | **sample**:

              .. code-block::

                       ["8.8.8.8", "9.9.9.9", "7.7.7.7"]
            
      
      
                              
        route_info
          | Contains information about IPv4 and IPv6 routes.
      
          | **returned**: when operating system fact is present
          | **type**: list      
          | **sample**:

              .. code-block::

                       [{"CONFIGURED_ROUTE_MAXIMUM_TRANSMISSION_UNIT": "", "CONNECTION_TYPE": "IPV4", "DUPLICATE": "", "EXPIRATION": "", "LAST_CHANGE_TIMESTAMP": "2021-01-14 09:22:26", "LOCAL_BINDING_INTERFACE": "192.168.55.154", "LOCAL_BINDING_INTERFACE_STATUS": "ACTIVE", "LOCAL_BINDING_LINE_DESCRIPTION": "ETHLINE", "LOCAL_BINDING_LINE_STATUS": "", "LOCAL_BINDING_LINE_TYPE": "ELAN", "LOCAL_BINDING_NETWORK_ADDRESS": "192.168.55.0", "LOCAL_BINDING_SUBNET_MASK": "255.255.255.0", "LOCAL_BINDING_TYPE": "STATIC", "LOCAL_BINDING_VIRTUAL_LAN_ID": "NONE", "NEXT_HOP": "*DIRECT", "PPP_AUTHENTICATION_USER_ID": "", "PPP_CONFIGURATION_PROFILE": "", "PPP_DIAL_ON_DEMAND_PROFILE": "", "PPP_INTERNET_ADDRESS": "", "PREFIX_LENGTH": "", "ROUTE_DESTINATION": "224.0.0.0", "ROUTE_MAXIMUM_TRANSMISSION_UNIT": "1500", "ROUTE_PRECEDENCE": 1, "ROUTE_PREFERENCE": "", "ROUTE_PROTOCOL": "", "ROUTE_SOURCE": "CFG", "ROUTE_STATUS": "YES", "ROUTE_TEXT": "", "ROUTE_TYPE": "DIRECT", "SERVICE_TYPE": "NORMAL", "SUBNET_MASK": "240.0.0.0"}]
            
      
        
      
        
