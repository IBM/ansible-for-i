
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_download_fix_status.py

.. _ibmi_download_fix_status_module:


ibmi_download_fix_status -- Checking whether the fix downloading complete
=========================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The :literal:`ibmi\_download\_fix\_status` module check the downloading fix's status.





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


     
order_list
  The  order list of download ptf group


  | **required**: True
  | **type**: list
  | **elements**: str




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Check the fix order status
     ibm.power_ibmi.ibmi_download_fix_status:
       order_list:
         - '2029604329'
         - '2020579181'

   - name: Check the fix order status with become user
     ibm.power_ibmi.ibmi_download_fix_status:
       order_list:
         - '2029604329'
         - '2020579181'
       become_user: 'USER1'
       become_user_password: 'yourpassword'




Notes
-----

.. note::
   Only support English language ibm i system, language ID 2924.

   See SNDPTFORD command for more information.





  

Return Values
-------------


   
                              
       status
        | The fix downloading status.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"complete_time": "2020-11-01 00:59:58", "download_status": "DOWNLOADED", "file_path": "/QIBM/UserData/OS/Service/ECS/PTF/2029604329", "order_id": "2029604329"}, {"complete_time": "UNKNOWN", "download_status": "UNKNOWN", "file_path": "UNKNOWN", "order_id": "2020579181"}]
            
      
      
                              
       rc
        | The SQL command action return code. 0 means success.
      
        | **returned**: always
        | **type**: int
      
        
