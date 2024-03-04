
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_sql_query.py

.. _ibmi_sql_query_module:


ibmi_sql_query -- Executes a SQL DQL(Data Query Language) statement.
====================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The \ :literal:`ibmi\_sql\_query`\  module takes the SQL DQL(Data Query Language) statement as argument.





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


     
database
  Specified database name, usually, it is the iasp name, use WRKRDBDIRE to check Relational Database Directory Entries.

  Default to use the \ :literal:`\*LOCAL`\  entry.


  | **required**: false
  | **type**: str
  | **default**: \*SYSBAS


     
expected_row_count
  The expected row count.

  If it is equal or greater than 0, check if the actual row count returned from the query statement is matched with the expected row count.

  If it is less than 0, do not check if the actual row count returned from the query statement is matched with the expected row count.


  | **required**: false
  | **type**: int
  | **default**: -1


     
hex_columns
  Specifies the column names which actually a hex string.


  | **required**: false
  | **type**: list
  | **elements**: str


     
joblog
  If set to \ :literal:`true`\ , output the job log even success.


  | **required**: false
  | **type**: bool


     
sql
  The \ :literal:`ibmi\_sql\_query`\  module takes a IBM i SQL DQL(Data Query Language) statement to run.


  | **required**: True
  | **type**: str




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Query the data of table Persons.
     ibm.power_ibmi.ibmi_sql_query:
       sql: 'select * from Persons'
       become_user: 'USER1'
       become_user_password: 'yourpassword'




Notes
-----

.. note::
   This module can only run one statement at a time.



See Also
--------

.. seealso::

   - :ref:`ibmi_sql_execute_module`


  

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

            
      
      
                              
       row
        | The sql query statement result.
      
        | **returned**: when rc as 0(success)
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"ADDRESS": "Ring Building", "CITY": "Beijing", "FIRSTNAME": "Chang", "ID_P": "919665", "LASTNAME": "Le"}, {"ADDRESS": "Ring Building", "CITY": "Shanhai", "FIRSTNAME": "Zhang", "ID_P": "919689", "LASTNAME": "Li"}]
            
      
      
                              
       stdout
        | The sql statement standard output.
      
        | **returned**: When rc as non-zero(failure)
        | **type**: str
      
      
                              
       stderr
        | The sql statement standard error.
      
        | **returned**: When rc as non-zero(failure)
        | **type**: str
      
      
                              
       sql
        | The sql statement executed by the task.
      
        | **returned**: always
        | **type**: str
        | **sample**: select \* from Persons

            
      
      
                              
       rc
        | The sql statement return code (0 means success).
      
        | **returned**: always
        | **type**: int
      
      
                              
       stdout_lines
        | The sql statement standard output split in lines.
      
        | **returned**: When rc as non-zero(failure)
        | **type**: list      
        | **sample**:

              .. code-block::

                       [""]
            
      
      
                              
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
            
      
      
                              
       job_name
        | The QSQSRVR job information which the SQL statement executed.
      
        | **returned**: always
        | **type**: str
        | **sample**: 188624/QUSER/QSQSRVR

            
      
        
