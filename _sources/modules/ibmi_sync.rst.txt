
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_sync.py

.. _ibmi_sync_module:


ibmi_sync -- Synchronize a save file from current IBM i node A to another IBM i node B.
=======================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_sync`` module synchronize a save file from current IBM i node to another IBM i node.
- Only support to synchronize save file by now.
- For non-IBMi native targets, use the synchronize module instead.





Parameters
----------


     
dest
  Path on the destination host that will be synchronized from the source.

  The path must be absolute, and dest must be a IBM i native library. For example, /qsys.lib/test.lib.

  If not specify, dest will be equal to src.


  | **required**: false
  | **type**: str


     
private_key
  Specifies SSH private key used to connect to remote IBM i host.

  The path can be absolute or relative.


  | **required**: false
  | **type**: path
  | **default**: ~/.ssh/id_rsa


     
remote_host
  The remote IBM i node address.

  Can be IP or host name.


  | **required**: True
  | **type**: str


     
remote_user
  The user name to connect to the remote IBM i node.


  | **required**: True
  | **type**: str


     
src
  Save file path on the source host that will be synchronized to the destination.

  The path must be absolute, and src must be a IBM i native library. For example, /qsys.lib/test.lib/c1.file.


  | **required**: True
  | **type**: str




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Synchronize c1 save file to host.com.
     ibmi_sync:
       src: '/qsys.lib/test.lib/c1.file'
       remote_host: 'host.com'
       remote_user: 'user'
       private_key: '/home/test/id_rsa'




Notes
-----

.. note::
   Need install paramiko package on target IBM i.

   Make sure ssh passwordless login works from IBM i node A to IBM i node B.

   private_key must be a rsa key in the legacy PEM private key format.

   Doesn't support IASP by now.






Return Values
-------------


   
                              
       delta
        | The execution delta time.
      
        | **returned**: always
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       stdout
        | The standard output.
      
        | **returned**: always
        | **type**: str
        | **sample**: Successfully synchronize file /QSYS.LIB/TEST.LIB/C1.FILE to remote host host.com

            
      
      
                              
       stderr
        | The standard error.
      
        | **returned**: always
        | **type**: str
        | **sample**: Failed to mv file to qsys. Make sure library exists.

            
      
      
                              
       rc
        | The action return code. 0 means success.
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       stdout_lines
        | The standard output split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["Successfully synchronize file /QSYS.LIB/TEST.LIB/C1.FILE to remote host host.com"]
            
      
      
                              
       stderr_lines
        | The standard error split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["Failed to mv file to qsys. Make sure library exists."]
            
      
        
