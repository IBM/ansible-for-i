
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_sync_files.py

.. _ibmi_sync_files_module:


ibmi_sync_files -- Synchronize a list of files from current IBM i node A to another IBM i node B.
=================================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_sync_files`` module synchronize a list of files from current IBM i node to another IBM i node.
- Only supports SAVF(.file) format synchronize between QSYS and QSYS.





Parameters
----------


     
dest
  Path on the destination host that will be synchronized from the source.

  The path must be absolute.

  If specify, all the src files will be synchronized to the directory that dest speicified. Individual dest key in src_list will be ignored.

  If not specify, individual dest will be the dest value inputted in src_list.

  If both dest and dest key in src_list are not specify, individual dest will be equal to individual src in src_list.

  Example '/test/dir/'


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


     
src_list
  src files information list on the source host.

  Evey src_list element should be a dict. dict can contain 'src' and 'dest'. 'dest' is optional.

  The src key is the path to the src, and must be absolute.

  The dest key is the path on the destination host that will be synchronized from the source.


  | **required**: True
  | **type**: list
  | **elements**: dict




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Synchronize a list of different types of files to host.com.
     ibmi_sync_files:
       src_list:
         - {'src': '/tmp/c1.file', 'dest': '/qsys.lib/fish.lib/'}
         - {'src': '/qsys.lib/fish.lib/test.file', 'dest': '/qsys.lib/fish.lib'}
         - {'src': '/tmp/c2.SAVF', 'dest': '/qsys.lib/fish.lib/'}
         - {'src': '/tmp/c3.bin', 'dest': '/test/dir'}
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
        | **sample**: Complete synchronize file list to remote host host.com

            
      
      
                              
       stderr
        | The standard error.
      
        | **returned**: always
        | **type**: str
        | **sample**: Exception. not a valid RSA private key file. Use -vvv for more information.

            
      
      
                              
       rc
        | The action return code. 0 means success.
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       msg
        | The general message returned.
      
        | **returned**: always
        | **type**: str
        | **sample**: No files were successfully transferred.

            
      
      
                              
       success_list
        | The success transferred list.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"dest": "/qsys.lib/fish.lib/", "src": "/tmp/c1.file"}, {"dest": "/qsys.lib/fish.lib/", "src": "/tmp/c2.SAVF"}, {"src": "/tmp/c3.log"}]
            
      
      
                              
       fail_list
        | The fail transferred list.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"dest": "/qsys.lib/fish.lib/", "fail_reason": "Can\u0027t sync file to /QSYS.LIB", "src": "/qsys.lib/fish.lib/test.file"}, {"dest": "/qsys.lib/fish.lib/", "fail_reason": "src /qsys.lib/fish.lib/test.file doesn\u0027t exist.", "src": "/tmp/c4.SAVF"}]
            
      
      
                              
       stdout_lines
        | The standard output split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["Complete synchronize file list to remote host host.com"]
            
      
      
                              
       stderr_lines
        | The standard error split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["Exception. not a valid RSA private key file. Use -vvv for more information."]
            
      
        
