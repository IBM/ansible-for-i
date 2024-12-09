
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_fix_product_check.py

.. _ibmi_fix_product_check_module:


ibmi_fix_product_check -- Check the software product installation status for a fix
==================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The :literal:`ibmi\_fix\_product\_check` module checks if the software product of a fix is installed.





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
  The list of the PTF.


  | **required**: True
  | **type**: list
  | **elements**: dict




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Get PTF products installation status
     ibm.power_ibmi.ibmi_fix_product_check:
       ptfs:
         - {
           "product": "5770UME",
           "ptf_id": "SI67856",
           "release": "V1R4M0"
           }
         - {
           "product": "5733SC1",
           "ptf_id": "SI73751",
           "release": "V7R2M0"
           }






See Also
--------

.. seealso::

   - :ref:`ibmi_fix_module`


  

Return Values
-------------


   
                              
       ptfs_with_product_installed
        | The PTF list which the product was installed.
      
        | **returned**: always, empty list if error occurred or none of the product was installed.
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"product": "5770UME", "ptf_id": "SI67856", "release": "V1R4M0"}]
            
      
      
                              
       ptfs_without_product_installed
        | The PTF list which the product was not installed.
      
        | **returned**: always, empty list if all of the products were installed.
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"product": "5733SC1", "ptf_id": "SI73751", "release": "V7R2M0"}]
            
      
      
                              
       rc
        | The return code (0 means success, non-zero means failure).
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       msg
        | The error or success message.
      
        | **returned**: always
        | **type**: str
        | **sample**: Success to check software product installation status

            
      
        
