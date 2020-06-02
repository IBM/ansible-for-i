..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_fix_imgclg.py


ibmi_fix_imgclg -- Install fixes such as PTF, PTF Group, Technology refresh to the target IBM i system by image catalog.
========================================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The ``ibmi_fix`` module install fixes to target IBM i system by image catalog.

Single PTF, PTF group and TR PTF are supported.






Parameters
----------

  src (True, str, None)
    The path on the target IBM i system where the fix installation file is located.

    The path is an IFS directory format.


  rollback (optional, bool, True)
    Whether or not rollback if there's failure during the installation of the fixes


  product_id (optional, list, [u'*ALL'])
    The product ID of the fixes to be installed.


  apply_type (optional, str, *DLYALL)
    The fix apply type of the install to perform.


  virtual_image_name_list (False, list, [u'*ALL'])
    The name list of the installation file.


  hiper_only (optional, bool, False)
    Whether or not only install the hiper fixes.

    Specify true if only need to install hiper fixes.


  use_temp_path (optional, bool, True)
    Whether or not to copy the installation file to a temp path.

    If true is chosen, it will copy the installation file to a temp path.

    The temp directory and the installation file copied to the temp directory will be both deleted after the task.

    It is recommended to use temp path to avoid conflicts.

    If false is chosen, the install will directly use the file specified in src option.

    The installation file will not be deleted after install if false is chosen.


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

   :ref:`ibmi_fix, ibmi_fix_savf_module`
      The official documentation on the **ibmi_fix, ibmi_fix_savf** module.


Examples
--------

.. code-block:: yaml+jinja

    
    - name: Install a list of PTFs of LPP 5733SC1 from image catalog
      ibmi_fix_imgclg:
        product_id:
          - '5733SC1'
        src: '{{ fix_install_path }}'
        apply_type: '*DLYALL'
        hiper_only: False
        use_temp_path: True
        rollback: True
        virtual_image_name_list:
          - 'S2018V01.BIN'
        fix_omit_list:
          - 5733SC1: "SI70819"



Return Values
-------------

  stderr_lines (When error occurs., list, ['CPF2111:Library TESTLIB already exists.'])
    The task standard error split in lines


  end (When rc is zero, str, 2019-12-02 11:07:54.064969)
    The task execution end time


  stdout_lines (When error occurs., list, ["CRTDEVOPT DEVD(ANSIBOPT2) RSRCNAME(*VRT) ONLINE(*YES) TEXT('Created by Ansible for IBM i')", "+++ success CRTDEVOPT DEVD(ANSIBOPT2) RSRCNAME(*VRT) ONLINE(*YES) TEXT('Created by Ansible for IBM i')", "CRTIMGCLG IMGCLG(ANSIBCLG1) DIR('/home/ansiblePTFInstallTemp/') CRTDIR(*YES)"])
    The task standard output split in lines


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


  need_action_ptf_list (When rc is zero., list, [{'PTF_ACTION_REQUIRED': 'NONE', 'PTF_IPL_REQUIRED': 'IMMEDIATE', 'PTF_IDENTIFIER': 'SI71746', 'PTF_CREATION_TIMESTAMP': '2019-12-06T01:00:43', 'PTF_PRODUCT_ID': '5733SC1', 'PTF_TEMPORARY_APPLY_TIMESTAMP': None, 'PTF_IPL_ACTION': 'TEMPORARILY APPLIED', 'PTF_SAVE_FILE': 'NO', 'PTF_STATUS_TIMESTAMP': '2020-03-24T09:03:55', 'PTF_LOADED_STATUS': 'LOADED', 'PTF_ACTION_PENDING': 'NO'}])
    The list contains the information of the just installed PTFs that need further IPL actions.





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Wang Yun (@airwangyun)

