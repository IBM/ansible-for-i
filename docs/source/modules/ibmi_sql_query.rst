..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_sql_query.py


ibmi_sql_query -- Executes a SQL DQL(Data Query Language) statement on a remote IBMi node.
==========================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The ``ibmi_sql_query`` module takes the SQL DQL(Data Query Language) statement as argument.

The given SQL DQL(Data Query Language) statement will be executed on all selected nodes.

Only run one statement at a time.






Parameters
----------

  expected_row_count (optional, int, -1)
    The expected row count

    If it is equal or greater than 0, check if the actual row count returned from the query statement is matched with the expected row count

    If it is less than 0, do not check if the actual row count returned from the query statement is matched with the expected row counit


  sql (True, str, None)
    The ``ibmi_sql_query`` module takes a IBM i SQL DQL(Data Query Language) statement to run.


  database (optional, str, )
    Specified database name, usually, its the iasp name, use WRKRDBDIRE to check Relational Database Directory Entries

    Default to use the '*LOCAL' entry





Notes
-----

.. note::
   - Hosts file needs to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)


See Also
--------

.. seealso::

   :ref:`ibmi_sql_execute_module`
      The official documentation on the **ibmi_sql_execute** module.


Examples
--------

.. code-block:: yaml+jinja

    
    - name: Query the data of table Persons
      ibmi_sql_query:
        sql: 'select * from Persons'



Return Values
-------------

  stderr_lines (When rc as non-zero(failure), list, [''])
    The sql statement standard error split in lines


  end (always, str, 2019-12-02 11:07:54.064969)
    The sql statement execution end time


  stdout (When rc as non-zero(failure), str, )
    The sql statement standard output


  rc (always, int, 0)
    The sql statement return code (0 means success)


  start (always, str, 2019-12-02 11:07:53.757435)
    The sql statement execution start time


  delta (always, str, 0:00:00.307534)
    The sql statement execution delta time


  stderr (When rc as non-zero(failure), str, )
    The sql statement standard error


  sql (always, str, select * from Persons)
    The sql statement executed by the task


  stdout_lines (When rc as non-zero(failure), list, [''])
    The sql statement standard output split in lines


  rc_msg (always, str, Generic failure)
    Meaning of the return code


  row (when rc as 0(success), list, [{'LASTNAME': 'Le', 'ID_P': '919665', 'ADDRESS': 'Ring Building', 'FIRSTNAME': 'Chang', 'CITY': 'Beijing'}, {'LASTNAME': 'Li', 'ID_P': '919689', 'ADDRESS': 'Ring Building', 'FIRSTNAME': 'Zhang', 'CITY': 'Shanhai'}])
    The sql query statement result





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Chang Le(@changlexc)

