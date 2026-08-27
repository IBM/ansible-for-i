
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_download_fix_from_cloud.py

.. _ibmi_download_fix_from_cloud_module:


ibmi_download_fix_from_cloud -- Download fix using the cloud API to Electronic Fix Delivery (EFD).
==================================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The \ :literal:`ibmi\_download\_fix\_from\_cloud`\  module downloads fixes using a cloud API to Electronic Fix Delivery (EFD). This allows fixes to be downloaded to a Linux server for those environments where it is not possible to download to an IBM i server, e.g., due to network restrictions. Users should continue to use module ibmi\_download\_fix (based on the SNDPTFORD CL command) for downloading fixes to an IBM i server.
- Only individual PTFs can be downloaded due to current cloud API limitations.
- Individual PTFs are only provided in save files due to current cloud API limitations.
- The downloaded save files and cover letters will have sym links created in the download directory to follow naming protocols for these files on the IBM i server in the QGPL library. The PTF file link is "Q\<ptf\_id\>.FILE" and the cover letter file link is "Q\<pfd\_id\>.MBR".
- Future support will include virtual images for PTFS, PTF groups, and cumulative PTF packages.





Parameters
----------


     
clean_directory
  Clean out contents of specified directory prior to download.


  | **required**: False
  | **type**: bool


     
credentials
  Machine credentials used to validate entitlement for the requested fix.

  Includes fields for 'machine\_model', 'machine\_type', 'serial\_number', and 'country'. This information can be determined from the ibmi\_facts module output.


  | **required**: True
  | **type**: dict


     
directory
  Directory to download the fix files to. The directory is created if it does not already exist. The full or absolute directory path must be specified.


  | **required**: True
  | **type**: str


     
include_requisites
  Specifies if requisite PTFs should be included with the ordered PTFs.


  | **required**: False
  | **type**: bool


     
operation
  The various operations include

  Download the fix (includes validating fix entitlement based on the provided credentials).

  Validate machine entitlement for the fix based on credentials provided. No download occurs.

  Preview the fix. Useful for viewing the pre/co-requisite fixes. No download occurs.


  | **required**: False
  | **type**: str
  | **default**: download
  | **choices**: download, validate, preview


     
ptf_id
  Specify the identifier of the PTF information being ordered.


  | **required**: True
  | **type**: str


     
time_out
  The max time that the module waits for the download to complete.

  The unit can be 's', 'm', 'h', 'd' and 'w'.

  Future parameter to enforce. Currently we only enforce the recommended 2 minute timeout for cloud API handshake and do not time out for the PTF image download, but we plan to incorporate an enforced time out that factors in the image download time in a future release.


  | **required**: False
  | **type**: str
  | **default**: 15m




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Download an individual PTF
     ibm.power_ibmi.ibmi_download_fix_from_cloud:
       ptf_id: 'SJ08024'
       credentials: {
         'machine_model': 'HEX',
         'machine_type': '9080',
         'serial_number': 'XXXXXXX',
         'country': 'US'
       }
       directory: "~/PTFs/SJ08024"
       include_requisites: false








  

Return Values
-------------


   
                              
       delta
        | The module execution delta time.
      
        | **returned**: always
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       stdout
        | The last command standard output.
      
        | **returned**: always
        | **type**: str
      
      
                              
       stderr
        | The last command standard error.
      
        | **returned**: always
        | **type**: str
      
      
                              
       cmd
        | The last command executed.
      
        | **returned**: always
        | **type**: str
      
      
                              
       rc
        | The last command return code. 0 means success.
      
        | **returned**: always
        | **type**: int
      
      
                              
       entitlement_verified
        | Returns whether the software entitlement for the fix is verified with the provided machine credentials. Returns true if the machine has authorized access to the software fix. This is only applicable for the validation and download operations where credential checking occurs.
      
        | **returned**: always (however, the result is not applicable to the preview operation)
        | **type**: bool      
        | **sample**:

              .. code-block::

                       true
            
      
      
                              
       msg
        | The execution message.
      
        | **returned**: always.
        | **type**: str
      
      
                              
       updates
        | Updates recieved from EFD portal after sending the payload. Includes information on the fixes with the preview operation. Includes information on the downloaded files with the the download operation. Provided in JSON format (list of dictionaries).
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"applies_to_version": "V7R6M0", "description": "JDK 80-32 SR8 FP55 IBM Technology for Java", "files": [{"description": "DeploymentDescriptor", "descriptor": "metadata/deployment-descriptor.fix", "hash": "E4AMkam85CBpdYpmhtZra5h3BEagg7UVtuchaGI+YA8=", "hashAlgorithm": "SHA-256", "size": 4924, "url": "https://esupport.ibm.com/eccedge/fix/dhe/delivery04-bld/sar/CMA/ISA/0dmyw/0/SJ08024.dd.xml", "url_type": "edge", "urls": [{"type": "edge", "url": "https://esupport.ibm.com/eccedge/fix/dhe/delivery04-bld/sar/CMA/ISA/0dmyw/0/SJ08024.dd.xml"}, {"type": "edge", "url": "https://esupport.ibm.com/eccedge/fix/dhe/delivery04-mul/sar/CMA/ISA/0dmyw/0/SJ08024.dd.xml"}, {"type": "edge", "url": "https://delivery04.mul.dhe.ibm.com/sar/CMA/ISA/0dmyw/0/SJ08024.dd.xml"}]}, {"description": "PackageDescriptor", "descriptor": "metadata/package-descriptor.fix", "hash": "f2ItcEw3a2jlihlfM+wIPwy/667DNPZ6fxZTHhNg/cw=", "hashAlgorithm": "SHA-256", "size": 2209, "url": "https://esupport.ibm.com/eccedge/fix/dhe/delivery04-bld/sar/CMA/ISA/0dmyw/0/SJ08024.pd.sdd", "url_type": "edge", "urls": [{"type": "edge", "url": "https://esupport.ibm.com/eccedge/fix/dhe/delivery04-bld/sar/CMA/ISA/0dmyw/0/SJ08024.pd.sdd"}, {"type": "edge", "url": "https://esupport.ibm.com/eccedge/fix/dhe/delivery04-mul/sar/CMA/ISA/0dmyw/0/SJ08024.pd.sdd"}, {"type": "edge", "url": "https://delivery04.mul.dhe.ibm.com/sar/CMA/ISA/0dmyw/0/SJ08024.pd.sdd"}]}, {"description": "Savefile", "descriptor": "data/installable-unit.fix", "hash": "tGjPjB+eW0UtF8hA57Epcpd3M4qOn6V/yXiPU1H+Yn4=", "hashAlgorithm": "SHA-256", "size": 149526432, "url": "https://esupport.ibm.com/eccedge/fix/dhe/delivery04-bld/sar/CMA/ISA/0dmyw/0/SJ08024.savf", "url_type": "edge", "urls": [{"type": "edge", "url": "https://esupport.ibm.com/eccedge/fix/dhe/delivery04-bld/sar/CMA/ISA/0dmyw/0/SJ08024.savf"}, {"type": "edge", "url": "https://esupport.ibm.com/eccedge/fix/dhe/delivery04-mul/sar/CMA/ISA/0dmyw/0/SJ08024.savf"}, {"type": "edge", "url": "https://delivery04.mul.dhe.ibm.com/sar/CMA/ISA/0dmyw/0/SJ08024.savf"}]}, {"description": "Upper Case Coverletter", "descriptor": "metadata/readme.fix", "hash": "8FdiMKzxqyceo2WAVaXsNQBMVouacyV4KsJxMJOnxbk=", "hashAlgorithm": "SHA-256", "size": 9440, "url": "https://esupport.ibm.com/eccedge/fix/dhe/delivery04-bld/sar/CMA/ISA/0dmyw/0/SJ08024.50.txt", "url_type": "edge", "urls": [{"type": "edge", "url": "https://esupport.ibm.com/eccedge/fix/dhe/delivery04-bld/sar/CMA/ISA/0dmyw/0/SJ08024.50.txt"}, {"type": "edge", "url": "https://esupport.ibm.com/eccedge/fix/dhe/delivery04-mul/sar/CMA/ISA/0dmyw/0/SJ08024.50.txt"}, {"type": "edge", "url": "https://delivery04.mul.dhe.ibm.com/sar/CMA/ISA/0dmyw/0/SJ08024.50.txt"}]}], "id": "SJ08024", "name": "SJ08024", "release_date": "2025-12-29T16:44:39.000Z", "status": "available", "type": "interim fix", "upgrades_to_version": "V7R6M0"}]
            
      
      
                              
       download_list
        | The successful downloaded fix list including a dictionary entry for each PTF.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"file_name": "QSJ08213.FILE", "file_path": "/home/gjertsen/ansible/ptf_repo/SJ08213/", "product": "5770JV1", "ptf_id": "SJ08213", "release": "V7R6M0"}]
            
      
        
