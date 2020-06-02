..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_fix.py


ibmi_fix -- Install, remove or query an individual fix or a set of fixes on to IBM i system.
============================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The ``ibmi_fix`` module install fixes to target IBM i system.

The installation file of the fixes should be in the format of save file.

The fixes are normally known as PTFs for IBM i users.






Parameters
----------

  save_file_lib (optional, str, QGPL)
    The library name of the save file to be installed.


  fix_list (optional, list, [u'*ALL'])
    PTF list that will be applied to the IBM i system.


  product_id (optional, str, None)
    Product identifier to which PTFs are applied.


  save_file_object (optional, str, None)
    The object name of the save file to be installed.


  temp_or_perm (optional, str, *TEMP)
    Controls whether the PTF will be permanent applied or temporary applied.


  delayed_option (optional, str, *NO)
    Controls whether the PTF is delayed apply or not


  operation (optional, str, load_and_apply)
    The operation for the fix, the options are as follows

    load_and_apply will load the PTF and apply the PTF

    load_only will only load the PTF by LODPTF

    remove_and_delete will remove the PTF and delete the PTF

    remove_only will only remove the PTF

    delete_only will only delete the PTF

    query will return the specific PTF status


  fix_omit_list (False, list, None)
    The list of PTFs that will be omitted.

    The key of the dict should be the product ID of the fix that is omitted.





Notes
-----

.. note::
   - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)


See Also
--------

.. seealso::

   :ref:`ibmi_fix_imgclg_module`
      The official documentation on the **ibmi_fix_imgclg** module.


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



Return Values
-------------

  stderr_lines (When error occurs., list, ['CPF2111:Library TESTLIB already exists.'])
    The task standard error split in lines


  end (When rc is zero, str, 2019-12-02 11:07:54.064969)
    The task execution end time


  stdout (When error occurs., str, CPC2102: Library TESTLIB created)
    The task standard output


  rc (always, int, 255)
    The task return code (0 means success, non-zero means failure)


  start (When rc is zero, str, 2019-12-02 11:07:53.757435)
    The task execution start time


  stderr (When error occurs., str, CPF2111:Library TESTLIB already exists)
    The task standard error


  delta (When rc is zero, str, 0:00:00.307534)
    The task execution delta time


  stdout_lines (When error occurs., list, ['CPC2102: Library TESTLIB created.'])
    The task standard output split in lines





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Wang Yun (@airwangyun)

