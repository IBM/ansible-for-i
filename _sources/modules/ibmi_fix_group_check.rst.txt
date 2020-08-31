
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_fix_group_check.pyy

.. _ibmi_fix_group_check_module:


ibmi_fix_group_check -- Retrieve the latest PTF group information from PSP server.
==================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_fix_group_check`` module retrieve latest PTF group information from PSP server.
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

   
   - name: Check all the PTF groups
     ibmi_fix_group_check:
       groups:
         - "*ALL"

   - name: Check specific PTF groups
     ibmi_fix_group_check:
       groups:
         - "SF12345"




Notes
-----

.. note::
   Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)






Return Values
-------------


   
                              
       stderr
        | The task standard error
      
        | **returned**: When error occurs.
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

                       [{"ptf_group_level": "46", "ptf_group_number": "SF99115", "release": "R610", "release_date": "09/28/2015", "title": "610 IBM HTTP Server for i"}]
            
      
        
