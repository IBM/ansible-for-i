
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_fix_group_check.py

.. _ibmi_fix_group_check_module:


ibmi_fix_group_check -- Retrieve the latest PTF group information from PSP server.
==================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_fix_group_check`` module retrieve latest PTF group information from PSP(Preventive Service Planning) server.
- Refer to https://www.ibm.com/support/pages/node/667567 for more details of PSP.
- ALL PTF groups or specific PTF groups are supported.





Parameters
----------


     
groups
  The list of the PTF groups number.


  | **required**: False
  | **type**: list
  | **elements**: str
  | **default**: ['\*ALL']




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Check specific PTF groups
     ibmi_fix_group_check:
       groups:
         - "SF12345"




Notes
-----

.. note::
   Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3






Return Values
-------------


   
                              
       stderr
        | The task standard error
      
        | **returned**: always
        | **type**: str
        | **sample**: PTF groups SF12345 does not exist

            
      
      
                              
       rc
        | The task return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
      
      
                              
       count
        | The number of PTF groups which has been retrieved
      
        | **returned**: always.
        | **type**: int
        | **sample**: 1

            
      
      
                              
       group_info
        | PTF group information.
      
        | **returned**: When rc is zero.
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"PTF_GROUP_LEVEL": "46", "PTF_GROUP_NUMBER": "SF99115", "RELEASE": "R610", "RELEASE_DATE": "09/28/2015", "TITLE": "610 IBM HTTP Server for i"}]
            
      
        
