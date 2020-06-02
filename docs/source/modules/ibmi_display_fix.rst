..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_display_fix.py


ibmi_display_fix -- display the PTF(Program Temporary Fix)information and also get the requisite information for the PTF
========================================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The ``ibmi_display_fix`` module display the information of the PTF and also get the requisite PTF






Parameters
----------

  release (True, str, None)
    Specifies the release level of the PTF in one of the following formats.

    VxRyMz, for example, V7R2M0 is version 7, release 2, modification 0

    vvrrmm, this format must be used if the version or release of the product is greater than 9.

    For example, 110300 is version 11, release 3, modification 0.


  ptf (True, str, None)
    Specifies which PTF is shown for the specified product.


  product (True, str, None)
    Specifies the product for the PTF


  joblog (optional, bool, False)
    If set to ``true``, output the avaiable JOBLOG even the rc is 0(success).







See Also
--------

.. seealso::

   :ref:`ibmi_fix_module`
      The official documentation on the **ibmi_fix** module.


Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get PTF information
      ibmi_display_fix:
        product: '5770SS1'
        ptf: 'SI70439'
        release: 'V7R4M0'



Return Values
-------------

  stderr_lines (always, list, ['CPF2111:Library TESTLIB already exists.'])
    The command standard error split in lines


  job_log (always, str, [{'TO_MODULE': 'QSQSRVR', 'TO_PROGRAM': 'QSQSRVR', 'MESSAGE_TEXT': 'Printer device PRT01 not found.', 'FROM_MODULE': '', 'FROM_PROGRAM': 'QWTCHGJB', 'MESSAGE_TIMESTAMP': '2020-05-20-21.41.40.845897', 'FROM_USER': 'CHANGLE', 'TO_INSTRUCTION': '9369', 'MESSAGE_SECOND_LEVEL_TEXT': 'Cause . . . . . :   This message is used by application programs as a general escape message.', 'MESSAGE_TYPE': 'DIAGNOSTIC', 'MESSAGE_ID': 'CPD0912', 'MESSAGE_LIBRARY': 'QSYS', 'FROM_LIBRARY': 'QSYS', 'SEVERITY': '20', 'FROM_PROCEDURE': '', 'TO_LIBRARY': 'QSYS', 'FROM_INSTRUCTION': '318F', 'MESSAGE_SUBTYPE': '', 'ORDINAL_POSITION': '5', 'MESSAGE_FILE': 'QCPFMSG', 'TO_PROCEDURE': 'QSQSRVR'}])
    the job_log


  stdout (always, str, CPC2102: Library TESTLIB created)
    The command standard output


  stderr (always, str, CPF2111:Library TESTLIB already exists)
    The command standard error


  rc (always, int, 255)
    The command return code (0 means success, non-zero means failure)


  stdout_lines (always, list, ['CPC2102: Library TESTLIB created.'])
    The command standard output split in lines


  requisite_ptf (always, dict, {'SI71139': '*PREREQ', 'SI71138': '*PREREQ', 'SI71080': '*COREQ', 'SI71137': '*COREQ', 'SI70030': '*PREREQ', 'SI71135': '*COREQ'})
    The requisite PTFs and type


  ptf_info (always, str, [{'PTF_ACTION_REQUIRED': 'NONE', 'PTF_PRODUCT_DESCRIPTION': 'IBM i', 'PTF_IS_RELEASED': 'NO', 'PTF_IPL_ACTION': 'NONE', 'PTF_MINIMUM_LEVEL': '00', 'PTF_PRODUCT_RELEASE_LEVEL': 'V7R4M0', 'PTF_SUPERSEDED_BY_PTF': '', 'PTF_TECHNOLOGY_REFRESH_PTF': 'NO', 'PTF_PRODUCT_LOAD': '5050', 'PTF_ACTION_PENDING': 'NO', 'PTF_IDENTIFIER': 'SI73329', 'PTF_IPL_REQUIRED': 'IMMEDIATE', 'PTF_CREATION_TIMESTAMP': '2020-05-14-22.08.22.000000', 'PTF_PRODUCT_ID': '5770SS1', 'PTF_COVER_LETTER': 'YES', 'PTF_TEMPORARY_APPLY_TIMESTAMP': '2020-05-14-22.39.06.000000', 'PTF_PRODUCT_OPTION': '*BASE', 'PTF_MAXIMUM_LEVEL': '00', 'PTF_SAVE_FILE': 'YES', 'PTF_RELEASE_LEVEL': 'V7R4M0', 'PTF_LOADED_STATUS': 'APPLIED', 'PTF_ON_ORDER': 'NO', 'PTF_STATUS_TIMESTAMP': '2020-05-14-22.39.06.000000'}])
    the ptf information





Status
------




- This module is not guaranteed to have a backwards compatible interface. *[preview]*


- This module is maintained by community.



Authors
~~~~~~~

- Chang Le(@changlexc)

