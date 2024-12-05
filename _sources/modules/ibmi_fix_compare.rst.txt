
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_fix_compare.py

.. _ibmi_fix_compare_module:


ibmi_fix_compare -- Verify whether the PTFs are installed.
==========================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The :literal:`ibmi\_fix\_compare` module compare the PTF list to target system to see whether the PTF is applied.





Parameters
----------


     
become_user
  The name of the user profile that the IBM i task will run under.

  Use this option to set a user with desired privileges to run the task.


  | **required**: false
  | **type**: str


     
become_user_password
  Use this option to set the password of the user specified in :literal:`become\_user`.


  | **required**: false
  | **type**: str


     
ptfs
  The list of the PTF number.


  | **required**: True
  | **type**: list
  | **elements**: str




Examples
--------

.. code-block:: yaml+jinja

   

   - name: Check the PTFs' status
     ibm.power_ibmi.ibmi_fix_compare:
       ptfs:
         - 'SI12345'
         - 'SI67890'




Notes
-----

.. note::
   Ansible hosts file need to specify ansible\_python\_interpreter=/QOpenSys/pkgs/bin/python3





  

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
        | **sample**: 1

            
      
      
                              
       verified
        | The number of PTFs which has been retrieved
      
        | **returned**: always.
        | **type**: int
        | **sample**: 1

            
      
      
                              
       unexpected
        | The number of PTFs which are not installed
      
        | **returned**: always.
        | **type**: int
        | **sample**: 1

            
      
      
                              
       ptf_info
        | PTF group information.
      
        | **returned**: When rc is 1.
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"PTF_IDENTIFIER": "SI12345", "PTF_STATUS": "Not installed"}, {"PTF_ACTION_PENDING": "NO", "PTF_ACTION_REQUIRED": "NONE", "PTF_CREATION_TIMESTAMP": "2015-02-18T16:58:46", "PTF_IDENTIFIER": "SI12345", "PTF_IPL_ACTION": "NONE", "PTF_IPL_REQUIRED": "IMMEDIATE", "PTF_PRODUCT_ID": "57XXXXX", "PTF_SAVE_FILE": "YES", "PTF_STATUS": "NOT LOADED", "PTF_STATUS_TIMESTAMP": null}]
            
      
        
