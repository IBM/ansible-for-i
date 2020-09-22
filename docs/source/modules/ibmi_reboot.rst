
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_reboot.py

.. _ibmi_reboot_module:


ibmi_reboot -- Reboot an IBM i machine
======================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Reboot a IBM i machine, wait for it to go down, come back up, and respond to commands.





Parameters
----------


     
become_user
  The name of the user profile that the IBM i task will run under.

  Use this option to set a user with desired privileges to run the task.


  | **required**: false
  | **type**: str


     
become_user_password
  Use this option to set the password of the user specified in ``become_user``.


  | **required**: false
  | **type**: str


     
connect_timeout
  Maximum seconds to wait for a successful connection to the managed hosts before trying again.

  If unspecified, the default setting for the underlying connection plugin is used.


  | **required**: false
  | **type**: int
  | **default**: 300


     
controlled_end_delay_time
  Specifies the amount of time(1-99999), in seconds, that the system allows a controlled end to be performed by the active subsystems.

  If the value is greater than 99999, ``*NOLIMIT`` will be used in PWRDWNSYS commnad.


  | **required**: false
  | **type**: int
  | **default**: 600


     
end_subsystem_option
  Specifies the options to take when ending the active.


  | **required**: false
  | **type**: str
  | **default**: \*DFT
  | **choices**: \*DFT, \*NOJOBLOG, \*CHGPTY, \*CHGTSL


     
how_to_end
  Specifies whether the system allows the active subsystem to end processing of active jobs in a controlled manner. or whether the system ends the jobs immediately. In either case, the system does perform certain job-cleanup functions.


  | **required**: false
  | **type**: str
  | **default**: \*IMMED
  | **choices**: \*IMMED, \*CNTRLD


     
ipl_source
  Specifies whether an initial-program-load (IPL) is started from the A-source, B-source or D-source of the system.


  | **required**: false
  | **type**: str
  | **default**: \*PANEL
  | **choices**: \*PANEL, A, B, D, \*IMGCLG


     
msg
  Message to display to users before reboot.


  | **required**: false
  | **type**: str
  | **default**: Reboot initiated by Ansible


     
parameters
  The parameters that PWRDWNSYS command will take.

  Other than options above, all other parameters need to be specified here.

  The default values of parameters for PWRDWNSYS will be taken if not specified.

  Only Install PTF device(INSPTFDEV) is supported now for IBMi 7.3 and above.


  | **required**: false
  | **type**: str


     
post_reboot_delay
  Seconds to wait after the reboot command was successful before attempting to validate the system rebooted successfully.

  This is useful if you want wait for something to settle despite your connection already working.


  | **required**: false
  | **type**: int
  | **default**: 60


     
pre_reboot_delay
  Seconds to wait before issue the reboot command.


  | **required**: false
  | **type**: int
  | **default**: 60


     
reboot_timeout
  Maximum seconds to wait for machine to reboot and respond to a test command.

  This timeout is evaluated separately for both reboot verification and test command success so the maximum execution time for the module is twice this amount.


  | **required**: false
  | **type**: int
  | **default**: 1800


     
reboot_type
  Specifies the point from which the initial program load (IPL) restarts.


  | **required**: false
  | **type**: str
  | **default**: \*IPLA
  | **choices**: \*IPLA, \*SYS, \*FULL


     
test_command
  Command to run on the rebooted host and expect success from to determine the machine is ready for further tasks.


  | **required**: false
  | **type**: str
  | **default**: uname


     
timeout_option
  Specifies the option to take when the system does not end within the time limit specified by the QPWRDWNLMT system value.

  If this time limit is exceeded, the subsequent IPL will be abnormal regardless of the value specified for this parameter.


  | **required**: false
  | **type**: str
  | **default**: \*CONTINUE
  | **choices**: \*CONTINUE, \*MSD, \*SYSREFCDE




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Unconditionally reboot the machine with all defaults
     reboot:

   - name: Reboot a slow machine that might have lots of updates to apply
     reboot:
       reboot_timeout: 3600

   - name: Unconditionally reboot the machine with become user
     reboot:
       become_user: 'USER'
       become_user_password: 'yourpassword'




Notes
-----

.. note::
   ansible.cfg needs to specify interpreter_python=/QOpenSys/pkgs/bin/python3 under[defaults] section.

   Be careful to use ``*CNTRLD`` for option how_to_end, you need to specify the appropriate value for all the timout options according to the system performance.



See Also
--------

.. seealso::

   - :ref:`reboot_module`



Return Values
-------------


   
                              
       rebooted
        | true if the machine was rebooted
      
        | **returned**: always
        | **type**: bool      
        | **sample**:

              .. code-block::

                       true
            
      
      
                              
       elapsed
        | The number of seconds that elapsed waiting for the system to be rebooted.
      
        | **returned**: always
        | **type**: int
        | **sample**: 553

            
      
        
