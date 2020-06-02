..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_copy.py


ibmi_copy -- Copy a save file from local to a remote IBMi node
==============================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The ibmi_copy copies a save file from local to a remote IBMi node.

ibmi_copy will not restore save file on IBMi node.

For non-IBMi native targets, use the copy module instead.






Parameters
----------

  src (True, str, None)
    Local path to a save file to copy to the remote server.

    This can be absolute or relative.


  force (optional, bool, False)
    Influence whether the remote save file must always be replaced.

    If ``yes``, the remote save file will be replaced.

    If ``no``, the save file will only be transferred if the destination does not exist.


  backup (optional, bool, False)
    If set force true and save file already exists on remote, rename the exists remote save file so you can get the original file back.

    The backup save file name will be the original file name+number[1:9]. For example, the origial file name is obja, then rename the original file to obja1. If obja1 already exists, then rename the original file to obja2... util obja9, then report error.

    Only works when force is True.


  lib_name (True, str, None)
    Remote library where the save file should be copied to.





Notes
-----

.. note::
   - ansible.cfg needs to specify interpreter_python=/QOpenSys/pkgs/bin/python3(or python2) under [defaults] section


See Also
--------

.. seealso::

   :ref:`copy_module`
      The official documentation on the **copy** module.


Examples
--------

.. code-block:: yaml+jinja

    
    - name: Copy test.file on local to a remote IBMi.
      ibmi_copy:
        src: '/backup/test.file'
        lib_name: 'testlib'
        force: true
        backup: true



Return Values
-------------

  src (always, str, /backup/test.file)
    Local absolute path to a save file to copy to the remote server.


  stderr (always, list, ['CPF5813: File TEST in library TESTLIB already exists.', 'CPF7302: File TEST not created in library TESTLIB.'])
    The copy standard error


  stdout (always, list, File TEST in library TESTLIB already exists.)
    The copy standard output


  dest (always, str, /QSYS.LIB/TESTLIB.LIB/TEST.FILE)
    Remote absolute path where the file is copied to.


  delta (always, str, 0:00:00.307534)
    The copy execution delta time when file is renewed.


  msg (always, str, File is successfully copied.)
    The fetch execution message.





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Peng Zeng Yu (@pengzengyufish)

