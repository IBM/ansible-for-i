..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_object_find.py


ibmi_object_find -- Find specific IBM i object(s).
==================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Return a list of IBM i objects based on specific criteria. Multiple criteria are AND'd together.






Parameters
----------

  age (False, str, None)
    Select objects whose age is equal to or greater than the specified time. Use a negative age to find objects equal to or less than the specified time. You can choose seconds, minutes, hours, days, or weeks by specifying the first letter of any of those \n words (e.g., "1w").


  age_stamp (False, str, ctime)
    Choose the object statistic against which we compare age. Default is ctime which is the object creation time.


  object_name (optional, str, *ALL)
    The name of the object that will be returned. Whether regex can be used for object_name is controlled by ``use_regex`` option


  object_type_list (False, str, *ALL)
    One or more system object types separated by either a blank or a comma.


  iasp_name (optional, str, *SYSBAS)
    The auxiliary storage pool (ASP) where storage is allocated for the object.

    The default value is "*SYSBAS".

    If an IASP name is specified, objects in this ASP group will be returned, including both SYSBAS and IASP.


  use_regex (optional, bool, False)
    Controls whether regex can be used for object_name option. The target IBM i system needs to have the International Components for Unicode (ICU) option installed. It takes time to return result if this option is turned on.


  lib_name (False, str, *ALLUSR)
    The name of the library that returned objects locate in


  size (False, str, None)
    Select objects whose size is equal to or greater than the specified size. Use a negative size to find objects equal to or less than the specified size. Unqualified values are in bytes but b, k, m, g, and t can be appended to specify bytes, kilobytes, megabytes, gigabytes, and terabytes, respectively.





Notes
-----

.. note::
   - Hosts file needs to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)


See Also
--------

.. seealso::

   :ref:`find_module`
      The official documentation on the **find** module.


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



Return Values
-------------

  stderr_lines (When rc as non-zero(failure), list, [''])
    The task execution standard error split in lines


  end (always, str, 2019-12-02 11:07:54.064969)
    The task execution end time


  stdout (When rc as non-zero(failure), str, )
    The task execution standard output


  object_list (when rc as 0(success), list, [{'OBJLIB': 'TESTLIB', 'OBJCREATED': '2019-02-18T10:48:41', 'OBJOWNER': 'WY', 'TEXT': 'TEST', 'OBJDEFINER': 'USERADMIN', 'IASP_NUMBER': 0, 'OBJSIZE': 131072, 'OBJNAME': 'TESTOBJ1', 'OBJATTRIBUTE': 'SAVF', 'OBJTYPE': '*FILE', 'LAST_USED_TIMESTAMP': None, 'LAST_RESET_TIMESTAMP': None}, {'OBJLIB': 'TESTLIB', 'OBJCREATED': '2019-02-18T10:48:41', 'OBJOWNER': 'WY', 'TEXT': 'test', 'OBJDEFINER': 'USERAPP', 'IASP_NUMBER': 0, 'OBJSIZE': 131072, 'OBJNAME': 'RING1', 'OBJATTRIBUTE': 'SAVF', 'OBJTYPE': '*FILE', 'LAST_USED_TIMESTAMP': None, 'LAST_RESET_TIMESTAMP': None}])
    The object list returned


  start (always, str, 2019-12-02 11:07:53.757435)
    The task execution start time


  delta (always, str, 0:00:00.307534)
    The task execution delta time


  stderr (When rc as non-zero(failure), str, )
    The task execution standard error


  rc (always, int, 0)
    The task execution return code (0 means success)


  stdout_lines (When rc as non-zero(failure), list, [''])
    The task execution standard output split in lines





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Wang Yun(@airwangyun)

