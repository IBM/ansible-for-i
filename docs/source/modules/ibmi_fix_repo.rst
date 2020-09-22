
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_fix_repo.py

.. _ibmi_fix_repo_module:


ibmi_fix_repo -- Manipulate the PTF database via sqlite3
========================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_fix_repo`` module manipulate the PTF database via sqlite3.
- Required dependencies are ``SQLite3 >= 3.26`` and python module ``requests``.
- Install them using ``yum install libsqlite3`` and ``pip3 install requests``





Parameters
----------


     
action
  The action the ``ibmi_fix_repo`` module takes towards the PTF database.

  ``add``, ``update``, ``find``, ``delete`` or ``clear``.


  | **required**: True
  | **type**: str


     
checksum
  Specified if check the ptf/group image files as well when checking database


  | **required**: false
  | **type**: bool


     
database
  Specified database file name, e.g. '/tmp/testdb.sqlite3'


  | **required**: false
  | **type**: str
  | **default**: /tmp/testdb.sqlite3


     
parameters
  The binding parameters for the action executed by the task.


  | **required**: false
  | **type**: list
  | **elements**: dict


     
type
  The type of the target, ``single_ptf``, ``ptf_group`` or ``download_status``.


  | **required**: false
  | **type**: str




Examples
--------

.. code-block:: yaml+jinja

   
   - name: add some group records
     ibmi_fix_repo:
       database: '/tmp/testdb.sqlite3'
       action: 'add'
       type: 'ptf_group'
       checksum: true
       parameters:
         - {'order_id':'2020579181', 'file_path':'/QIBM/UserData/OS/Service/ECS/PTF/2020579181'}
   - name: query some PTFs records
     ibmi_fix_repo:
       database: "/tmp/testdb.sqlite3"
       action: "find"
       type: 'ptf_group'
       parameters:
         - {'ptf_group_number':'SF99738', 'ptf_group_level':'10'}
   - name: delete some PTFs records
     ibmi_fix_repo:
       database: "/tmp/testdb.sqlite3"
       action: "delete"
       type: 'ptf_group'
       parameters:
         - {'ptf_group_number':'SF99738', 'ptf_group_level':'10'}
   - name: run sql to drop the table
     ibmi_fix_repo:
       database: "/tmp/testdb.sqlite3"
       action: "clear"
       type: 'ptf_group'









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
      
        | **returned**: when action is 'update', 'add' or 'delete'
        | **type**: str
        | **sample**: 1

            
      
      
                              
       rows
        | The result of the found PTFs.
      
        | **returned**: when action is 'find'
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"add_time": "2020-08-17 00:26:01", "checksum": "d02367d07c5ef43a5722a1ad2c36034409aad2fe", "description": "SF99738 740 Group Security", "download_time": "2020-08-17 00:26:01", "file_name": "S6582V01.BIN", "file_path": "/QIBM/UserData/OS/Service/ECS/PTF/2020579181", "id": 1, "order_id": "2020579181", "product": null, "ptf_group_level": 10, "ptf_group_number": "SF99738", "ptf_group_status": null, "ptf_list": ["SI69187", "SI69189", "SI69886", "SI70103", "SI70725", "SI70734", "SI70767", "SI70819", "SI70961", "SI71097", "SI71746", "SI72577", "SI72646", "SI73284", "SI73415", "SI73430", "SI73482"], "release": "R740", "release_date": "07/07/2020"}]
            
      
      
                              
       sql
        | The formated sql statement executed by the task.
      
        | **returned**: always
        | **type**: str
        | **sample**: SELECT \* FROM ptf_group_image_info WHERE ptf_group_number=:ptf_group_number AND ptf_group_level=:ptf_group_level

            
      
      
                              
       parameters
        | The input binding parameters for the sql statement executed by the task.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"ptf_group_level": "10", "ptf_group_number": "SF99738"}]
            
      
        
