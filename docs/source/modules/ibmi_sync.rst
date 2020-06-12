..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/IBM/ansible-for-i/tree/ansible_collection_beta/plugins/modules/ibmi_sync.py

.. _ibmi_sync_module:

ibmi_sync -- Synchronize a save file from current ibm i node A to another ibm i node B.
=======================================================================================


.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ibmi_sync module synchronize a save file from current ibm i node to another ibm i node.
- Only support to synchronize save file by now.
- For non-IBMi native targets, use the synchronize module instead.



Parameters
----------


     
dest
  Path on the destination host that will be synchronized from the source.

  The path must be absolute, and dest must be a ibm i native library. For example, /qsys.lib/test.lib.

  If not specify, dest will be equal to src.


  | **required**: false
  | **type**: str


     
private_key
  Specifies SSH private key used to connect to remote ibm i host.

  The path can be absolute or relative.


  | **required**: false
  | **type**: path
  | **default**: ~/.ssh/id_rsa


     
remote_host
  The remote ibm i node address.

  Can be IP or host name.


  | **required**: True
  | **type**: str


     
remote_user
  The user name to connect to the remote ibm i node.


  | **required**: True
  | **type**: str


     
src
  Save file path on the source host that will be synchronized to the destination.

  The path must be absolute, and src must be a ibm i native library. For example, /qsys.lib/test.lib/c1.file.


  | **required**: True
  | **type**: str



Examples
--------

.. code-block:: yaml+jinja

   
   - name: Synchronize c1 save file to host.com
     ibmi_sync:
       src: '/qsys.lib/test.lib/c1.file'
       remote_host: 'host.com'
       remote_user: 'user'
       private_key: '/home/test/id_rsa'



Notes
-----

.. note::
   Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3

   Make sure ssh passwordless login works from ibm i node A to ibm i node B

   private_key must be a rsa key in the legacy PEM private key format

   Doesn't support IASP by now




Return Values
-------------


   
                              
       stderr_lines
        | The standard error split in lines
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["Failed to mv file to qsys. Make sure library exists."]
            
      
      
                              
       stderr
        | The standard error
      
        | **returned**: always
        | **type**: str
        | **sample**: Failed to mv file to qsys. Make sure library exists.

            
      
      
                              
       stdout
        | The standard output
      
        | **returned**: always
        | **type**: str
        | **sample**: Successfully synchronize file /QSYS.LIB/TEST.LIB/C1.FILE to remote host host.com

            
      
      
                              
       stdout_lines
        | The standard output split in lines
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["Successfully synchronize file /QSYS.LIB/TEST.LIB/C1.FILE to remote host host.com"]
            
      
      
                              
       delta
        | The execution delta time.
      
        | **returned**: always
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       rc
        | The action return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
        
