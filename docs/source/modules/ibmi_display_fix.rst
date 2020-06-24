..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/IBM/ansible-for-i/tree/ansible_collection_beta/plugins/modules/ibmi_display_fix.py

.. _ibmi_display_fix_module:

ibmi_display_fix -- Displays the PTF(Program Temporary Fix) information and also get the requisite PTFs information of the PTF
==============================================================================================================================


.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_display_fix`` module displays the information of the PTF and also get the requisite PTFs.
- Type of requisite values meaning refer to https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/apis/qpzrtvfx.htm#HDRPTFLLH2



Parameters
----------


     
joblog
  If set to ``true``, output the avaiable job log even the rc is 0(success).


  | **required**: false
  | **type**: bool


     
product
  Specifies the product ID for the PTF.


  | **required**: True
  | **type**: str


     
ptf
  Specifies which PTF is shown for the specified product.


  | **required**: True
  | **type**: str


     
release
  Specifies the release level of the PTF in one of the following formats, VxRyMz, for example, V7R2M0 is version 7, release 2, modification 0, vvrrmm, this format must be used if the version or release of the product is greater than 9. For example, 110300 is version 11, release 3, modification 0.


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


   
                              
       requisite_ptf_info
        | The requisite PTFs infomation.
      
        | **returned**: always, empty list if there is no requisite ptf
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"RELEASE_OF_REQUISITE": "V7R4M0", "REQUISITE_IS_CONDITIONAL": "0", "REQUISITE_IS_REQUIRED": "1", "REQUISITE_LOAD_ID": "5050", "REQUISITE_MAX_LEVLE": "00", "REQUISITE_MIN_LEVLE": "00", "REQUISITE_OPTION": "0000", "REQUISITE_PRODUCT_ID": "5770SS1", "REQUISITE_PTF_ID": "SI69832", "TYPE_OF_REQUISITE": "1"}, {"RELEASE_OF_REQUISITE": "V7R4M0", "REQUISITE_IS_CONDITIONAL": "0", "REQUISITE_IS_REQUIRED": "1", "REQUISITE_LOAD_ID": "5050", "REQUISITE_MAX_LEVLE": "00", "REQUISITE_MIN_LEVLE": "00", "REQUISITE_OPTION": "0000", "REQUISITE_PRODUCT_ID": "5770SS1", "REQUISITE_PTF_ID": "SI69837", "TYPE_OF_REQUISITE": "2"}, {"RELEASE_OF_REQUISITE": "V7R4M0", "REQUISITE_IS_CONDITIONAL": "0", "REQUISITE_IS_REQUIRED": "1", "REQUISITE_LOAD_ID": "5050", "REQUISITE_MAX_LEVLE": "00", "REQUISITE_MIN_LEVLE": "00", "REQUISITE_OPTION": "0000", "REQUISITE_PRODUCT_ID": "5770SS1", "REQUISITE_PTF_ID": "SI69616", "TYPE_OF_REQUISITE": "2"}, {"RELEASE_OF_REQUISITE": "V7R4M0", "REQUISITE_IS_CONDITIONAL": "0", "REQUISITE_IS_REQUIRED": "1", "REQUISITE_LOAD_ID": "5050", "REQUISITE_MAX_LEVLE": "00", "REQUISITE_MIN_LEVLE": "00", "REQUISITE_OPTION": "0000", "REQUISITE_PRODUCT_ID": "5770SS1", "REQUISITE_PTF_ID": "SI69618", "TYPE_OF_REQUISITE": "2"}, {"RELEASE_OF_REQUISITE": "V7R4M0", "REQUISITE_IS_CONDITIONAL": "0", "REQUISITE_IS_REQUIRED": "1", "REQUISITE_LOAD_ID": "5050", "REQUISITE_MAX_LEVLE": "00", "REQUISITE_MIN_LEVLE": "00", "REQUISITE_OPTION": "0000", "REQUISITE_PRODUCT_ID": "5770SS1", "REQUISITE_PTF_ID": "SI69619", "TYPE_OF_REQUISITE": "2"}, {"RELEASE_OF_REQUISITE": "V7R4M0", "REQUISITE_IS_CONDITIONAL": "0", "REQUISITE_IS_REQUIRED": "1", "REQUISITE_LOAD_ID": "5050", "REQUISITE_MAX_LEVLE": "00", "REQUISITE_MIN_LEVLE": "00", "REQUISITE_OPTION": "0000", "REQUISITE_PRODUCT_ID": "5770SS1", "REQUISITE_PTF_ID": "SI69416", "TYPE_OF_REQUISITE": "2"}]
            
      
      
                              
       rc
        | The command return code (0 means success, non-zero means failure).
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       stderr
        | The command standard error.
      
        | **returned**: when rc is not 0
        | **type**: str
        | **sample**: CPF2111:Library TESTLIB already exists

            
      
      
                              
       stderr_lines
        | The command standard error split in lines.
      
        | **returned**: when rc is not 0
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF2111:Library TESTLIB already exists."]
            
      
      
                              
       job_log
        | The IBM i job log of the task executed.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "318F", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "", "FROM_PROCEDURE": "", "FROM_PROGRAM": "QWTCHGJB", "FROM_USER": "CHANGLE", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPD0912", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "Printer device PRT01 not found.", "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897", "MESSAGE_TYPE": "DIAGNOSTIC", "ORDINAL_POSITION": "5", "SEVERITY": "20", "TO_INSTRUCTION": "9369", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
      
                              
       ptf_info
        | the ptf information
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"PTF_ACTION_PENDING": "NO", "PTF_ACTION_REQUIRED": "NONE", "PTF_COVER_LETTER": "YES", "PTF_CREATION_TIMESTAMP": "2020-05-14-22.08.22.000000", "PTF_IDENTIFIER": "SI73329", "PTF_IPL_ACTION": "NONE", "PTF_IPL_REQUIRED": "IMMEDIATE", "PTF_IS_RELEASED": "NO", "PTF_LOADED_STATUS": "APPLIED", "PTF_MAXIMUM_LEVEL": "00", "PTF_MINIMUM_LEVEL": "00", "PTF_ON_ORDER": "NO", "PTF_PRODUCT_DESCRIPTION": "IBM i", "PTF_PRODUCT_ID": "5770SS1", "PTF_PRODUCT_LOAD": "5050", "PTF_PRODUCT_OPTION": "*BASE", "PTF_PRODUCT_RELEASE_LEVEL": "V7R4M0", "PTF_RELEASE_LEVEL": "V7R4M0", "PTF_SAVE_FILE": "YES", "PTF_STATUS_TIMESTAMP": "2020-05-14-22.39.06.000000", "PTF_SUPERSEDED_BY_PTF": "", "PTF_TECHNOLOGY_REFRESH_PTF": "NO", "PTF_TEMPORARY_APPLY_TIMESTAMP": "2020-05-14-22.39.06.000000"}]
            
      
        