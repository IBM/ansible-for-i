
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_fix_group_check.py

.. _ibmi_fix_group_check_module:


ibmi_fix_group_check -- Retrieve the latest PTF group information from PSP server.
==================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The :literal:`ibmi\_fix\_group\_check` module retrieve latest PTF group information from PSP(Preventive Service Planning) server.
- Refer to https://www.ibm.com/support/pages/node/667567 for more details of PSP.
- ALL PTF groups or specific PTF groups are supported.
- A PTF group returns a list of PTFs that the group consists of, while a cumulative PTF returns a package ID.
- The PTF group information is derived from the top level XML web page https://public.dhe.ibm.com/services/us/igsc/PSP/xmldoc.xml with a corresponding XML file at https://public.dhe.ibm.com/services/us/igsc/PSP/ for each PTF group (or text file for a cumulative).





Parameters
----------


     
groups
  The list of the PTF groups number.


  | **required**: False
  | **type**: list
  | **elements**: str
  | **default**: ['\*ALL']


     
timeout
  Timeout in seconds for URL request.


  | **required**: False
  | **type**: int
  | **default**: 60


     
validate_certs
  If set to :literal:`False`\ , the SSL certificate verification will be disabled. It's recommended for test scenario.

  It's recommended to enable the SSL certificate verification for security concern.


  | **required**: False
  | **type**: bool
  | **default**: True




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Check specific PTF groups
     ibm.power_ibmi.ibmi_fix_group_check:
       groups:
         - "SF12345"

   - name: Check the PTF groups without certificate verification
     ibm.power_ibmi.ibmi_fix_group_check:
       groups:
         - "SF12345"
       validate_certs: False




Notes
-----

.. note::
   Ansible hosts file need to specify ansible\_python\_interpreter=/QOpenSys/pkgs/bin/python3.

   If the module is delegated to an IBM i server and SSL certificate verification is enabled, package :literal:`ca-certificates-mozilla` is required.





  

Return Values
-------------


   
                              
       stderr
        | The task standard error
      
        | **returned**: always
        | **type**: str
        | **sample**: PTF groups SF12345 does not exist

            
      
      
                              
       rc
        | The task return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
      
      
                              
       count
        | The number of PTF groups which has been retrieved
      
        | **returned**: always.
        | **type**: int
        | **sample**: 1

            
      
      
                              
       group_info
        | PTF group information.
      
        | **returned**: When rc is zero.
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"description": "SF99738 - 740 Group Security", "package_id": null, "ptf_group_level": 70, "ptf_group_number": "SF99738", "ptf_list": ["SJ02177", "...", "SI70103"], "release": "R740", "release_date": "10/01/2024", "url": "https://public.dhe.ibm.com/services/us/igsc/PSP/SF99738.xml"}]
            
      
        
