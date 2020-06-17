..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/IBM/ansible-for-i/tree/ansible_collection_beta/plugins/modules/ibmi_fix.py

.. _ibmi_fix_module:

ibmi_fix -- Install, remove or query an individual fix or a set of fixes on to IBM i system.
============================================================================================


.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_fix`` module install fixes to target IBM i system.
- The installation file of the fixes should be in the format of save file.
- The fixes are normally known as PTFs for IBM i users.



Parameters
----------


     
delayed_option
  Controls whether the PTF is delayed apply or not


  | **required**: false
  | **type**: str
  | **default**: *NO
  | **choices**: *YES, *NO


     
fix_list
  PTF list that will be applied to the IBM i system.


  | **required**: false
  | **type**: list
  | **elements**: str
  | **default**: [u'*ALL']


     
fix_omit_list
  The list of PTFs that will be omitted.

  The key of the dict should be the product ID of the fix that is omitted.


  | **required**: False
  | **type**: list
  | **elements**: str


     
operation
  The operation for the fix, the options are as follows

  load_and_apply will load the PTF and apply the PTF

  load_only will only load the PTF by LODPTF

  remove_and_delete will remove the PTF and delete the PTF

  remove_only will only remove the PTF

  delete_only will only delete the PTF

  query will return the specific PTF status


  | **required**: false
  | **type**: str
  | **default**: load_and_apply
  | **choices**: load_and_apply, apply_only, load_only, remove, query


     
product_id
  Product identifier to which PTFs are applied.


  | **required**: false
  | **type**: str


     
save_file_lib
  The library name of the save file to be installed.


  | **required**: false
  | **type**: str
  | **default**: QGPL


     
save_file_object
  The object name of the save file to be installed.


  | **required**: false
  | **type**: str


     
temp_or_perm
  Controls whether the PTF will be permanent applied or temporary applied.


  | **required**: false
  | **type**: str
  | **default**: *TEMP
  | **choices**: *TEMP, *PERM



Examples
--------

.. code-block:: yaml+jinja

   
   - name: Remove a single PTF
     ibmi_fix:
       product_id: '5770DBM'
       delayed_option: "*NO"
       temp_or_perm: "*PERM"
       operation: 'remove'
       fix_list:
         - "SI72223"
   - name: Install a single PTF
     ibmi_fix:
       product_id: '5770DBM'
       save_file_object: 'QSI72223'
       save_file_lib: 'QGPL'
       delayed_option: "*NO"
       temp_or_perm: "*TEMP"
       operation: 'load_and_apply'
       fix_list:
         - "SI72223"
   - name: query ptf
     ibmi_fix:
       operation: 'query'
       fix_list:
         - "SI72223"
         - "SI70819"



Notes
-----

.. note::
   Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)


See Also
--------

.. seealso::

   - :ref:`ibmi_fix_imgclg_module`


Return Values
-------------


   
                              
       stderr_lines
        | The task standard error split in lines
      
        | **returned**: When error occurs.
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF2111:Library TESTLIB already exists."]
            
      
      
                              
       end
        | The task execution end time
      
        | **returned**: When rc is zero
        | **type**: str
        | **sample**: 2019-12-02 11:07:54.064969

            
      
      
                              
       stdout
        | The task standard output
      
        | **returned**: When error occurs.
        | **type**: str
        | **sample**: CPC2102: Library TESTLIB created

            
      
      
                              
       rc
        | The task return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       start
        | The task execution start time
      
        | **returned**: When rc is zero
        | **type**: str
        | **sample**: 2019-12-02 11:07:53.757435

            
      
      
                              
       stderr
        | The task standard error
      
        | **returned**: When error occurs.
        | **type**: str
        | **sample**: CPF2111:Library TESTLIB already exists

            
      
      
                              
       delta
        | The task execution delta time
      
        | **returned**: When rc is zero
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       stdout_lines
        | The task standard output split in lines
      
        | **returned**: When error occurs.
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPC2102: Library TESTLIB created."]
            
      
        
