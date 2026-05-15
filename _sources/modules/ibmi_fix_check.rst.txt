
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_fix_check.py

.. _ibmi_fix_check_module:


ibmi_fix_check -- Retrieve the latest PTF group information from PSP server.
============================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The \ :literal:`ibmi\_fix\_check`\  module retrieve latest PTF group information from PSP(Preventive Service Planning) server.
- Refer to https://www.ibm.com/support/pages/node/667567 for more details of PSP.
- ALL PTF groups or specific PTF groups are supported.





Parameters
----------


     
expanded_requisites
  Deep search all its required PTFs.


  | **required**: False
  | **type**: bool


     
groups
  The list of the PTF groups number.


  | **required**: False
  | **type**: list
  | **elements**: str


     
ptfs
  The list of the PTF number.


  | **required**: False
  | **type**: list
  | **elements**: str


     
timeout
  Timeout in seconds for URL request.


  | **required**: False
  | **type**: int
  | **default**: 60


     
validate_certs
  If set to \ :literal:`False`\ , the SSL certificate verification will be disabled. It's recommended for test scenario.

  It's recommended to enable the SSL certificate verification for security concern.


  | **required**: False
  | **type**: bool
  | **default**: True




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Check specific PTF groups
     ibm.power_ibmi.ibmi_fix_check:
       groups:
         - "SF12345"

   - name: Check the PTF groups without certificate verification
     ibm.power_ibmi.ibmi_fix_check:
       groups:
         - "SF12345"
       validate_certs: False




Notes
-----

.. note::
   Ansible hosts file need to specify ansible\_python\_interpreter=/QOpenSys/pkgs/bin/python3.

   If the module is delegated to an IBM i server and SSL certificate verification is enabled, package \ :literal:`ca-certificates-mozilla`\  is required.





  

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

                       [{"PTF_GROUP_LEVEL": "46", "PTF_GROUP_NUMBER": "SF99115", "RELEASE": "R610", "RELEASE_DATE": "09/28/2015", "TITLE": "610 IBM HTTP Server for i"}]
            
      
      
                              
       ptf_info
        | PTF information.
      
        | **returned**: When rc is zero.
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"ptf_id": "SI71691", "req_list": [{"ptf_id": "SI70931", "req_type": "PRE"}]}]
            
      
        
