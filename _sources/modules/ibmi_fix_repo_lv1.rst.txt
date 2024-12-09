
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_fix_repo_lv1.py

.. _ibmi_fix_repo_lv1_module:


ibmi_fix_repo_lv1 -- Manipulate the PTF database via sqlite3
============================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The :literal:`ibmi\_fix\_repo\_lv1` module manipulate the PTF database via sqlite3.
- Required dependency is :literal:`SQLite3 \>= 3.26`.
- Install it using :literal:`yum install libsqlite3`





Parameters
----------


     
action
  The action the :literal:`ibmi\_fix\_repo\_lv1` module takes towards the PTF database.

  :literal:`refresh`\ , :literal:`list`\ , :literal:`find` or :literal:`clear`.


  | **required**: True
  | **type**: str


     
additional_sql
  The additional sql appended to the query for action 'find'.


  | **required**: false
  | **type**: str


     
checksum
  Specified if check the image file's integrity when action is 'find' or 'list'


  | **required**: false
  | **type**: bool


     
database
  Specified database file name, e.g. '/tmp/testdb.sqlite3'


  | **required**: false
  | **type**: str
  | **default**: /etc/ibmi_ansible/fix_management/repo_lv1.sqlite3


     
fields
  The expected output column names of the query result for the 'find' action.


  | **required**: false
  | **type**: list
  | **elements**: str


     
image_root
  The image\_root of the image files.


  | **required**: false
  | **type**: str


     
parameters
  The query parameters for the 'find' action executed by the task.


  | **required**: false
  | **type**: list
  | **elements**: dict




Examples
--------

.. code-block:: yaml+jinja

   
   - name: scan the PTF images root and refresh the database records
     ibmi_fix_repo_lv1:
       action: 'refresh'
       image_root: '/home/you/PTF'
   - name: query some PTF records
     ibm.power_ibmi.ibmi_fix_repo_lv1:
       action: "find"
       checksum: true
       additional_sql: 'WHERE image_type IS NOT "single_ptf" ORDER BY ordered_ptf_count'
       fields:
         - 'image_type'
         - 'image_path'
         - 'ordered_ptf_count'
       parameters:
         - {'group':'SF99738', 'level':'10'}
         - {"group": "SF99876"}
         - {"ptf": "SI77631"}
         - {"shipped_ptf": "SI50077"}
   - name: list all PTF records from database
     ibmi_fix_repo_lv1:
       action: 'list'
       additional_sql: 'WHERE image_type IS NOT "cum" ORDER BY download_date DESC'
   - name: clear the PTF database
     ibm.power_ibmi.ibmi_fix_repo_lv1:
       action: "clear"








  

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
        | The updated row number after refresh operations.
      
        | **returned**: when action is 'refresh'
        | **type**: str
        | **sample**: 1

            
      
      
                              
       success_list
        | The result of the found PTFs.
      
        | **returned**: when action is 'find' or 'list'
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"query_item": {"shipped_ptf": "SI50077"}, "query_result": [{"image_files": [{"expected_chksum": "672d1e85aa70a79c705bbe7fffd50aad9698428f83c5fae0f2e16f508df8cba8", "file": "SI77271B_1.bin", "file_chksum": "672d1e85aa70a79c705bbe7fffd50aad9698428f83c5fae0f2e16f508df8cba8", "integrity": true}], "image_path": "/home/pengzy/PTF/singleptf/SI77271SI77631", "image_type": "single_ptf", "ordered_ptf_count": 2}]}]
            
      
      
                              
       sql
        | The formatted sql statement executed by the task.
      
        | **returned**: always
        | **type**: str
        | **sample**: SELECT image_type,image_path,ordered_ptf_count,image_files,ordered_ptf,shipped_ptf FROM ptf_repo_lv1_info

            
      
      
                              
       parameters
        | The input query parameters for the sql statement executed by the task.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"shipped_ptf": "SI50077"}]
            
      
        
