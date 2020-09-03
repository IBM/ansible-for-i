
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_sqlite3.py

.. _ibmi_sqlite3_module:


ibmi_sqlite3 -- Executes a SQL statement via sqlite3
====================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_sqlite3`` module takes the SQL statement as argument.





Parameters
----------


     
database
  Specified database file name, e.g. '/tmp/testdb.sqlite3'


  | **required**: False
  | **type**: str
  | **default**: /tmp/testdb.sqlite3


     
parameters
  The binding parameters for the sql statement executed by the task.


  | **required**: False
  | **type**: list
  | **elements**: dict


     
sql
  The ``ibmi_sqlite3`` module takes a IBM i SQL statement to run.


  | **required**: True
  | **type**: str




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Create table PTFINFO
     ibmi_sqlite3:
       database: "/tmp/testdb.sqlite3"
       sql: "CREATE TABLE PTFINFO (ID CHAR(10) PRIMARY KEY NOT NULL, PRODUCT CHAR(10) NOT NULL, VRM CHAR(10) NOT NULL, CHECKSUM CHAR(256))"

   - name: Insert some records to table PTFINFO
     ibmi_sqlite3:
       database: "/tmp/testdb.sqlite3"
       sql: "INSERT INTO PTFINFO (ID, PRODUCT, VRM, CHECKSUM) VALUES (:ID, :PRODUCT, :VRM, :CHECKSUM)"
       parameters: [
         {
           "ID": "SI12345",
           "PRODUCT": "5770UME",
           "SAVF": "QSI12345",
           "CHKSUM": "f234cvfsd5345"
         },
         {
           "ID": "SI67890",
           "PRODUCT": "5770DG1",
           "SAVF": "QSI67890",
           "CHKSUM": "f2eqwe345345"
         }
       ]

   - name: Find a record to table PTFINFO
     ibmi_sqlite3:
       database: "/tmp/testdb.sqlite3"
       sql: "SELECT ID FROM PTFINFO WHERE ID = :ID"
       parameters: {"ID": "SI69379"}

   - name: Update a record in table PTFINFO
     ibmi_sqlite3:
       database: "/tmp/testdb.sqlite3"
       sql: "UPDATE PTFINFO SET CHECKSUM=:CHECKSUM WHERE ID=:ID"
       parameters: {"ID": "SI69379", "CHECKSUM": "abc123"}

   - name: Delete a record in table PTFINFO
     ibmi_sqlite3:
       database: "/tmp/testdb.sqlite3"
       sql: "DELETE FROM PTFINFO WHERE ID=:ID"
       parameters: {"ID": "SI69379"}

   - name: Delete table PTFINFO
     ibmi_sqlite3:
       database: "/tmp/testdb.sqlite3"
       sql: "DROP TABLE IF EXISTS PTFINFO"









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

            
      
      
                              
       row_changed
        | The updated row number after add/update/delete operations.
      
        | **returned**: always
        | **type**: str
        | **sample**: 1

            
      
      
                              
       rows
        | The sql query statement result.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [["SI69375", "5770UME", "QSI69375", "f2342345345"], ["SI69379", "5770DG1", "V7R3M0", "f2eqwe345345"]]
            
      
      
                              
       sql
        | The input sql statement executed by the task.
      
        | **returned**: always
        | **type**: str
        | **sample**: INSERT INTO PTFINFO (ID, PRODUCT, VRM, CHECKSUM) VALUES (:ID, :PRODUCT, :VRM, :CHECKSUM)

            
      
      
                              
       parameters
        | The input binding parameters for the sql statement executed by the task.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"CHKSUM": "f2342345345", "ID": "SI69375", "PRODUCT": "5770UME", "SAVF": "QSI69375"}, {"CHKSUM": "f2eqwe345345", "ID": "SI69379", "PRODUCT": "5770DG1", "SAVF": "QSI69379"}]
            
      
        
