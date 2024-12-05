
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_mirror_warm_clone_activity.py

.. _ibmi_mirror_warm_clone_activity_module:


ibmi_mirror_warm_clone_activity -- Performs suspend and resume activity for warm clone.
=======================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The :literal:`ibmi\_mirror\_warm\_clone\_activity` module performs the suspend and resume activity for a warm clone to reach a quiesce point before the clone and resume from that point after clone.
- The setup source node must reach a quiesce point before tracking changes can begin.
- If a quiesce point cannot be reached within the specified timeout, then the setup process will not proceed.





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


     
operation
  Specifies the activity to be performed for a warm clone.


  | **required**: True
  | **type**: str
  | **choices**: suspend, resume


     
suspend_timeout
  Specifies the the number of seconds timeout value to allow for the suspend operation to complete.


  | **required**: false
  | **type**: int
  | **default**: 300




Examples
--------

.. code-block:: yaml+jinja

   
   - name: suspend the system for a warm clone to do a clone
     ibm.power_ibmi.ibmi_mirror_warm_clone_activity:
       operation: suspend






See Also
--------

.. seealso::

   - :ref:`ibmi_mirror_setup_source_module`


  

Return Values
-------------


   
                              
       msg
        | The message that describes the error or success
      
        | **returned**: always
        | **type**: str
        | **sample**: Error occurred when retrieving the mirror state

            
      
      
                              
       rc
        | The return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
      
        
