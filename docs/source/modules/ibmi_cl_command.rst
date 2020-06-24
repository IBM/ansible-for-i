..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/IBM/ansible-for-i/tree/ansible_collection_beta/plugins/modules/ibmi_cl_command.py

.. _ibmi_cl_command_module:

ibmi_cl_command -- Executes a CL command on a remote IBMi node
==============================================================


.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_cl_command`` module takes the CL command name followed by a list of space-delimited arguments.
- The given CL command will be executed on all selected nodes.
- For Pase or Qshell(Unix/Linux-liked) commands run on IBMi targets, like 'ls', 'chmod' etc, use the :ref:`command <command_module>` module instead.
- Only run one command at a time.



Parameters
----------


     
asp_group
  Specifies the name of the auxiliary storage pool (ASP) group to set for the current thread.

  The ASP group name is the name of the primary ASP device within the ASP group.

  Ignored when the CL command with OUTPUT parameter, e.g. DSPLIBL OUTPUT(*), DSPHDWRSC TYPE(*AHW) OUTPUT(*).


  | **required**: false
  | **type**: str
  | **default**: *SYSBAS


     
cmd
  The IBM i CL command to run.


  | **required**: True
  | **type**: str


     
joblog
  If set to ``true``, output the avaiable JOBLOG even the rc is 0(success).

  Ignored when the CL command with OUTPUT parameter, e.g. DSPLIBL OUTPUT(*), DSPHDWRSC TYPE(*AHW) OUTPUT(*).


  | **required**: false
  | **type**: bool



Examples
--------

.. code-block:: yaml+jinja

   
   - name: Create a library by using CL command CRTLIB
     ibmi_cl_command:
       command: 'CRTLIB LIB(TESTLIB)'
       asp_group: 'IASP1'



Notes
-----

.. note::
   IBM i CL command with OUTPUT parameter, e.g. DSPLIBL OUTPUT(*), DSPHDWRSC TYPE(*AHW) OUTPUT(*) don't have joblog returned.

   IBM i CL command can also be run by command module with quite simple result messages, add a prefix 'system' to the CL command.

   Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2).


See Also
--------

.. seealso::

   - :ref:`command_module`


Return Values
-------------


   
                              
       stderr_lines
        | The command standard error split in lines
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF2111:Library TESTLIB already exists."]
            
      
      
                              
       end
        | The command execution end time
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:54.064969

            
      
      
                              
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

            
      
      
                              
       cmd
        | The command executed by the task
      
        | **returned**: always
        | **type**: str
        | **sample**: CRTLIB LIB(TESTLIB)

            
      
      
                              
       rc
        | The command return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       start
        | The command execution start time
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:53.757435

            
      
      
                              
       delta
        | The command execution delta time
      
        | **returned**: always
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       stderr
        | The command standard error
      
        | **returned**: always
        | **type**: str
        | **sample**: CPF2111:Library TESTLIB already exists

            
      
      
                              
       joblog
        | Print JOBLOG or not when using itoolkit to run the CL command.
      
        | **returned**: always
        | **type**: bool
      
      
                              
       stdout_lines
        | The command standard output split in lines
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPC2102: Library TESTLIB created."]
            
      
        
