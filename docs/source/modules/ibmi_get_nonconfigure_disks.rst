..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/IBM/ansible-for-i/tree/ansible_collection_beta/plugins/modules/ibmi_get_nonconfigure_disks.py

.. _ibmi_get_nonconfigure_disks_module:

ibmi_get_nonconfigure_disks -- Get all nonconfigure disks on target IBMi node
=============================================================================


.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Get all nonconfigure disks on target IBMi node
- For non-IBMi targets, no need



Parameters
----------


     
joblog
  If set to ``true``, append JOBLOG to stderr/stderr_lines.


  | **required**: false
  | **type**: bool



Examples
--------

.. code-block:: yaml+jinja

   
   - name: get all nonconfigure disks
     ibmi_get_nonconfigure_disks:
       joblog: True






Return Values
-------------


   
                              
       start
        | The command execution start time
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:53.757435

            
      
      
                              
       end
        | The command execution end time
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:54.064969

            
      
      
                              
       delta
        | The command execution delta time
      
        | **returned**: always
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       disks
        | all un-configure disks
      
        | **returned**: always
        | **type**: str
        | **sample**: DMP002 DMP019 DMP005 DMP014 DMP031 DMP012 

            
      
      
                              
       rc
        | The command return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
      
      
                              
       rc_msg
        | Meaning of the return code
      
        | **returned**: always
        | **type**: str
        | **sample**: Success to get all un-configure disks.

            
      
        
