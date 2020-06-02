..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_synchronize.py


ibmi_synchronize -- Synchronize a save file from ibm i node A to another ibm i node B.
======================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The ibmi_synchronize plugin synchronize a save file from ibm i node A to another ibm i node B.

ibmi_synchronize plugin calls ibmi_sync module

Only support to synchronize save file by now.

For non-IBMi native targets, use the synchronize module instead.

delegate_to must be set to ibm i node A, and set hosts to ibm i node B

Be careful to set delegate_to or hosts to node groups. The synchronized data may be overridden.






Parameters
----------

  dest (optional, str, )
    Path on the destination host that will be synchronized from the source.

    The path must be absolute, and dest must be a ibm i native library. For example, /qsys.lib/test.lib.

    If not specify, dest will be equal to src.


  src (True, str, None)
    Save file path on the source host that will be synchronized to the destination.

    The path must be absolute. For example, /qsys.lib/test.lib/c1.file.


  private_key (optional, str, ~/.ssh/id_rsa)
    Specifies SSH private key path on ibm i node A used to connect to remote ibm i node B.

    The path can be absolute or relative.


  remote_user (optional, str, )
    The user name to connect to the remote ibm i node B.

    If not specify, remote_user will be the ansible_ssh_user of ibm i node B, which stored in ansible inventory.





Notes
-----

.. note::
   - ansible.cfg needs to specify interpreter_python=/QOpenSys/pkgs/bin/python3 under [defaults] section
   - delegate_to must be set to ibm i node A
   - Make sure ssh passwordless login works from ibm i node A to ibm i node B
   - private_key must be a rsa key in the legacy PEM private key format.
   - Doesn't support IASP by now




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Synchronize c1 save file from ibm i node A to another ibm i node B
      ibmi_synchcronize:
        src: '/qsys.lib/test.lib/c1.file'
        remote_user: 'user'
        private_key: '/home/test/id_rsa'
      delegate_to: nodeA



Return Values
-------------

  stderr_lines (always, list, ['Failed to mv file to qsys. Make sure library exists.'])
    The standard error split in lines


  stderr (always, str, Failed to mv file to qsys. Make sure library exists.)
    The standard error


  stdout (always, str, Successfully synchronize file /QSYS.LIB/TEST.LIB/C1.FILE to remote host host.com)
    The standard output


  stdout_lines (always, list, ['Successfully synchronize file /QSYS.LIB/TEST.LIB/C1.FILE to remote host host.com'])
    The standard output split in lines


  delta (always, str, 0:00:00.307534)
    The execution delta time.


  rc (always, int, 255)
    The action return code (0 means success, non-zero means failure)





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Peng Zeng Yu (@pengzengyufish)

