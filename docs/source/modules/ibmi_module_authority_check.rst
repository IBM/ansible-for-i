
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_module_authority_check.py

.. _ibmi_module_authority_check_module:


ibmi_module_authority_check -- Check the authority of executing a module.
=========================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_module_authority_check`` module can do the module authority check.
- This module returns the authority of executing the module specified in the parameter





Parameters
----------


     
modulelist
  Specifies a list of module which are checked the authority.


  | **required**: True
  | **type**: list
  | **elements**: str




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Do module authority check
     ibmi_user_compliance_check:
          modulelist:
           - 'ibmi_copy'
           - 'ibmi_display_subsystem'
           - 'ibmi_invaild_module'










Return Values
-------------


   
                              
       rc
        | The return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       authority_result
        | The result set of required authories of module.
      
        | **returned**: always
        | **type**: dict      
        | **sample**:

              .. code-block::

                       {"ibmi_copy": ["*ALLOBJ"], "ibmi_display_subsystem": ["*JOBCTL"], "ibmi_invaild_module": "this module name is invaild."}
            
      
        
