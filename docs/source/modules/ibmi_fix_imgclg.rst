..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/IBM/ansible-for-i/tree/ansible_collection_beta/plugins/modules/ibmi_fix_imgclg.py

.. _ibmi_fix_imgclg_module:

ibmi_fix_imgclg -- Install fixes such as PTF, PTF Group, Technology refresh to the target IBM i system by image catalog.
========================================================================================================================


.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_fix`` module install fixes to target IBM i system by image catalog.
- Single PTF, PTF group and TR PTF are supported.



Parameters
----------


     
apply_type
  The fix apply type of the install to perform.


  | **required**: false
  | **type**: str
  | **default**: *DLYALL
  | **choices**: *DLYALL, *IMMDLY, *IMMONLY


     
fix_omit_list
  The list of PTFs that will be omitted.

  The key of the dict should be the product ID of the fix that is omitted.


  | **required**: False
  | **type**: list
  | **elements**: dict


     
hiper_only
  Whether or not only install the hiper fixes.

  Specify true if only need to install hiper fixes.


  | **required**: false
  | **type**: bool


     
product_id
  The product ID of the fixes to be installed.


  | **required**: false
  | **type**: list
  | **elements**: str
  | **default**: [u'*ALL']


     
rollback
  Whether or not rollback if there's failure during the installation of the fixes


  | **required**: false
  | **type**: bool
  | **default**: True


     
src
  The path on the target IBM i system where the fix installation file is located.

  The path is an IFS directory format.


  | **required**: True
  | **type**: str


     
use_temp_path
  Whether or not to copy the installation file to a temp path.

  If true is chosen, it will copy the installation file to a temp path.

  The temp directory and the installation file copied to the temp directory will be both deleted after the task.

  It is recommended to use temp path to avoid conflicts.

  If false is chosen, the install will directly use the file specified in src option.

  The installation file will not be deleted after install if false is chosen.


  | **required**: false
  | **type**: bool
  | **default**: True


     
virtual_image_name_list
  The name list of the installation file.


  | **required**: False
  | **type**: list
  | **elements**: str
  | **default**: [u'*ALL']



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



Notes
-----

.. note::
   Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)


See Also
--------

.. seealso::

   - :ref:`ibmi_fix, ibmi_fix_savf_module`


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

            
      
      
                              
       stdout_lines
        | The task standard output split in lines
      
        | **returned**: When error occurs.
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CRTDEVOPT DEVD(ANSIBOPT2) RSRCNAME(*VRT) ONLINE(*YES) TEXT(\u0027Created by Ansible for IBM i\u0027)", "+++ success CRTDEVOPT DEVD(ANSIBOPT2) RSRCNAME(*VRT) ONLINE(*YES) TEXT(\u0027Created by Ansible for IBM i\u0027)", "CRTIMGCLG IMGCLG(ANSIBCLG1) DIR(\u0027/home/ansiblePTFInstallTemp/\u0027) CRTDIR(*YES)"]
            
      
      
                              
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

            
      
      
                              
       need_action_ptf_list
        | The list contains the information of the just installed PTFs that need further IPL actions.
      
        | **returned**: When rc is zero.
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"PTF_ACTION_PENDING": "NO", "PTF_ACTION_REQUIRED": "NONE", "PTF_CREATION_TIMESTAMP": "2019-12-06T01:00:43", "PTF_IDENTIFIER": "SI71746", "PTF_IPL_ACTION": "TEMPORARILY APPLIED", "PTF_IPL_REQUIRED": "IMMEDIATE", "PTF_LOADED_STATUS": "LOADED", "PTF_PRODUCT_ID": "5733SC1", "PTF_SAVE_FILE": "NO", "PTF_STATUS_TIMESTAMP": "2020-03-24T09:03:55", "PTF_TEMPORARY_APPLY_TIMESTAMP": null}]
            
      
        
