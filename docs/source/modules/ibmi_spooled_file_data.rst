
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_spooled_file_data.py

.. _ibmi_spooled_file_data_module:


ibmi_spooled_file_data -- Returns the content of a spooled file.
================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The \ :literal:`ibmi\_spooled\_file\_data`\  returns the content of a spooled file.





Parameters
----------


     
become_user
  The name of the user profile that the IBM i task will run under.

  Use this option to set a user with desired privileges to run the task.


  | **required**: false
  | **type**: str


     
become_user_password
  Use this option to set the password of the user specified in \ :literal:`become\_user`\ .


  | **required**: false
  | **type**: str


     
job_name
  A character string containing a qualified job name.


  | **required**: True
  | **type**: str


     
spooled_data_filter
  If supplied, only return lines that match this shell-style (fnmatch) wildcard. If this parameter is omitted, all the spooled file content is returned.


  | **required**: false
  | **type**: str
  | **default**: \*


     
spooled_file_name
  A character string containing the name of the spooled file. If this parameter is an incorrect value or the spooled file is not existed, nothing will return to spooled\_data.


  | **required**: True
  | **type**: str


     
spooled_file_number
  A character string containing the number of the spooled file for current job. If this parameter is omitted, the spooled file with the highest number matching spooled-file-name is used.


  | **required**: false
  | **type**: str
  | **default**: \*LAST




Examples
--------

.. code-block:: yaml+jinja

   
   - name: print the spooled file data
     ibm.power_ibmi.ibmi_spooled_file_data:
       job_name: '024800/CHANGLE/QDFTJOBD'
       spooled_file_name: 'QPSECUSR'






See Also
--------

.. seealso::

   - :ref:`ibmi_submit_job_module`


  

Return Values
-------------


   
                              
       rc
        | The command return code (0 means success, non-zero means failure).
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       msg
        | Simple description of the error.
      
        | **returned**: when rc as non-zero(failure)
        | **type**: str
        | **sample**: 255

            
      
      
                              
       spooled_data
        | The spooled file content split in lines.
      
        | **returned**: when rc as 0(success)
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["5770SS1 V7R4M0  190621                                 MIRRORS   11/25/20  10:08:37 CST ", " Report type  . . . . . . . . . :   *PWDLVL                                             ", " Select by  . . . . . . . . . . :   *SPCAUT                                             ", " Special authorities  . . . . . :   *ALL                                                ", "                Password      Password      Password                                    ", " User           for level     for level        for                                      ", " Profile         0 or 1        2 or 3       NetServer                                   ", " CHANGLE          *YES          *YES          *YES                                      ", " DHQB             *NO           *YES          *NO                                       ", " QANZAGENT        *NO           *NO           *NO                                       ", " QAUTPROF         *NO           *NO           *NO                                       ", " QBRMS            *NO           *NO           *NO                                       "]
            
      
      
                              
       job_log
        | The IBM i job log of the task executed.
      
        | **returned**: when rc as non-zero(failure) and error happened for CL command CPYSPLF used in this module.
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "318F", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "", "FROM_PROCEDURE": "", "FROM_PROGRAM": "QWTCHGJB", "FROM_USER": "CHANGLE", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPD0912", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "Printer device PRT01 not found.", "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897", "MESSAGE_TYPE": "DIAGNOSTIC", "ORDINAL_POSITION": "5", "SEVERITY": "20", "TO_INSTRUCTION": "9369", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
        
