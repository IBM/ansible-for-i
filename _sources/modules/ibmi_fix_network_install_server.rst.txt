
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_fix_network_install_server.py

.. _ibmi_fix_network_install_server_module:


ibmi_fix_network_install_server -- Setup IBM i Network install server which contains image files of PTFs, PTF Group and Technology refresh.
===========================================================================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The :literal:`ibmi\_fix` module setup IBM i Network install server which contains images files.
- Single PTF, PTF group and TR PTF are supported.





Parameters
----------


     
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
  The virtual optical device name.


  | **required**: false
  | **type**: str
  | **default**: REPOSVROPT


     
image_catalog_directory_name
  The image catalog directory on the IBM i Network install server.

  The path is an IFS directory format.


  | **required**: false
  | **type**: str
  | **default**: /etc/ibmi_ansible/fix_management/network_install


     
image_catalog_name
  The name of image catalog that is created on the server.


  | **required**: false
  | **type**: str
  | **default**: REPOSVRCLG


     
joblog
  The job log of the job executing the task will be returned even rc is zero if it is set to True.


  | **required**: false
  | **type**: bool


     
operation
  The operation on the Network install server, the options are as follows

  setup\_only will only setup the network install server, including configuring a virtual optical device and image catalog.

  setup\_and\_addimgclge will setup the network install server and add image catalog entries for PTF image files.

  addimgclge\_only will only add image catalog entries for PTF image files.

  rmvimgclge\_only will only remove all the image catalog entries for PTF image files.

  rmvimgclge\_and\_addimgclge will first remove all the image catalog entries for existing PTF image files, then add entries for new PTF image files.

  uninstall will remove the network install server configuration.

  retrieve\_image\_catalog\_entries will retrieve the current image catalog entries.

  restart\_NFS\_server will restart NFS Server.


  | **required**: false
  | **type**: str
  | **default**: setup_only
  | **choices**: setup_only, setup_and_addimgclge, addimgclge_only, rmvimgclge_only, rmvimgclge_and_addimgclge, uninstall, retrieve_image_catalog_entries, restart_NFS_server


     
remove_image_files
  Whether the PTF image files under image catalog directory will be removed when removing entries from image catalog.

  Whether the PTF image files under image catalog directory will be removed when removing the network install server configuration.


  | **required**: false
  | **type**: bool
  | **default**: True


     
rollback
  Whether or not rollback if there's failure during the operation.


  | **required**: false
  | **type**: bool
  | **default**: True


     
virtual_image_name_list
  The name list of the PTF image file and its directory, for example, :literal:`/tmp/5733WQXPTFs/SF99433\_1.bin`.

  You can specify all the PTF image files under one directory, for example, :literal:`/tmp/PTFs/\*ALL`.

  bin and iso image files are supported.

  default is :literal:`\*ALL` for all the PTF image files under image catalog directory.


  | **required**: false
  | **type**: list
  | **elements**: str
  | **default**: \*ALL


     
virtual_image_name_remove_list
  The name list of the PTF image file which will be moved from the image catalog, for example, :literal:`SF99433\_1.bin`.

  default is :literal:`\*ALL` for all the PTF image files under the image caltalog.


  | **required**: false
  | **type**: list
  | **elements**: str
  | **default**: \*ALL




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Setup IBM i Netwotk install server and add image files of group PTF for LPP 5733WQX
     ibm.power_ibmi.ibmi_fix_network_install_server:
       operation: 'setup_and_addimgclge'
       rollback: True
       virtual_image_name_list:
         - "/tmp/5733WQXPTFs/SF99433_1.bin"
         - "/tmp/5733WQXPTFs/SF99433_2.bin"
       become_user: "QSECOFR"
       become_user_password: "yourpassword"




Notes
-----

.. note::
   Ansible hosts file need to specify ansible\_python\_interpreter=/QOpenSys/pkgs/bin/python3

   If operation is setup\_only or setup\_and\_addimgclge, the user who this task will run under, should be enrolled in system distribution directorty

   Issue ADDDIRE command to add the user to the system distribution directory entry

   Issue WRKDIRE command to check the current system distribution directory entries



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
        | **sample**: Same optical device with different configuration already exists

            
      
      
                              
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
            
      
      
                              
       image_catalog_name
        | The name of image catalog on the server
      
        | **returned**: always
        | **type**: str
        | **sample**: REPOSVRCLG

            
      
      
                              
       device_name
        | The virtual optical device name
      
        | **returned**: always
        | **type**: str
        | **sample**: REPOSVROPT

            
      
      
                              
       image_catalog_directory_name
        | The path on the IBM i Network install server where the PTF image files are located.
      
        | **returned**: always
        | **type**: str
        | **sample**: /etc/ibmi_ansible/fix_management/network_install

            
      
      
                              
       image_catalog_entries
        | The image catalog entries (image file name and its index) in the image catalog after the operation
      
        | **returned**: When use operation setup_and_addmgclge, addimgclge_only, rmvimgclge_and_addimgclge, rmvimgclge_only or retrieve_image_catalog_entries
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"SF99433_1.bin": "1"}, {"SF99433_2.bin": "2"}]
            
      
      
                              
       success_list
        | The image catalog entries (image file name) which are added or removed successfully
      
        | **returned**: When use operation setup_and_addmgclge, addimgclge_only, rmvimgclge_and_addimgclge, rmvimgclge_only
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"add": "SF99433_1.bin"}, {"remove": "SF99433_2.bin"}]
            
      
      
                              
       fail_list
        | The image catalog entries (image file name) which are failed to be added or removed
      
        | **returned**: When use operation setup_and_addmgclge, addimgclge_only, rmvimgclge_and_addimgclge, rmvimgclge_only
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"add": "SF99433_1.bin"}, {"remove": "SF99433_2.bin"}]
            
      
        
