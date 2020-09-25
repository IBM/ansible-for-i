
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_download_fix.py

.. _ibmi_download_fix_module:


ibmi_download_fix -- Download fix through SNDPTFORD
===================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_download_fix`` module download fix through SNDPTFORD.
- The supported fixs are individual PTFs, cumulative PTF package and PTF Groups.





Parameters
----------


     
become_user
  The name of the user profile that the IBM i task will run under.

  Use this option to set a user with desired privileges to run the task.


  | **required**: false
  | **type**: str


     
become_user_password
  Use this option to set the password of the user specified in ``become_user``.


  | **required**: false
  | **type**: str


     
check_PTF
  Specifies whether checking is performed on the service requester system to determine if PTFs are ordered based on whether or not the PTF product is installed or supported.


  | **required**: false
  | **type**: str
  | **default**: \*NO
  | **choices**: \*NO, \*YES


     
delivery_format
  Specifies the format of the delivered PTFs.


  | **required**: false
  | **type**: str
  | **default**: \*SAVF
  | **choices**: \*SAVF, \*IMAGE


     
image_directory
  Specifies the directory where the optical image files are stored. If IMGCLG parameter is specified, the directory specified will be associated with the image catalog.


  | **required**: false
  | **type**: str
  | **default**: \*DFT


     
joblog
  If set to ``true``, output the available joblog even the rc is 0(success).


  | **required**: false
  | **type**: bool


     
order
  Specifies if requisite PTFs should be included with the ordered PTFs.


  | **required**: false
  | **type**: str
  | **default**: \*REQUIRED
  | **choices**: \*REQUIRED, \*PTFID


     
parameters
  The parameters that SNDPTFORD command will take. Other than options above, all other parameters need to be specified here.

  The default values of parameters for SNDPTFORD will be taken if not specified.


  | **required**: false
  | **type**: str
  | **default**:  


     
product
  Specifies the product ID associated with the PTF.


  | **required**: false
  | **type**: str
  | **default**: \*ONLYPRD


     
ptf_id
  Specify the identifier of the PTF information being ordered.

  For Cumulative PTF package and PTF group ID, please see

  ``*CUMPKG`` Order the latest level of the Cumulative PTF package group (SF99vrm) for the operating system release that is installed on the system. The HIPER and DB2 for IBM i PTF groups are automatically included when the Cumulative PTF package PTF group is specified. This value cannot be specified with any other PTF identifier or special value.

  ``*ALLGRP`` Order the latest level of all PTF groups for the installed operating system release, except the Cumulative PTF package group.

  ``*HIPERGRP`` Order the latest level of the HIPER PTF group for the operating system release that is installed on the system.

  ``*DB2GRP`` Order the latest level of the DB2 for IBM i PTF group for the operating system release that is installed on the system.

  ``*BRSGRP`` Order the latest level of the Backup Recovery Solutions PTF group for the operating system release that is installed on the system.

  ``*HTTPGRP`` Order the latest level of the IBM HTTP Server for i PTF group for the operating system release that is installed on the system.

  ``*JVAGRP`` Order the latest level of the Java PTF group for the operating system release that is installed on the system.

  ``*PFRGRP`` Order the latest level of the Performance Tools PTF group for the operating system release that is installed on the system.


  | **required**: True
  | **type**: str


     
release
  Specifies the release level of the PTF in one of the following formats, VxRyMz, where Vx is the version number, Ry is the release number, and Mz is the modification level. The variables x and y can be a number from 0 through 9, and the variable z can be a number from 0 through 9 or a letter from A through Z. vvrrmm, where version vv and release rr must be a number from 00 through 35, and modification mm must be a number from 00 through 09 or a letter from 0A through 0Z.  The leading zeros are required.  This format must be used if the version or release of the product is greater than 9.


  | **required**: false
  | **type**: str
  | **default**: \*ONLYRLS


     
reorder
  Specifies whether a PTF that is currently loaded, applied, or on order should be ordered again.


  | **required**: false
  | **type**: str
  | **default**: \*YES
  | **choices**: \*NO, \*YES


     
time_out
  The max time that the module waits for the SNDPTFORD command complete.

  The unit can be 's', 'm', 'h', 'd' and 'w'.


  | **required**: false
  | **type**: str
  | **default**: 15m


     
wait
  Only works when delivery_format is ``*SAVF``.

  If delivery_format is ``*SAVF``, and ``wait`` set to ``true``, module will wait until all PTF save files are delivered or time is up.


  | **required**: false
  | **type**: bool
  | **default**: True




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Download a single PTF
     ibmi_download_fix:
       ptf_id: 'SI63556'
       reorder: '*YES'
       order: '*PTFID'

   - name: Download a PTF group with become user
     ibmi_download_fix:
       ptf_id: 'SF99740'
       delivery_format: '*IMAGE'
       become_user: 'USER1'
       become_user_password: 'yourpassword'




Notes
-----

.. note::
   Only support English language ibm i system, language ID 2924.

   See SNDPTFORD command for more information.






Return Values
-------------


   
                              
       delta
        | The module execution delta time.
      
        | **returned**: always
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       stdout
        | The command standard output.
      
        | **returned**: always
        | **type**: str
        | **sample**: PTF 5770UME-SI63556 V1R4M0 received and stored in library QGPL.

            
      
      
                              
       stderr
        | The command standard error.
      
        | **returned**: always
        | **type**: str
        | **sample**: CPD0043: Keyword LOGOUTPUT not valid for this command.\n

            
      
      
                              
       command
        | The excuted SNDPTFORD command.
      
        | **returned**: always
        | **type**: str
        | **sample**: QSYS/SBMJOB CMD(SNDPTFORD PTFID((SI63556 \*ONLYPRD \*ONLYRLS)) DLVRYFMT(\*SAVF) ORDER(\*PTFID) REORDER(\*YES) CHKPTF(\*NO))

            
      
      
                              
       rc
        | The command action return code. 0 means success.
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       stdout_lines
        | The command standard output split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPC3703: 2 objects restored from test to test."]
            
      
      
                              
       stderr_lines
        | The command standard error split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPD0043: Keyword LOGOUTPUT not valid for this command.", "CPD0099: Previous 1 errors found in embedded command SNDPTFORD."]
            
      
      
                              
       download_list
        | The successful downloaded fix list.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"download_time": "2020-07-30T22:55:11.754388", "file_name": "QSI63556", "file_path": "/qsys.lib/qgpl.lib/QSI63556.FILE", "order_id": "2348376546", "product": "5770UME", "ptf_id": "SI63556", "release": "V1R4M0"}]
            
      
      
                              
       order_id
        | The order identifier of the PTF order.
      
        | **returned**: always
        | **type**: int
        | **sample**: 2021278656

            
      
      
                              
       msg
        | The general message returned.
      
        | **returned**: always
        | **type**: str
        | **sample**: PTF order cannot be processed. See joblog

            
      
      
                              
       job_log
        | The IBM i job log of the task executed.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "54", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "QESECARE", "FROM_PROCEDURE": "SendMsg__FPcT1iT1", "FROM_PROGRAM": "QESECARE", "FROM_USER": "QSECOFR", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPI35F1", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "\u0026N Cause . . . . . :   The cover letter has been copied to file QAPZCOVER in library QGPL with member name of QSI63556 from file *N member *N. \u0026N Recovery  . . . :   Use the Display Program Temporary Fix (DSPPTF) command to display the cover letter. Specify product 5770UME, PTF SI63556, release  and request cover letter only.", "MESSAGE_SUBTYPE": null, "MESSAGE_TEXT": "Cover letter has been copied to file QAPZCOVER member QSI63556.", "MESSAGE_TIMESTAMP": "2020-07-30T22:55:12.865122", "MESSAGE_TYPE": "INFORMATIONAL", "ORDINAL_POSITION": 7, "SEVERITY": 0, "TO_INSTRUCTION": "54", "TO_LIBRARY": "QSYS", "TO_MODULE": "QESECARE", "TO_PROCEDURE": "SendMsg__FPcT1iT1", "TO_PROGRAM": "QESECARE"}, {"FROM_INSTRUCTION": "54", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "QESECARE", "FROM_PROCEDURE": "SendMsg__FPcT1iT1", "FROM_PROGRAM": "QESECARE", "FROM_USER": "QSECOFR", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPZ8C12", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "\u0026N Cause . . . . . :   Program temporary fix (PTF) SI63556 product 5770UME at release V1R4M0 was received and is stored in library QGPL.  Use the Display PTF (DSPPTF) command to view the status of the PTF on your system.", "MESSAGE_SUBTYPE": null, "MESSAGE_TEXT": "PTF 5770UME-SI63556 V1R4M0 received and stored in library QGPL.", "MESSAGE_TIMESTAMP": "2020-07-30T22:55:11.754388", "MESSAGE_TYPE": "INFORMATIONAL", "ORDINAL_POSITION": 6, "SEVERITY": 0, "TO_INSTRUCTION": "54", "TO_LIBRARY": "QSYS", "TO_MODULE": "QESECARE", "TO_PROCEDURE": "SendMsg__FPcT1iT1", "TO_PROGRAM": "QESECARE"}]
            
      
        
