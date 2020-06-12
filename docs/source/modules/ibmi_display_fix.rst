..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/IBM/ansible-for-i/tree/ansible_collection_beta/plugins/modules/ibmi_display_fix.py

.. _ibmi_display_fix_module:

ibmi_display_fix -- display the PTF(Program Temporary Fix)information and also get the requisite information for the PTF
========================================================================================================================


.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_display_fix`` module display the information of the PTF and also get the requisite PTF



Parameters
----------


     
joblog
  If set to ``true``, output the avaiable JOBLOG even the rc is 0(success).


  | **required**: false
  | **type**: bool


     
product
  Specifies the product for the PTF


  | **required**: True
  | **type**: str


     
ptf
  Specifies which PTF is shown for the specified product.


  | **required**: True
  | **type**: str


     
release
  Specifies the release level of the PTF in one of the following formats.

  VxRyMz, for example, V7R2M0 is version 7, release 2, modification 0

  vvrrmm, this format must be used if the version or release of the product is greater than 9.

  For example, 110300 is version 11, release 3, modification 0.


  | **required**: True
  | **type**: str



Examples
--------

.. code-block:: yaml+jinja

   
   - name: Get PTF information
     ibmi_display_fix:
       product: '5770SS1'
       ptf: 'SI70439'
       release: 'V7R4M0'




See Also
--------

.. seealso::

   - :ref:`ibmi_fix_module`


Return Values
-------------


   
                              
       stderr_lines
        | The command standard error split in lines
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF2111:Library TESTLIB already exists."]
            
      
      
                              
       job_log
        | the job_log
      
        | **returned**: always
        | **type**: str
        | **sample**: [{'TO_MODULE': 'QSQSRVR', 'TO_PROGRAM': 'QSQSRVR', 'MESSAGE_TEXT': 'Printer device PRT01 not found.', 'FROM_MODULE': '', 'FROM_PROGRAM': 'QWTCHGJB', 'MESSAGE_TIMESTAMP': '2020-05-20-21.41.40.845897', 'FROM_USER': 'CHANGLE', 'TO_INSTRUCTION': '9369', 'MESSAGE_SECOND_LEVEL_TEXT': 'Cause . . . . . :   This message is used by application programs as a general escape message.', 'MESSAGE_TYPE': 'DIAGNOSTIC', 'MESSAGE_ID': 'CPD0912', 'MESSAGE_LIBRARY': 'QSYS', 'FROM_LIBRARY': 'QSYS', 'SEVERITY': '20', 'FROM_PROCEDURE': '', 'TO_LIBRARY': 'QSYS', 'FROM_INSTRUCTION': '318F', 'MESSAGE_SUBTYPE': '', 'ORDINAL_POSITION': '5', 'MESSAGE_FILE': 'QCPFMSG', 'TO_PROCEDURE': 'QSQSRVR'}]

            
      
      
                              
       stdout
        | The command standard output
      
        | **returned**: always
        | **type**: str
        | **sample**: CPC2102: Library TESTLIB created

            
      
      
                              
       stderr
        | The command standard error
      
        | **returned**: always
        | **type**: str
        | **sample**: CPF2111:Library TESTLIB already exists

            
      
      
                              
       rc
        | The command return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       stdout_lines
        | The command standard output split in lines
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPC2102: Library TESTLIB created."]
            
      
      
                              
       requisite_ptf
        | The requisite PTFs and type
      
        | **returned**: always
        | **type**: dict      
        | **sample**:

              .. code-block::

                       {"SI70030": "*PREREQ", "SI71080": "*COREQ", "SI71135": "*COREQ", "SI71137": "*COREQ", "SI71138": "*PREREQ", "SI71139": "*PREREQ"}
            
      
      
                              
       ptf_info
        | the ptf information
      
        | **returned**: always
        | **type**: str
        | **sample**: [{'PTF_ACTION_REQUIRED': 'NONE', 'PTF_PRODUCT_DESCRIPTION': 'IBM i', 'PTF_IS_RELEASED': 'NO', 'PTF_IPL_ACTION': 'NONE', 'PTF_MINIMUM_LEVEL': '00', 'PTF_PRODUCT_RELEASE_LEVEL': 'V7R4M0', 'PTF_SUPERSEDED_BY_PTF': '', 'PTF_TECHNOLOGY_REFRESH_PTF': 'NO', 'PTF_PRODUCT_LOAD': '5050', 'PTF_ACTION_PENDING': 'NO', 'PTF_IDENTIFIER': 'SI73329', 'PTF_IPL_REQUIRED': 'IMMEDIATE', 'PTF_CREATION_TIMESTAMP': '2020-05-14-22.08.22.000000', 'PTF_PRODUCT_ID': '5770SS1', 'PTF_COVER_LETTER': 'YES', 'PTF_TEMPORARY_APPLY_TIMESTAMP': '2020-05-14-22.39.06.000000', 'PTF_PRODUCT_OPTION': '*BASE', 'PTF_MAXIMUM_LEVEL': '00', 'PTF_SAVE_FILE': 'YES', 'PTF_RELEASE_LEVEL': 'V7R4M0', 'PTF_LOADED_STATUS': 'APPLIED', 'PTF_ON_ORDER': 'NO', 'PTF_STATUS_TIMESTAMP': '2020-05-14-22.39.06.000000'}]

            
      
        
