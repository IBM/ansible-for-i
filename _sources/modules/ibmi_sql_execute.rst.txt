
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_sql_execute.py

.. _ibmi_sql_execute_module:


ibmi_sql_execute -- Executes a SQL non-DQL(Data Query Language) statement
=========================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_sql_execute`` module takes the SQL non-DQL(Data Query Language) statement as argument.





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


     
database
  Specified database name, usually, its the iasp name, use WRKRDBDIRE to check Relational Database Directory Entries

  Default to use the ``*LOCAL`` entry


  | **required**: false
  | **type**: str
  | **default**: \*SYSBAS


     
joblog
  If set to ``true``, output the JOBLOG even success.


  | **required**: false
  | **type**: bool


     
sql
  The ``ibmi_sql_execute`` module takes a IBM i SQL non-DQL(Data Query Language) statement to run.


  | **required**: True
  | **type**: str




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Insert one record to table Persons
     ibmi_sql_execute:
       sql: "INSERT INTO Persons VALUES('919665', 'Le', 'Chang', 'Ring Building', 'Beijing')"
       become_user: 'USER1'
       become_user_password: 'yourpassword'




Notes
-----

.. note::
   This module can only run one SQL statement at a time.



See Also
--------

.. seealso::

   - :ref:`IBMi_sql_query_module`



Return Values
-------------


   
                              
       start
        | The sql statement execution start time.
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:53.757435

            
      
      
                              
       end
        | The sql statement execution end time.
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:54.064969

            
      
      
                              
       delta
        | The sql statement execution delta time.
      
        | **returned**: always
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       stdout
        | The sql statement standard output.
      
        | **returned**: always
        | **type**: str
        | **sample**: +++ success INSERT INTO Persons VALUES('919665', 'Le', 'Chang', 'Ring Building', 'Beijing')

            
      
      
                              
       stderr
        | The sql statement standard error.
      
        | **returned**: always
        | **type**: str
      
      
                              
       sql
        | The sql statement executed by the task.
      
        | **returned**: always
        | **type**: str
        | **sample**: INSERT INTO Persons VALUES('919665', 'Le', 'Chang', 'Ring Building', 'Beijing')

            
      
      
                              
       rc
        | The sql statement return code (0 means success, non-zero means failure).
      
        | **returned**: always
        | **type**: int
      
      
                              
       stdout_lines
        | The sql statement standard output split in lines.
      
        | **returned**: When rc as non-zero(failure)
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["+++ success INSERT INTO Persons VALUES(\u0027919665\u0027, \u0027Le\u0027, \u0027Chang\u0027, \u0027Ring Building\u0027, \u0027Beijing\u0027)"]
            
      
      
                              
       stderr_lines
        | The sql statement standard error split in lines.
      
        | **returned**: When rc as non-zero(failure)
        | **type**: list      
        | **sample**:

              .. code-block::

                       [""]
            
      
      
                              
       job_log
        | The IBM i job log of the task executed.
      
        | **returned**: when rc as non-zero(failure) or rc as success(0) but joblog set to true.
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "318F", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "", "FROM_PROCEDURE": "", "FROM_PROGRAM": "QWTCHGJB", "FROM_USER": "CHANGLE", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPD0912", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "Printer device PRT01 not found.", "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897", "MESSAGE_TYPE": "DIAGNOSTIC", "ORDINAL_POSITION": "5", "SEVERITY": "20", "TO_INSTRUCTION": "9369", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
        
