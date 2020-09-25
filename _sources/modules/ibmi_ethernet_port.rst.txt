
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_ethernet_port.py

.. _ibmi_ethernet_port_module:


ibmi_ethernet_port -- Retrieves all the ethernet ports(both virtual and physical)information on the system.
===========================================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_ethernet_port`` module lists the ethernet ports information of the system.





Parameters
----------


     
become_user
  The name of the user profile that the IBM i task will run under.

  Use this option to set a user with desired privileges to run the task.


  | **required**: false
  | **type**: str


     
become_user_password
  Use this option to set the password of the user specified in ``become_user``.


  | **required**: false
  | **type**: str


     
operation
  The ethernet port operation.


  | **required**: false
  | **type**: str
  | **default**: display
  | **choices**: display




Examples
--------

.. code-block:: yaml+jinja

   
   - name: list all the ethernet port information
     ibmi_ethernet_port:




Notes
-----

.. note::
   The following PTFs are required for getting the default MAC address of a port, V7R1M0 SI64305, MF63437, MF63430 V7R2M0 SI63691, MF99106 V7R3M0 SI63671, MF99202

   Field Descriptions refer to https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/apis/qgyrhri.htm



See Also
--------

.. seealso::

   - :ref:`ibmi_cl_command_module`



Return Values
-------------


   
                              
       msg
        | The message that descript the error or success
      
        | **returned**: always
        | **type**: str
        | **sample**: Error occurred when retrieving the mirror state

            
      
      
                              
       ethernet_ports
        | the ethernet ports information
      
        | **returned**: when rc as 0
        | **type**: str
        | **sample**: [{'ADAPTER_ADDRESS': '2', 'CARD_POSITION': '', 'DEFAULT_MAC_ADDRESS': 'FAB7D940D220', 'EXPANDED_SERIAL_NUMBER': '00-00000', 'FRAME_ID': '', 'IO_BUS_ADDRESS': '208', 'LAN speed': '0000000000000003', 'LOCATION_CODE': 'U8286.42A.10C4DAT-V14-C2-T1', 'PART_NUMBER': '', 'PORT_NUMBER': '0', 'RESOURCE_NAME': 'CMN06', 'SERIAL_NUMBER': '00-00000', 'SUPPORTS_LINK_AGGREGATION': '02', 'SYSTEM_BOARD_NUMBER': '2', 'SYSTEM_BUS_NUMBER': '255', 'SYSTEM_CARD_NUMBER': '2'}, {'ADAPTER_ADDRESS': '3', 'CARD_POSITION': '', 'DEFAULT_MAC_ADDRESS': '0AF685E6D2C4', 'EXPANDED_SERIAL_NUMBER': '00-00000', 'FRAME_ID': '', 'IO_BUS_ADDRESS': '208', 'LAN speed': '0000000000000003', 'LOCATION_CODE': 'U8286.42A.10C4DAT-V14-C3-T1', 'PART_NUMBER': '', 'PORT_NUMBER': '0', 'RESOURCE_NAME': 'CMN05', 'SERIAL_NUMBER': '00-00000', 'SUPPORTS_LINK_AGGREGATION': '02', 'SYSTEM_BOARD_NUMBER': '3', 'SYSTEM_BUS_NUMBER': '255', 'SYSTEM_CARD_NUMBER': '3'}]

            
      
      
                              
       rc
        | The return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
      
        
