..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_at.py


ibmi_at -- Schedule a batch job on a remote IBMi node
=====================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The ibmi_at module schedule a batch job on a remote IBMi node






Parameters
----------

  parameters (optional, str, )
    The parameters that ADDJOBSCDE command will take. Other than options above, all other parameters need to be specified here. The default values of parameters for ADDJOBSCDE will be taken if not specified.


  scddate (optional, str, *CURRENT)
    Specifies the date on which the job is submitted.


  cmd (True, str, None)
    Specifies the command that runs in the submitted job.


  scdday (optional, list, *NONE)
    Specifies the day of the week on which the job is submitted.

    The valid value are '*NONE', '*ALL', '*MON', '*TUE', '*WED', '*THU', '*FRI', '*SAT', '*SUN'.


  frequency (True, str, None)
    Specifies how often the job is submitted.


  text (optional, str, *BLANK)
    Specifies text that briefly describes the job schedule entry.


  schtime (optional, str, *CURRENT)
    Specifies the time on the scheduled date at which the job is submitted.


  joblog (optional, bool, False)
    If set to ``true``, append JOBLOG to stderr/stderr_lines.


  job_name (True, str, None)
    Specifies the name of the job schedule entry.





Notes
-----

.. note::
   - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Add a job schedule entry test
      ibmi_at:
        job_name: 'test'
        cmd: 'QSYS/WRKSRVAGT TYPE(*UAK)'
        frequency: '*WEEKLY'
        scddate: '*CURRENT'
        text: 'Test job schedule'



Return Values
-------------

  stderr_lines (always, list, ['CPF5813: File archive in library archlib already exists.', 'CPF7302: File archive not created in library archlib.'])
    The standard error split in lines


  stdout (always, str, CPC1238: Job schedule entry TEST number 000074 added.)
    The standard output


  rc (always, int, 255)
    The action return code (0 means success, non-zero means failure)


  command (always, str, QSYS/ADDJOBSCDE JOB(fish) CMD(QBLDSYSR/CHGSYSSEC OPTION(*CHGPW)) FRQ(*WEEKLY) SCDDATE(*CURRENT) SCDDAY(*NONE) SCDTIME(*CURRENT) TEXT(*BLANK) )
    The execution command


  stderr (always, str, CPF5813: File archive in library archlib already exists.\nCPF7302: File archive not created in library archlib.\n)
    The standard error


  delta (always, str, 0:00:00.307534)
    The execution delta time.


  msg (always, str, Either scddate or scdday need to be *NONE.)
    The execution message.


  stdout_lines (always, list, ['CPC1238: Job schedule entry TEST number 000074 added.'])
    The standard output split in lines





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Peng Zeng Yu (@pengzengyufish)

