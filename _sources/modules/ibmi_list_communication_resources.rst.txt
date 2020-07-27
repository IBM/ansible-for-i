
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_list_communication_resources.pyy

.. _ibmi_list_communication_resources_module:


ibmi_list_communication_resources -- Retrieves all the communication resources information in the system.
=========================================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_list_communication_resources`` module list the communication resources information of the system.





Parameters
----------


     
dummy
  No options needed for this module.


  | **required**: false
  | **type**: str




Examples
--------

.. code-block:: yaml+jinja

   
   - name: list the RDMA resource ports information
     ibmi_list_communication_resources:






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

            
      
      
                              
       resource_info
        | the resources information
      
        | **returned**: when rc as 0
        | **type**: str
        | **sample**: [{'ADAPTER_ADDRESS': '2', 'CARD_POSITION': '', 'DEFAULT_MAC_ADDRESS': 'FAB7D940D220', 'EXPANDED_SERIAL_NUMBER': '00-00000', 'FRAME_ID': '', 'IO_BUS_ADDRESS': '208', 'LAN speed': '0000000000000003', 'LOCATION_CODE': 'U8286.42A.10C4DAT-V14-C2-T1', 'PART_NUMBER': '', 'PORT_NUMBER': '0', 'RESOURCE_NAME': 'CMN06', 'SERIAL_NUMBER': '00-00000', 'SUPPORTS_LINK_AGGREGATION': '02', 'SYSTEM_BOARD_NUMBER': '2', 'SYSTEM_BUS_NUMBER': '255', 'SYSTEM_CARD_NUMBER': '2'}, {'ADAPTER_ADDRESS': '3', 'CARD_POSITION': '', 'DEFAULT_MAC_ADDRESS': '0AF685E6D2C4', 'EXPANDED_SERIAL_NUMBER': '00-00000', 'FRAME_ID': '', 'IO_BUS_ADDRESS': '208', 'LAN speed': '0000000000000003', 'LOCATION_CODE': 'U8286.42A.10C4DAT-V14-C3-T1', 'PART_NUMBER': '', 'PORT_NUMBER': '0', 'RESOURCE_NAME': 'CMN05', 'SERIAL_NUMBER': '00-00000', 'SUPPORTS_LINK_AGGREGATION': '02', 'SYSTEM_BOARD_NUMBER': '3', 'SYSTEM_BUS_NUMBER': '255', 'SYSTEM_CARD_NUMBER': '3'}]

            
      
      
                              
       rc
        | The return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
      
      
                              
       job_log
        | The command standard error.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       "{u\u0027dftccsid\u0027: u\u002737\u0027, u\u0027jobnbr\u0027: u\u0027029163\u0027, u\u0027xmlhint\u0027: u\u002701567:7905:Table ANSIBLE_T2 in QGPL created but was not jour\u0027, u\u0027jobuser\u0027: u\u0027QUSER\u0027, u\u0027usrlibl\u0027: u\u0027QGPL QTEMP QDEVELOP QBLDSYS QBLDSYSR\u0027, u\u0027jobname\u0027: u\u0027QSQSRVR\u0027, u\u0027curuser\u0027: u\u0027CHANGLE\u0027, u\u0027version\u0027: u\u0027XML Toolkit 2.0.2-dev\u0027, u\u0027xmlhint1\u0027: u\u002701567:7905:Table ANSIBLE_T2 in QGPL created but was not jour\u0027, u\u0027syslibl\u0027: u\u0027QSYS QSYS2 QHLPSYS QUSRSYS\u0027, u\u0027jobipcskey\u0027: u\u0027FFFFFFFF\u0027, u\u0027paseccsid\u0027: u\u00270\u0027, u\u0027ccsid\u0027: u\u002737\u0027}"
            
      
        
