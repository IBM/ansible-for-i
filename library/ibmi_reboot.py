#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Le Chang <changle@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
module: ibmi_reboot
short_description: Reboot a machine
description:
    - Reboot a IBMi machine, wait for it to go down, come back up, and respond to commands.
version_added: "1.1"
options:
  pre_reboot_delay:
    description:
      - Seconds to wait before issue the reboot command.
    type: int
    default: 60
  post_reboot_delay:
    description:
      - Seconds to wait after the reboot command was successful before attempting to validate the system rebooted successfully.
      - This is useful if you want wait for something to settle despite your connection already working.
    type: int
    default: 60
  reboot_timeout:
    description:
      - Maximum seconds to wait for machine to reboot and respond to a test command.
      - This timeout is evaluated separately for both reboot verification and test command success so the
        maximum execution time for the module is twice this amount.
    type: int
    default: 900
  connect_timeout:
    description:
      - Maximum seconds to wait for a successful connection to the managed hosts before trying again.
      - If unspecified, the default setting for the underlying connection plugin is used.
    type: int
    default: 900
  test_command:
    description:
      - Command to run on the rebooted host and expect success from to determine the machine is ready for further tasks.
    type: str
    default: 'uname'
  msg:
    description:
      - Message to display to users before reboot.
    type: str
    default: Reboot initiated by Ansible
  how_to_end:
    description:
      - Specifies whether the system allows the active subsystem to end processing of active jobs in a controlled manner.
      - or whether the system ends the jobs immediately. In either case, the system does perform certain job-cleanup functions.
    type: str
    default: '*CNTRLD'
    choices: ['*IMMED', '*CNTRLD']
  controlled_end_delay_time:
    description:
      - Specifies the amount of time(1-99999), in seconds, that the system allows a controlled end to be performed by the active subsystems.
      - If the value is greater than 99999, '*NOLIMIT' will be used in PWRDWNSYS commnad.
    type: int
    default: 3600
  reboot_type:
    description:
      - Specifies the point from which the initial program load (IPL) restarts.
    type: str
    default: '*IPLA'
    choices: ['*IPLA', '*SYS', '*FULL']
  ipl_source:
    description:
      - Specifies whether an initial-program-load (IPL) is started from the A-source, B-source or D-source of the system.
    type: str
    default: '*PANEL'
    choices: ['*PANEL', 'A', 'B', 'D', '*IMGCLG']
  end_subsystem_option:
    description:
      - Specifies the options to take when ending the active.
    type: str
    default: '*DFT'
    choices: ['*DFT', '*NOJOBLOG', '*CHGPTY', '*CHGTSL']
  timeout_option:
    description:
      - Specifies the option to take when the system does not end within the time limit specified by the QPWRDWNLMT system value.
      - If this time limit is exceeded, the subsequent IPL will be abnormal regardless of the value specified for this parameter.
    type: str
    default: '*CONTINUE'
    choices: ['*CONTINUE', '*MSD', '*SYSREFCDE']
  install_ptf_device:
    description:
      - Specifies whether Program Temporary Fixes (PTFs) should be installed before the system is powered down.
    type: str
    default: '*NONE'
notes:
- ansible.cfg needs to specify interpreter_python=/QOpenSys/pkgs/bin/python3(or python2) under[defaults] section
- OPTION('*CNTRLD') in PWRDWNSYS is not used in the ibmi_reboot module.
seealso:
- module: reboot
author:
- Chang Le (@changlexc)
'''

EXAMPLES = r'''
- name: Unconditionally reboot the machine with all defaults
  reboot:

- name: Reboot a slow machine that might have lots of updates to apply
  reboot:
    reboot_timeout: 3600
'''

RETURN = r'''
rebooted:
  description: true if the machine was rebooted
  returned: always
  type: bool
  sample: true
elapsed:
  description: The number of seconds that elapsed waiting for the system to be rebooted.
  returned: always
  type: int
  sample: 553
'''
