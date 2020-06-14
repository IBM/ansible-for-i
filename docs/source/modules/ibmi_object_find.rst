..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/IBM/ansible-for-i/tree/ansible_collection_beta/plugins/modules/ibmi_object_find.py

.. _ibmi_object_find_module:

ibmi_object_find -- Find specific IBM i object(s).
==================================================


.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Return a list of IBM i objects based on specific criteria. Multiple criteria are AND'd together.



Parameters
----------


     
age
  Select objects whose age is equal to or greater than the specified time. Use a negative age to find objects equal to or less than the specified time. You can choose seconds, minutes, hours, days, or weeks by specifying the first letter of any of those \n words (e.g., "1w").


  | **required**: False
  | **type**: str


     
age_stamp
  Choose the object statistic against which we compare age. Default is ctime which is the object creation time.


  | **required**: False
  | **type**: str
  | **default**: ctime
  | **choices**: ctime


     
iasp_name
  The auxiliary storage pool (ASP) where storage is allocated for the object.

  The default value is "*SYSBAS".

  If an IASP name is specified, objects in this ASP group will be returned, including both SYSBAS and IASP.


  | **required**: false
  | **type**: str
  | **default**: *SYSBAS


     
lib_name
  The name of the library that returned objects locate in


  | **required**: False
  | **type**: str
  | **default**: *ALLUSR


     
object_name
  The name of the object that will be returned. Whether regex can be used for object_name is controlled by ``use_regex`` option


  | **required**: false
  | **type**: str
  | **default**: *ALL


     
object_type_list
  One or more system object types separated by either a blank or a comma.


  | **required**: False
  | **type**: str
  | **default**: *ALL


     
size
  Select objects whose size is equal to or greater than the specified size. Use a negative size to find objects equal to or less than the specified size. Unqualified values are in bytes but b, k, m, g, and t can be appended to specify bytes, kilobytes, megabytes, gigabytes, and terabytes, respectively.


  | **required**: False
  | **type**: str


     
use_regex
  Controls whether regex can be used for object_name option. The target IBM i system needs to have the International Components for Unicode (ICU) option installed. It takes time to return result if this option is turned on.


  | **required**: false
  | **type**: bool



Examples
--------

.. code-block:: yaml+jinja

   
   - name:  Find all journals and journal receivers in library WYTEST.
     ibmi_object_find:
       object_name: '*ALL'
       object_type_list: '*JRN *JRNRCV'
       lib_name: 'WYTEST'
       age: '1w'
       age_stamp: 'ctime'

   - name:  Find all the object names that contains 'ABC' with regex.
     ibmi_object_find:
       object_name: 'ABC+'
       object_type_list: '*ALL'
       lib_name: '*ALL'
       use_regex: true

   - name: find library WYTEST in sysbas
     ibmi_object_find:
       lib_name: 'QSYS'
       iasp_name: '*SYSBAS'
       object_name: 'WYTEST'
       object_type_list: "*LIB"

   - name: find object OBJABC in asp group WYTEST2
     ibmi_object_find:
       lib_name: '*ALL'
       iasp_name: 'WYTEST2'
       object_type_list: "*FILE"
       object_name: 'OBJABC'



Notes
-----

.. note::
   Hosts file needs to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)


See Also
--------

.. seealso::

   - :ref:`find_module`


Return Values
-------------


   
                              
       stderr_lines
        | The task execution standard error split in lines
      
        | **returned**: When rc as non-zero(failure)
        | **type**: list      
        | **sample**:

              .. code-block::

                       [""]
            
      
      
                              
       end
        | The task execution end time
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:54.064969

            
      
      
                              
       stdout
        | The task execution standard output
      
        | **returned**: When rc as non-zero(failure)
        | **type**: str
      
      
                              
       object_list
        | The object list returned
      
        | **returned**: when rc as 0(success)
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"IASP_NUMBER": 0, "LAST_RESET_TIMESTAMP": null, "LAST_USED_TIMESTAMP": null, "OBJATTRIBUTE": "SAVF", "OBJCREATED": "2019-02-18T10:48:41", "OBJDEFINER": "USERADMIN", "OBJLIB": "TESTLIB", "OBJNAME": "TESTOBJ1", "OBJOWNER": "WY", "OBJSIZE": 131072, "OBJTYPE": "*FILE", "TEXT": "TEST"}, {"IASP_NUMBER": 0, "LAST_RESET_TIMESTAMP": null, "LAST_USED_TIMESTAMP": null, "OBJATTRIBUTE": "SAVF", "OBJCREATED": "2019-02-18T10:48:41", "OBJDEFINER": "USERAPP", "OBJLIB": "TESTLIB", "OBJNAME": "RING1", "OBJOWNER": "WY", "OBJSIZE": 131072, "OBJTYPE": "*FILE", "TEXT": "test"}]
            
      
      
                              
       start
        | The task execution start time
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:53.757435

            
      
      
                              
       delta
        | The task execution delta time
      
        | **returned**: always
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       stderr
        | The task execution standard error
      
        | **returned**: When rc as non-zero(failure)
        | **type**: str
      
      
                              
       rc
        | The task execution return code (0 means success)
      
        | **returned**: always
        | **type**: int
      
      
                              
       stdout_lines
        | The task execution standard output split in lines
      
        | **returned**: When rc as non-zero(failure)
        | **type**: list      
        | **sample**:

              .. code-block::

                       [""]
            
      
        
