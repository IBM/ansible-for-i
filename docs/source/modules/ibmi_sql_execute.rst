..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_sql_execute.py


ibmi_sql_execute -- Executes a SQL non-DQL(Data Query Language) statement on a remote IBMi node
===============================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The ``ibmi_sql_execute`` module takes the SQL non-DQL(Data Query Language) statement as argument.

The given SQL non-DQL(Data Query Language) statement will be executed on all selected nodes.

Only run one statement at a time.






Parameters
----------

  sql (True, str, None)
    The ``ibmi_sql_execute`` module takes a IBM i SQL non-DQL(Data Query Language) statement to run.


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

   :ref:`IBMi_sql_query_module`
      The official documentation on the **IBMi_sql_query** module.


Examples
--------

.. code-block:: yaml+jinja

    
    - name: Insert one record to table Persons
      ibmi_sql_execute:
        sql: "INSERT INTO Persons VALUES('919665', 'Le', 'Chang', 'Ring Building', 'Beijing')"



Return Values
-------------

  stderr_lines (When rc as non-zero(failure), list, [''])
    The sql statement standard error split in lines


  end (always, str, 2019-12-02 11:07:54.064969)
    The sql statement execution end time


  stdout (always, str, +++ success INSERT INTO Persons VALUES('919665', 'Le', 'Chang', 'Ring Building', 'Beijing'))
    The sql statement standard output


  sql (always, str, INSERT INTO Persons VALUES('919665', 'Le', 'Chang', 'Ring Building', 'Beijing'))
    The sql statement executed by the task


  rc (always, int, 0)
    The sql statement return code (0 means success, non-zero means failure)


  start (always, str, 2019-12-02 11:07:53.757435)
    The sql statement execution start time


  stderr (always, str, )
    The sql statement standard error


  delta (always, str, 0:00:00.307534)
    The sql statement execution delta time


  stdout_lines (When rc as non-zero(failure), list, ["+++ success INSERT INTO Persons VALUES('919665', 'Le', 'Chang', 'Ring Building', 'Beijing')"])
    The sql statement standard output split in lines





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Chang Le(@changlexc)

