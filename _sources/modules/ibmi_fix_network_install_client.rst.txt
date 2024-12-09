
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_fix_network_install_client.py

.. _ibmi_fix_network_install_client_module:


ibmi_fix_network_install_client -- Install PTFs on the client via IBM i Network install
=======================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The :literal:`ibmi\_fix` module installs PTFs on the client via IBM i Network install.
- Single PTF, PTF group and TR PTF are supported.





Parameters
----------


     
apply_type
  The fix apply type of the install to perform.


  | **required**: false
  | **type**: str
  | **default**: \*DLYALL
  | **choices**: \*DLYALL, \*IMMDLY, \*IMMONLY


     
become_user
  The name of the user profile that the IBM i task will run under.

  Use this option to set a user with desired privileges to run the task.


  | **required**: false
  | **type**: str


     
become_user_password
  Use this option to set the password of the user specified in :literal:`become\_user`.


  | **required**: false
  | **type**: str


     
device_name
  The virtual optical device name on the client


  | **required**: false
  | **type**: str
  | **default**: CLNTPTFOPT


     
fix_omit_list
  The list of PTFs which will be omitted.

  The key of the dict should be the product ID of the fix that is omitted.


  | **required**: False
  | **type**: list
  | **elements**: dict


     
hiper_only
  Whether or not only install the hiper fixes.

  Specify true if only need to install hiper fixes.


  | **required**: false
  | **type**: bool


     
image_catalog_directory_name
  The image catalog directory on the server

  The path is an IFS directory format.


  | **required**: false
  | **type**: str
  | **default**: /etc/ibmi_ansible/fix_management/network_install


     
joblog
  The job log of the job executing the task will be returned even rc is zero if it is set to True.


  | **required**: false
  | **type**: bool


     
operation
  The operation on the client, the options are as follows

  setup\_only will only setup the environment to install PTFs.

  setup\_and\_installPTF will setup the environment and install PTFs.

  installPTF\_only will only install PTFs.

  reload will vary off and vary on the optical device when the image catalog files are updated on the server.

  uninstall will remove the environment on the client.

  setup\_and\_installPTF\_and\_uninstall will setup the environment, install PTFs and then remove the environment.


  | **required**: false
  | **type**: str
  | **default**: setup_and_installPTF_and_uninstall
  | **choices**: setup_only, setup_and_installPTF, installPTF_only, reload, uninstall, setup_and_installPTF_and_uninstall


     
product_id
  The product ID of the fixes to be installed.


  | **required**: false
  | **type**: list
  | **elements**: str
  | **default**: \*ALL


     
rollback
  Whether or not rollback if there's failure during the operation


  | **required**: false
  | **type**: bool
  | **default**: True


     
server_address
  The address of IBM i network install server

  It could be IP address or host name


  | **required**: false
  | **type**: str




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Setup the client
     ibm.power_ibmi.ibmi_fix_network_install_client:
       operation: 'setup_only'
       server_address: '9.123.123.45'
       image_catalog_directory_name: '/tmp/PTFs'
       rollback: True
       become_user: "QSECOFR"
       become_user_password: "yourpassword"




Notes
-----

.. note::
   Ansible hosts file need to specify ansible\_python\_interpreter=/QOpenSys/pkgs/bin/python3



See Also
--------

.. seealso::

   - :ref:`ibmi_fix_module`


  

Return Values
-------------


   
                              
       start
        | The task execution start time
      
        | **returned**: When rc is zero
        | **type**: str
        | **sample**: 2019-12-02 11:07:53.757435

            
      
      
                              
       end
        | The task execution end time
      
        | **returned**: When rc is zero
        | **type**: str
        | **sample**: 2019-12-02 11:07:54.064969

            
      
      
                              
       delta
        | The task execution delta time
      
        | **returned**: When rc is zero
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       stdout
        | The task standard output
      
        | **returned**: When error occurs.
        | **type**: str
        | **sample**: CPC2102: Library TESTLIB created

            
      
      
                              
       stderr
        | The task standard error
      
        | **returned**: When error occurs.
        | **type**: str
        | **sample**: CPF2111:Library TESTLIB already exists

            
      
      
                              
       rc
        | The task return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       stdout_lines
        | The task standard output split in lines
      
        | **returned**: When error occurs.
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CRTDEVOPT DEVD(ANSIBOPT2) RSRCNAME(*VRT) ONLINE(*YES) TEXT(\u0027Created by Ansible for IBM i\u0027)", "+++ success CRTDEVOPT DEVD(ANSIBOPT2) RSRCNAME(*VRT) ONLINE(*YES) TEXT(\u0027Created by Ansible for IBM i\u0027)", "CRTIMGCLG IMGCLG(ANSIBCLG1) DIR(\u0027/home/ansiblePTFInstallTemp/\u0027) CRTDIR(*YES)"]
            
      
      
                              
       stderr_lines
        | The task standard error split in lines
      
        | **returned**: When error occurs.
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF2111:Library TESTLIB already exists."]
            
      
      
                              
       job_log
        | The job log of the job executes the task.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "318F", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "", "FROM_PROCEDURE": "", "FROM_PROGRAM": "QWTCHGJB", "FROM_USER": "CHANGLE", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPD0912", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "Printer device PRT01 not found.", "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897", "MESSAGE_TYPE": "DIAGNOSTIC", "ORDINAL_POSITION": "5", "SEVERITY": "20", "TO_INSTRUCTION": "9369", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
      
                              
       device_name
        | The virtual optical device name
      
        | **returned**: always
        | **type**: str
        | **sample**: REPOSVROPT

            
      
      
                              
       need_action_ptf_list
        | The list contains the information of the just installed PTFs that need further IPL actions.
      
        | **returned**: When use operation 'setup_and_installPTF', 'installPTF_only' and 'setup_and_installPTF_and_uninstall'
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"PTF_ACTION_PENDING": "NO", "PTF_ACTION_REQUIRED": "NONE", "PTF_CREATION_TIMESTAMP": "2019-12-06T01:00:43", "PTF_IDENTIFIER": "SI71746", "PTF_IPL_ACTION": "TEMPORARILY APPLIED", "PTF_IPL_REQUIRED": "IMMEDIATE", "PTF_LOADED_STATUS": "LOADED", "PTF_PRODUCT_ID": "5733SC1", "PTF_SAVE_FILE": "NO", "PTF_STATUS_TIMESTAMP": "2020-03-24T09:03:55", "PTF_TEMPORARY_APPLY_TIMESTAMP": null}]
            
      
      
                              
       requisite_ptf_list
        | The PTF list contains the requiste PTF of the PTF being applied.
      
        | **returned**: When use operation 'setup_and_installPTF', 'installPTF_only' and 'setup_and_installPTF_and_uninstall'
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"ptf_id": "SI76012", "requisite": "SI76014"}, {"ptf_id": "SI76012", "requisite": "SI76013"}]
            
      
      
                              
       ptf_install_fail_reason
        | The failure reason if it fails to install PTFs. It is from the message content
      
        | **returned**: When use operation 'setup_and_installPTF', 'installPTF_only' and 'setup_and_installPTF_and_uninstall'
        | **type**: str
        | **sample**: Program temporary fixes (PTFs) can only be loaded, applied and removed for products which are installed.

            
      
        
