..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_reboot.py


ibmi_reboot -- Reboot a machine
===============================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Reboot a IBMi machine, wait for it to go down, come back up, and respond to commands.






Parameters
----------

  pre_reboot_delay (optional, int, 60)
    Seconds to wait before issue the reboot command.


  how_to_end (optional, str, *IMMED)
    Specifies whether the system allows the active subsystem to end processing of active jobs in a controlled manner.

    or whether the system ends the jobs immediately. In either case, the system does perform certain job-cleanup functions.


  end_subsystem_option (optional, str, *DFT)
    Specifies the options to take when ending the active.


  parameters (optional, str, )
    The parameters that PWRDWNSYS command will take.

    Other than options above, all other parameters need to be specified here.

    The default values of parameters for PWRDWNSYS will be taken if not specified.

    Only Install PTF device(INSPTFDEV) is supported now for IBMi 7.3 and above.


  reboot_timeout (optional, int, 1800)
    Maximum seconds to wait for machine to reboot and respond to a test command.

    This timeout is evaluated separately for both reboot verification and test command success so the maximum execution time for the module is twice this amount.


  timeout_option (optional, str, *CONTINUE)
    Specifies the option to take when the system does not end within the time limit specified by the QPWRDWNLMT system value.

    If this time limit is exceeded, the subsequent IPL will be abnormal regardless of the value specified for this parameter.


  post_reboot_delay (optional, int, 60)
    Seconds to wait after the reboot command was successful before attempting to validate the system rebooted successfully.

    This is useful if you want wait for something to settle despite your connection already working.


  reboot_type (optional, str, *IPLA)
    Specifies the point from which the initial program load (IPL) restarts.


  test_command (optional, str, uname)
    Command to run on the rebooted host and expect success from to determine the machine is ready for further tasks.


  msg (optional, str, Reboot initiated by Ansible)
    Message to display to users before reboot.


  controlled_end_delay_time (optional, int, 600)
    Specifies the amount of time(1-99999), in seconds, that the system allows a controlled end to be performed by the active subsystems.

    If the value is greater than 99999, '*NOLIMIT' will be used in PWRDWNSYS commnad.


  connect_timeout (optional, int, 300)
    Maximum seconds to wait for a successful connection to the managed hosts before trying again.

    If unspecified, the default setting for the underlying connection plugin is used.


  ipl_source (optional, str, *PANEL)
    Specifies whether an initial-program-load (IPL) is started from the A-source, B-source or D-source of the system.





Notes
-----

.. note::
   - ansible.cfg needs to specify interpreter_python=/QOpenSys/pkgs/bin/python3(or python2) under[defaults] section.
   - Be careful to use '*CNTRLD' for option how_to_end,
   - you need to specify the appropriate value for all the timout options according to the system performance.


See Also
--------

.. seealso::

   :ref:`reboot_module`
      The official documentation on the **reboot** module.


Examples
--------

.. code-block:: yaml+jinja

    
    - name: Unconditionally reboot the machine with all defaults
      reboot:

    - name: Reboot a slow machine that might have lots of updates to apply
      reboot:
        reboot_timeout: 3600



Return Values
-------------

  rebooted (always, bool, True)
    true if the machine was rebooted


  elapsed (always, int, 553)
    The number of seconds that elapsed waiting for the system to be rebooted.





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Chang Le (@changlexc)

