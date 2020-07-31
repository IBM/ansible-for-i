
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_module_config.py

.. _ibmi_module_config_module:


ibmi_module_config -- Configures managed nodes settings
=======================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_module_config`` module configures the managed nodes settings, like module log settings.





Parameters
----------


     
config_dir
  The configuration file directory.

  When set to ``home``, the configurations takes effect for the current user.

  When set to ``etc``, the configurations takes effect for all the users.


  | **required**: false
  | **type**: str
  | **default**: home
  | **choices**: etc, home


     
log_dir
  The directory of the modules log file.


  | **required**: false
  | **type**: str
  | **default**: /var/log


     
log_file
  The modules log file name.


  | **required**: false
  | **type**: str
  | **default**: ibmi_ansible_modules.log


     
log_level
  The log level setting.

  critical > error > warning > info > debug

  debug, print all the log

  info, print info,warning,error,critical

  warning, print warning,error,critical

  error, print error,critical

  critical, print critical only


  | **required**: false
  | **type**: str
  | **default**: info
  | **choices**: debug, info, warning, error, critical


     
max_log_size_mb
  The maximum size of the modules log file, if the log file is larger that this value, an archieve(zip) will be occurred.


  | **required**: false
  | **type**: int
  | **default**: 5


     
no_log
  If set to ``true``, no module log will be written on managed nodes.


  | **required**: false
  | **type**: bool


     
section
  The section to be configured.

  When set to ``dump``, the current configuration will be displayed


  | **required**: True
  | **type**: str
  | **choices**: log_config, dump




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Config the logging as debug level
     ibmi_module_config:
       section: log_config
       config_dir: home
       log_level: debug






See Also
--------

.. seealso::

   - :ref:`ibmi_cl_command_module`



Return Values
-------------


   
                              
       version
        | The module version string.
      
        | **returned**: always
        | **type**: str
        | **sample**: 1.0.0

            
      
      
                              
       rc
        | The return code (0 means success, non-zero means failure).
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       msg
        | The message descript the return value
      
        | **returned**: always
        | **type**: str
        | **sample**: Success to confiure Ansible module settings

            
      
      
                              
       settings
        | The content of current settings
      
        | **returned**: when rc is 0 and the section is 'dump'
        | **type**: dict      
        | **sample**:

              .. code-block::

                       {"log_config": {"log_dir": "/var/log", "log_file": "ibmi_ansible_modules.log", "log_level": "DEBUG", "max_log_size_mb": 5, "no_log": false}, "time": "2020-06-28 22:01:57.881370"}
            
      
        
