
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_synchronize.py

.. _ibmi_synchronize_module:


ibmi_synchronize -- Synchronize a save file from IBM i node A to another IBM i node B
=====================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_synchronize`` plugin synchronize a save file from IBM i node A to another IBM i node B.
- ``ibmi_synchronize`` plugin calls ibmi_sync module.
- Only support to synchronize save file by now.
- For non-IBMi native targets, use the synchronize module instead.
- delegate_to must be set to IBM i node A, and set hosts to IBM i node B.
- Be careful to set delegate_to or hosts to node groups. The synchronized data may be overridden.





Parameters
----------


     
dest
  Path on the destination host that will be synchronized from the source.

  The path must be absolute, and dest must be a IBM i native library. For example, /qsys.lib/test.lib.

  If not specify, dest will be equal to src.


  | **required**: false
  | **type**: str


     
private_key
  Specifies SSH private key path on IBM i node A used to connect to remote IBM i node B.

  The path can be absolute or relative.


  | **required**: false
  | **type**: str
  | **default**: ~/.ssh/id_rsa


     
remote_user
  The user name to connect to the remote IBM i node B.

  If not specify, remote_user will be the ansible_ssh_user of IBM i node B, which stored in ansible inventory.


  | **required**: false
  | **type**: str


     
src
  Save file path on the source host that will be synchronized to the destination.

  The path must be absolute. For example, /qsys.lib/test.lib/c1.file.


  | **required**: True
  | **type**: str




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Synchronize c1 save file from IBM i node A to another IBM i node B.
     ibmi_synchcronize:
       src: '/qsys.lib/test.lib/c1.file'
       remote_user: 'user'
       private_key: '/home/test/id_rsa'
     delegate_to: nodeA




Notes
-----

.. note::
   ansible.cfg needs to specify interpreter_python=/QOpenSys/pkgs/bin/python3 under [defaults] section.

   delegate_to must be set to IBM i node A.

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
            
      
        
