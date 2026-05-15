#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Rob Gjertsen <gjertsen@us.ibm.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_download_fix_from_cloud
short_description: Download fix using the cloud API to Electronic Fix Delivery (EFD).
version_added: '3.4.0'
description:
    - The C(ibmi_download_fix_from_cloud) module downloads fixes using a cloud API to Electronic Fix Delivery (EFD).
      This allows fixes to be downloaded to a Linux server for those environments where it is not possible to download
      to an IBM i server, e.g., due to network restrictions. Users should continue to use module ibmi_download_fix
      (based on the SNDPTFORD CL command) for downloading fixes to an IBM i server.
    - Only individual PTFs can be downloaded due to current cloud API limitations.
    - Individual PTFs are only provided in save files due to current cloud API limitations.
    - The downloaded save files and cover letters will have sym links created in the download directory to follow
      naming protocols for these files on the IBM i server in the QGPL library. The PTF file link is "Q<ptf_id>.FILE"
      and the cover letter file link is "Q<pfd_id>.MBR".
    - Future support will include virtual images for PTFS, PTF groups, and cumulative PTF packages.
options:
  ptf_id:
    description:
      - Specify the identifier of the PTF information being ordered.
    type: str
    required: true
  credentials:
    description:
      - Machine credentials used to validate entitlement for the requested fix.
      - Includes fields for 'machine_model', 'machine_type', 'serial_number', and 'country'. This information can be determined
        from the ibmi_facts module output.
    type: dict
    required: True
  operation:
    description:
      - The various operations include
      - Download the fix (includes validating fix entitlement based on the provided credentials).
      - Validate machine entitlement for the fix based on credentials provided. No download occurs.
      - Preview the fix. Useful for viewing the pre/co-requisite fixes. No download occurs.
    choices: ['download', 'validate', 'preview']
    type: str
    default: 'download'
    required: False
  directory:
    description:
      - Directory to download the fix files to. The directory is created if it does not already exist.
        The full or absolute directory path must be specified.
    type: str
    required: True # if the download operation is specified
  clean_directory:
    description:
      - Clean out contents of specified directory prior to download.
    type: bool
    default: False
    required: False
  include_requisites:
    description:
      - Specifies if requisite PTFs should be included with the ordered PTFs.
    type: bool
    default: False
    required: False
  time_out:
    description:
      - The max time that the module waits for the download to complete.
      - The unit can be 's', 'm', 'h', 'd' and 'w'.
      - Future parameter to enforce.
        Currently we only enforce the recommended 2 minute timeout for cloud API handshake and
        do not time out for the PTF image download, but we plan to incorporate an enforced time out
        that factors in the image download time in a future release.
    type: str
    default: '15m'
    required: False
author:
    - Rob Gjertsen (@robgjertsen1)
'''

EXAMPLES = r'''
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
    include_requisites: False
'''

RETURN = r'''
delta:
    description: The module execution delta time.
    returned: always
    type: str
    sample: '0:00:00.307534'
stdout:
    description: The last command standard output.
    returned: always
    type: str
    sample: ''
stderr:
    description: The last command standard error.
    returned: always
    type: str
    sample: ''
cmd:
    description: The last command executed.
    returned: always
    type: str
    sample: ''
rc:
    description: The last command return code. 0 means success.
    returned: always
    type: int
    sample: 0
entitlement_verified:
    description: Returns whether the software entitlement for the fix is verified with the provided machine credentials.
                 Returns true if the machine has authorized access to the software fix.
                 This is only applicable for the validation and download operations where credential checking occurs.
    returned: always (however, the result is not applicable to the preview operation)
    type: bool
    sample: True
msg:
    description: The execution message.
    returned: always.
    type: str
    sample: ''
updates:
    description: Updates recieved from EFD portal after sending the payload.
                 Includes information on the fixes with the preview operation.
                 Includes information on the downloaded files with the the download operation.
                 Provided in JSON format (list of dictionaries).
    returned: always
    type: list
    sample:
        [
          {
            "applies_to_version":"V7R6M0",
            "description":"JDK 80-32 SR8 FP55 IBM Technology for Java",
            "files":[
              {
                "description":"DeploymentDescriptor",
                "descriptor":"metadata/deployment-descriptor.fix",
                "hash":"E4AMkam85CBpdYpmhtZra5h3BEagg7UVtuchaGI+YA8=",
                "hashAlgorithm":"SHA-256",
                "size":4924,
                "url":"https://esupport.ibm.com/eccedge/fix/dhe/delivery04-bld/sar/CMA/ISA/0dmyw/0/SJ08024.dd.xml",
                "url_type":"edge",
                "urls":[
                  {
                    "type":"edge",
                    "url":"https://esupport.ibm.com/eccedge/fix/dhe/delivery04-bld/sar/CMA/ISA/0dmyw/0/SJ08024.dd.xml"
                  },
                  {
                    "type":"edge",
                    "url":"https://esupport.ibm.com/eccedge/fix/dhe/delivery04-mul/sar/CMA/ISA/0dmyw/0/SJ08024.dd.xml"
                  },
                  {
                    "type":"edge",
                    "url":"https://delivery04.mul.dhe.ibm.com/sar/CMA/ISA/0dmyw/0/SJ08024.dd.xml"
                  }
                ]
              },
              {
                "description":"PackageDescriptor",
                "descriptor":"metadata/package-descriptor.fix",
                "hash":"f2ItcEw3a2jlihlfM+wIPwy/667DNPZ6fxZTHhNg/cw=",
                "hashAlgorithm":"SHA-256",
                "size":2209,
                "url":"https://esupport.ibm.com/eccedge/fix/dhe/delivery04-bld/sar/CMA/ISA/0dmyw/0/SJ08024.pd.sdd",
                "url_type":"edge",
                "urls":[
                  {
                    "type":"edge",
                    "url":"https://esupport.ibm.com/eccedge/fix/dhe/delivery04-bld/sar/CMA/ISA/0dmyw/0/SJ08024.pd.sdd"
                  },
                  {
                    "type":"edge",
                    "url":"https://esupport.ibm.com/eccedge/fix/dhe/delivery04-mul/sar/CMA/ISA/0dmyw/0/SJ08024.pd.sdd"
                  },
                  {
                    "type":"edge",
                    "url":"https://delivery04.mul.dhe.ibm.com/sar/CMA/ISA/0dmyw/0/SJ08024.pd.sdd"
                  }
                ]
              },
              {
                "description":"Savefile",
                "descriptor":"data/installable-unit.fix",
                "hash":"tGjPjB+eW0UtF8hA57Epcpd3M4qOn6V/yXiPU1H+Yn4=",
                "hashAlgorithm":"SHA-256",
                "size":149526432,
                "url":"https://esupport.ibm.com/eccedge/fix/dhe/delivery04-bld/sar/CMA/ISA/0dmyw/0/SJ08024.savf",
                "url_type":"edge",
                "urls":[
                  {
                    "type":"edge",
                    "url":"https://esupport.ibm.com/eccedge/fix/dhe/delivery04-bld/sar/CMA/ISA/0dmyw/0/SJ08024.savf"
                  },
                  {
                    "type":"edge",
                    "url":"https://esupport.ibm.com/eccedge/fix/dhe/delivery04-mul/sar/CMA/ISA/0dmyw/0/SJ08024.savf"
                  },
                  {
                    "type":"edge",
                    "url":"https://delivery04.mul.dhe.ibm.com/sar/CMA/ISA/0dmyw/0/SJ08024.savf"
                  }
                ]
              },
              {
                "description":"Upper Case Coverletter",
                "descriptor":"metadata/readme.fix",
                "hash":"8FdiMKzxqyceo2WAVaXsNQBMVouacyV4KsJxMJOnxbk=",
                "hashAlgorithm":"SHA-256",
                "size":9440,
                "url":"https://esupport.ibm.com/eccedge/fix/dhe/delivery04-bld/sar/CMA/ISA/0dmyw/0/SJ08024.50.txt",
                "url_type":"edge",
                "urls":[
                  {
                    "type":"edge",
                    "url":"https://esupport.ibm.com/eccedge/fix/dhe/delivery04-bld/sar/CMA/ISA/0dmyw/0/SJ08024.50.txt"
                  },
                  {
                    "type":"edge",
                    "url":"https://esupport.ibm.com/eccedge/fix/dhe/delivery04-mul/sar/CMA/ISA/0dmyw/0/SJ08024.50.txt"
                  },
                  {
                    "type":"edge",
                    "url":"https://delivery04.mul.dhe.ibm.com/sar/CMA/ISA/0dmyw/0/SJ08024.50.txt"
                  }
                ]
              }
            ],
            "id":"SJ08024",
            "name":"SJ08024",
            "release_date":"2025-12-29T16:44:39.000Z",
            "status":"available",
            "type":"interim fix",
            "upgrades_to_version":"V7R6M0"
          }
        ]
download_list:
    description: The successful downloaded fix list including a dictionary entry for each PTF.
    returned: always
    type: list
    sample: [
      {
        "file_name": "QSJ08213.FILE",
        "file_path": "/home/gjertsen/ansible/ptf_repo/SJ08213/",
        "product": "5770JV1",
        "ptf_id": "SJ08213",
        "release": "V7R6M0"
      }
    ]
'''

# This module uses http POST requests to initiate a transaction with the cloud API for a specified fix from EFD.
# The protocol uses a "software update" event to request the fixes and validate fix entitlement for the specified IBM i server.
# The next set of requests uses a "last contact" event to check for when the fixes are ready (or will provide an error such as if
# lacking entitlement). On success, a list of download URLs will be provided in the updates section for the "last contact" event.
# The final request for a "confirm response" event closes out the transaction and allows clean-up for the cloud API.
# The list of provided URLs are downloaded to the specified destination directory.
# The validate operation follows this protocol, but does not download the fixes; validate should be used when there are other
# IBM i servers to update with the same fix/PTF that was previously downloaded.
# The preview operation follows this protocol, but specifically notes this is for a fix preview with the "software update" event,
# so only information on the fix will be returned with the "last contact" event request (and no validation is performed).

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from builtins import round
from pathlib import Path
import os
import re
import json
import time
import datetime
import urllib.request
import hashlib
import base64
import xml.etree.ElementTree as ET

__ibmi_module_version__ = "3.4.0"

# Defined Globals
event_id = ""
event_time = 0
event_time_ms = 0
size_of_file = 0
softwareupdate_event_id = ""
getresponse_event_id = ""
confirmresponse_event_id = ""
payload = {}
results = dict(
    changed=False,
    stdout='',
    stderr='',
    rc=0,
    cmd='',
    msg='',
    delta='',
    start='',
    end='',
    entitlement_verified=False,
    updates=[],
    download_list=[]
)
server_credentials = {}
curl_cmd = ""
payload_file = ""

####################################################################################
# Helper Functions
####################################################################################


def convert_wait_time_to_seconds(input_wait_time):
    m = re.match(r"^(-?\d+)([smhdw])?$", input_wait_time.lower())
    seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    if m:
        wait_time = int(m.group(1)) * seconds_per_unit.get(m.group(2), 1)
    else:
        wait_time = 0
    return wait_time


def wait_for_certain_time(input_wait_time):
    wait_time = convert_wait_time_to_seconds(input_wait_time)
    time.sleep(wait_time)


def check_directory(module):
    '''
    Utility function to check if the provided directory exists and create directory if necessary.
    If "clean_directory" is set, then any files and symlinks in the provided directory are removed.

    arguments:
        module(dict) - The Ansible module.
    '''

    loc = module.params['directory']
    clean_directory = module.params['clean_directory']

    os.makedirs(loc, exist_ok=True)

    # Delete all files and symlinks in the provided directory if directory cleanout specified
    if clean_directory:
        for entry in os.listdir(loc):
            entry_path = os.path.join(loc, entry)
            # Check if the entry is a symlink
            if os.path.islink(entry_path):
                os.unlink(entry_path)
            # Check if the entry is a file (and not a directory)
            elif os.path.isfile(entry_path):
                os.remove(entry_path)


def filter_credentials(credentials):
    '''
    Utility function to filter whitespace out of provided credentials to keep in
    global server_credentials.

    arguments:
        credentials (dict) - The credentials.
    '''

    global server_credentials

    # Remove whitespace from credentials
    server_credentials = {}
    server_credentials['machine_type'] = credentials['machine_type'].strip()
    server_credentials['machine_model'] = credentials['machine_model'].strip()
    server_credentials['serial_number'] = credentials['serial_number'].strip()
    server_credentials['country'] = credentials['country'].strip()


def check_space(module, required_space):
    '''
    Utility function to check if the provided directory has required space or not.

    arguments:
        module (dict) - The Ansible module.
        required_space (int) - Space required in the provided directory.

    returns:
        True - If space is enough.
        False - If space is not enough.
    '''

    cmd = "df -m "
    cmd += module.params['directory']

    rc, stdout, stderr = module.run_command(cmd)

    results['cmd'] = cmd
    results['stdout'] = stdout
    results['stderr'] = stderr
    results['rc'] = rc

    if rc != 0:
        results['msg'] = "The following command failed: " + cmd
        module.fail_json(**results)

    # Assumes Linux format for "df -m" looks like
    #   Filesystem                                            1M-blocks  Used Available Use% Mounted on
    #   /dev/mapper/luks-ddcfc87e-0baf-4ee0-8f54-64e9bbf0b485    975267 55328    907818   6% /home
    values = stdout.split("\n")[1]
    details = values.split()
    space = float(details[3])
    required_space = float(required_space)

    if space < required_space:
        results['msg'] = "Not enough space present in the provided download directory. " + str(round(required_space - space, 1)) + "MB more needed."
        module.fail_json(**results)


def check_requirements(module):
    '''
    Utility Function to check if the requirements are already satisfied or not (curl present)

    arguments:
        module (dict) : The Ansible module.

    returns:
        Nothing
    '''

    cmd = "ls /usr/bin/"

    check_curl = cmd + 'curl'

    rc, stdout, stderr = module.run_command(check_curl)

    results['cmd'] = cmd
    results['stdout'] = stdout
    results['stderr'] = stderr
    results['rc'] = rc

    if rc != 0:
        results['msg'] = "Curl is not present in the system, please install and rerun."
        module.fail_json(**results)

    results['msg'] += " Curl is present on the system, requirement satisfied!"


def check_for_updates(stdout):
    '''
    Utility function to check if "updates" are available in the response field from the last contact event request.
    This indicates that the fixes are now available for download.

    arguments:
        stdout (str) : Contains standard output of the curl command

    returns:
        True: If updates are available
        False: If updates are not available
    '''

    res = json.loads(stdout)

    try:
        if res["response_state"]["transactions"][softwareupdate_event_id]["response_object"]["updates"]:
            return True
        return False
    except KeyError:
        return False


def check_response(stdout):
    '''
    Utility function to check if the connection was successfully made.

    arguments:
        stdout (str) : Contains standard output of the curl command

    returns:
        True : If the response was 200 (OK)
        False : In all the other cases (Except 200 OK response)
    '''

    res = json.loads(stdout)

    try:
        if res["transaction"]["rc"] == 200:
            return True
        return False
    except KeyError:
        return False


def check_for_authentication(module, stdout):
    '''
    Utility function to check that there was not any authentication related faliure.

    arguments:
        stdout (str) : Contains standard output of the command

    returns:
        True: If no authentication faliure was faced.
        False: If there was any type of authentication faliure.
    '''

    res = json.loads(stdout)

    try:
        res = res["response_state"]["transactions"][softwareupdate_event_id]["response_object"]["updates"][0]["error"]
        results['msg'] = "Following error was encountered: " + res
        return False
    except KeyError:
        if module.params['operation'] != "preview":
            results['entitlement_verified'] = True
        return True


def dictionary_to_json(dict_val, payload_type):
    '''
    Utility Function to convert the user provided data from dictionary
    format to JSON format, which will fbe used to send POST requests.
    Generates JSON payload file that will be used for the POST request.

    arguments:
        module (dict): the Ansible module.

    returns:
        json_object (JSON) : JSON object containing all the attributes in JSON format.
    '''

    with open(payload_file, "w", encoding="utf-8") as out_file:
        json.dump(dict_val, out_file, indent=4)


def remove_json_file(module):
    '''
    Helper function to remove the payload file from the system. The payload is being sent as a file,
    this function wil be removing that file.

    arguments:
        module (dict) : The Ansible module.

    returns:
        Nothing
    '''

    cmd = "rm " + payload_file

    rc, stdout, stderr = module.run_command(cmd)

    results['stdout'] = stdout
    results['stderr'] = stderr

    if rc != 0:
        results['rc'] = rc
        results['msg'] += " The temporary payload file " + payload_file + " could not be removed."
        module.fail_json(**results)

    results['msg'] += " The temporary payload file " + payload_file + " was deleted."


def wait_for_response(module):
    '''
    Utility function to keep sending the last contact request until the required response is received including
    download fix information.

    arguments:
        module (dict) : The Ansible module.
        cmd (str) : CURL command to send the payload.

    returns:
        Nothing
    '''

    # Cloud API suggests waiting up to 2 minutes for a response to last contact request indicating
    # the fixes are available ("updates" response section provided)
    counter = 0
    while counter <= 11:
        time.sleep(10)
        rc, stdout, stderr = module.run_command(curl_cmd)
        if check_for_updates(stdout):
            break
        counter += 1

    results['cmd'] = curl_cmd
    results['rc'] = rc
    results['stderr'] = stderr
    results['stdout'] = stdout

    if counter > 11 and not check_for_updates(stdout):
        results['msg'] += " Request timed out. The request for fixes was not satisifed within 2 minutes."
        module.fail_json(**results)
    else:
        if not check_for_authentication(module, stdout):
            module.fail_json(**results)
        results['msg'] += " Response received."


def extract_number_after_char(text, char):
    """
    Returns number string after a specified character (e.g., -)

    Arguments:
        text (str): The text string.
        char (char): The character the precedes a number string (e.g., =).

    Returns:
        str: The number string. None on failure.
    """
    # Pattern explanation:
    # (?<={char}) looks for the character 'char' (positive lookbehind)
    # \\s* matches zero or more whitespace characters
    # (\\d+\\.?\\d*) captures the number (one or more digits, optional dot, optional more digits)
    pattern = rf"(?<={char})\s*(\d+\.?\d*)"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None


def sha_checksum(filename, sha_num, block_size=65536):
    """
    Calculates the checksum of a file for various SHA hash algorithms (e.g., SHA-256).

    Arguments:
        filename (str): The path to the file.
        sha_num (int): SHA algorithm number, e.g., 256 for SHA-256.
        block_size (int): The size of chunks to read the file in (default: 65536 bytes).

    Returns:
        str: The hexadecimal representation of the SHA checksum.
    """
    sha_method = "sha" + str(sha_num)
    sha_hash = getattr(hashlib, sha_method)()
#    sha256_hash = hashlib.sha256()
    with open(filename, 'rb') as f:
        # Read the file in chunks and update the hash object
        for block in iter(lambda: f.read(block_size), b''):
            sha_hash.update(block)
    return sha_hash.hexdigest()


def get_URLs(module):
    '''
    Function to retreive the download URLs from the JSON response.
    Send post(s) with last contact event until download URLs are provided by the cloud API.

    arguments:
        module (dict) - The Ansible module

    returns:
        URLs (list of str) - URLs from where the fix can be downloaded.
    '''

    global size_of_file
    size_of_file = 0

    # Payload for last contact event request
    generate_payload(module, "download")

    wait_for_response(module)

    res = json.loads(results['stdout'])
    results["updates"] = res["response_state"]["transactions"][softwareupdate_event_id]["response_object"]["updates"]
    fields = res["response_state"]["transactions"][softwareupdate_event_id]["response_object"]["updates"]

    URLs = []

    for fix_group in fields:
        for keys in fix_group["files"]:
            URLs.append(keys["url"])
            size_of_file += keys['size']

    if URLs:
        return URLs
    else:
        results['msg'] = "Could not retrieve the URLs with last contact event request."
        module.fail_json(**results)


def generate_event_details():
    '''
    Utility function to generate get event_time and event_time_ms

    arguments: None

    returns:
        Nothing
    '''

    global event_time
    global event_time_ms

    event_time_ms = round(time.time() * 1000)
    event_time = str(datetime.datetime.now()).split('.', maxsplit=1)[0]


def generate_event_id(asset, asset_id):
    '''
    Utility function to generate the event id.

    arguments:
        module (dict) : The Ansible module.
        asset (str) : Asset information (type and model)
        asset_id (str) : Asset ID (serial number)

    returns:
        event_id (str) - Contains event_id that will be sent in the JSON payload.
    '''

    global event_id

    event_id = "IBM_IBMi_Ansible"

    event_id += "_" + asset
    event_id += "_" + asset_id
    event_id += "_" + str(event_time_ms)

    # event_id will look like the following: IBM_IBMi_Ansible_XXXX-XXX_XX-XXXXX_1687344006365
    return event_id


def generate_event_header(module, payload_type):
    '''
    Utility funtion for generating header of the event.

    arguments:
        module (dict) - The Ansible module
        payload_type (str) - Signifies the type of event (software_update, geturl, download or confirm_response)

    returns:
        event_header (dict) - Dictionary containing all the required details that need to go inside the event header.
    '''

    global softwareupdate_event_id
    global getresponse_event_id
    global confirmresponse_event_id

    event_header = {}
    if payload_type == "post" or payload_type == "downloadpost":
        event_header["event_type"] = "software_update"

    elif payload_type == "geturl" or payload_type == "download":
        event_header["event_type"] = "last_contact"

    else:
        # payload_type == "confirm"
        if not (payload_type == "confirm"):
            results['msg'] = "payload_type confirm expected and instead is " + payload_type
            module.fail_json(**results)
        event_header["event_type"] = "confirm_response"

    event_header["event_id"] = event_header["event_type"] + "_" + event_id

    if payload_type == "post" or payload_type == "downloadpost":
        softwareupdate_event_id = event_header["event_id"]
    elif payload_type == "geturl" or payload_type == "download":
        getresponse_event_id = event_header["event_id"]
    else:
        # payload_type == "confirm"
        if not (payload_type == "confirm"):
            results['msg'] = "payload_type confirm expected and instead is " + payload_type
            module.fail_json(**results)
        confirmresponse_event_id = event_header["event_id"]

    event_header["event_time"] = event_time
    event_header["event_time_ms"] = event_time_ms

    return event_header


def generate_post_body(module):
    '''
    Utility function that generates the body for the event part of the payload for POST method (preview specific fix).

    arguments:
       module (dict) - The Ansible module

    returns:
        event_body (dict) - Dictionary containing information which will go inside the body of the
                            payload for POST method.
    '''

    credentials = {}
    mtsn_info = {}
    ptf_id = module.params['ptf_id']

    event_body = {
        "action": "IBM i fix entitled by MTSN",
        "operation": "order_software",
        "request_type": "preview_specific_fix",
        "description": "Preview fix",
        "component": "system",
        "efd_product": "ibm/IBM i",
        "expand_groups": True,
    }

    include_requisites = module.params['include_requisites']
    if include_requisites:
        event_body["include_requisites"] = True

    if isinstance(ptf_id, list):
        event_body["update_ids"] = ptf_id
    else:
        event_body["update_ids"] = [ptf_id]

    mtsn_info["machine_type"] = server_credentials["machine_type"]
    mtsn_info["serial_number"] = server_credentials["serial_number"]
    mtsn_info["country"] = server_credentials["country"]

    credentials["mtsn"] = [mtsn_info]

    event_body["credentials"] = credentials

    return event_body


def generate_geturl_body():
    '''
    Utility function that generates the body for the event part of the payload for getting the fixes (last contact event).

    arguments: None

    returns:
        event_body (dict) - Dictionary containing information which will go inside the body of
                            the payload for getting the fixes.
    '''

    event_body = {}

    event_body["description"] = "Check on progress of software update with last contact event"
    event_body["enable_response_detail"] = True

    enable_response_detail_filter = []
    enable_response_detail_filter.append(softwareupdate_event_id)
    event_body["enable_response_detail_filter"] = enable_response_detail_filter

    event_body["component"] = "system"

    return event_body


def generate_confirm_body():
    '''
    Utility function that generates the body for the event part of the payload for confirming the response.

    arguments: None

    returns:
        event_body (dict) - Dictionary containing information which will go inside the body of the payload
                            for confirming the response.
    '''

    event_body = {}
    event_body["description"] = "Confirm response from earlier software update"
    event_body["event_transaction_id"] = softwareupdate_event_id
    event_body["event_type"] = "software_update"
    event_body["component"] = "system"

    return event_body


def generate_downloadpost_body(module):
    '''
    Utility function that generates the body for the event part of the payload for getting the URLs.

    arguments:
        module (dict) - The Ansible module

    returns:
        event_body (dict) - Dictionary containing information which will go inside the body of the payload
                            for getting the URLs.
    '''

    credentials = {}
    mtsn_info = {}
    ptf_id = module.params['ptf_id']

    event_body = {
        "action": "IBM i fix entitled by MTSN",
        "operation": "order_software",
        "request_type": "specific_fix",
        "description": "Single fix entitled by MTSN",
        "component": "system",
        "efd_product": "ibm/IBM i",
        "url_list": True,
        "expand_groups": True,
    }

    include_requisites = module.params['include_requisites']
    if include_requisites:
        event_body["include_requisites"] = True

    if isinstance(ptf_id, list):
        event_body["update_ids"] = ptf_id
    else:
        event_body["update_ids"] = [ptf_id]

    mtsn_info["machine_type"] = server_credentials["machine_type"]
    mtsn_info["serial_number"] = server_credentials["serial_number"]
    mtsn_info["country"] = server_credentials["country"]
    credentials["mtsn"] = [mtsn_info]

    event_body["credentials"] = credentials

    return event_body


def generate_download_body():
    '''
    Utility function that generates the body for the event part of the payload for getting the URLs for a particular fix (last contact event posted)

    arguments: None

    returns:
        event_body (dict) - Dictionary containing information which will go inside the body of
                            the payload for getting the URLs for fix.
    '''

    event_body = {}

    event_body["description"] = "Check on progress of software update with last contact event"
    event_body["enable_response_detail"] = True

    enable_response_detail_filter = []
    enable_response_detail_filter.append(softwareupdate_event_id)
    event_body["enable_response_detail_filter"] = enable_response_detail_filter

    event_body["component"] = "system"

    return event_body


def generate_event(module, payload_type):
    '''
    Utility function to generate the event for the JSON object that will be sent in the JSON payload.

    arguments:
        payload_type (str) - Contains the type of request for which the event needs to be generated

    returns:
        event (list) - Dictionary inside a list containing required information about the event.

    This part is being generated here :

    "events":[
    {
        "header":{
            "event_type":"software_update",
            "event_id": "software_update_IBM_IBMi_Ansible_Test_XXXX-XXX_XX-XXXXX-1768593293784",
            "event_time": "2026-01-16 13:54:53",
            "event_time_ms": 1768593293784
        },
        "body":{
            "action": "Fix entitled by MTSN",
            "operation": "order_software",
            "request_type": "specific_fix",
            "description": "Single fix with deps entitled by MTSN",
            "component": "system",
            "efd_product": "ibm/IBM i",
            "url_list": true,
            "include_requisites": true,
            "expand_groups": true,
            "update_ids": [
                "SJ08024"
            ],
            "credentials": {
                "mtsn": [
                {
                  "machine_type": "XXXX",
                  "serial_number": "XXXXXXX",
                  "country": "US"
                }
              ]
            }
        }
    }
  ]
    '''

    events = {}

    events["header"] = generate_event_header(module, payload_type)

    if payload_type == "post":
        events["body"] = generate_post_body(module)

    elif payload_type == "geturl":
        events["body"] = generate_geturl_body()

    elif payload_type == "download":
        events["body"] = generate_download_body()

    elif payload_type == "downloadpost":
        events["body"] = generate_downloadpost_body(module)

    else:
        # payload_type == "confirm"
        if not (payload_type == "confirm"):
            results['msg'] = "payload_type confirm expected and instead is " + payload_type
            module.fail_json(**results)
        events["body"] = generate_confirm_body()

    events_list = []
    events_list.append(events)

    return events_list


def generate_payload(module, payload_type):
    '''
    Function to generate the payload in json format and write it to the payload file.

    arguments:
        module - The Ansible module
        payload_type - Type of payload that needs to be created
    returns:
        payload_json (JSON) - A JSON object containing payload.

    The payload will look like this:

    {
        "agent":"IBMi_Ansible",
        "api_key":"IBM_IBMi_Ansible_call_home_connect_28aG*712b_kba9wIUks*_9Jlsio#142",
        "private_key":"IBM_IBMi_Ansible_J8*1@#_kIj&^Hyh@1",
        "target_space":"prod",
        "asset":"XXXX-YYY",
        "asset_id":"XX-XXXXX",
        "asset_type":"Power",
        "asset_vendor":"IBM",
        "asset_virtual_id":"0000000000000000",
        "country_code":"US",
        "event_id": "IBM_IBMi_Ansible_XXXX-XXX_XX-XXXXX_1768596159965",
        "event_time": "2026-01-16 15:00:00",
        "event_time_ms": 1768596159965,
        "type":"eccnext_apisv1s",
        "version":"1.0.0.1",
        "software_level":{
            "name":"IBM_IBMi_Version",
            "vrmf":"7.4"
        },
        "events":[
        {
            "header":{
                "event_type":"software_update",
                "event_id": "software_update_IBM_IBMi_Ansible_Test_XXXX-XXX_XX-XXXXX-1768593293784",
                "event_time": "2026-01-16 13:54:53",
                "event_time_ms": 1768593293784
            },
            "body":{
                "action": "Fix entitled by MTSN",
                "operation": "order_software",
                "request_type": "specific_fix",
                "description": "Single fix with deps entitled by MTSN",
                "component": "system",
                "efd_product": "ibm/IBM i",
                "url_list": true,
                "include_requisites": true,
                "expand_groups": true,
                "update_ids": [
                    "SJ08024"
                ],
                "credentials": {
                    "mtsn": [
                    {
                        "machine_type": "XXXX",
                        "serial_number": "XXXXXXX",
                        "country": "US"
                    }
                  ]
                }
            }
        }
    ]
}

    '''

    credentials = server_credentials
    software_level_info = {}

    payload["agent"] = "IBMi_Ansible"
    payload["api_key"] = "IBM_IBMi_Ansible_call_home_connect_28aG*712b_kba9wIUks*_9Jlsio#142"
    payload["private_key"] = "IBM_IBMi_Ansible_J8*1@#_kIj&^Hyh@1"
    payload["target_space"] = "prod"
    payload["asset"] = credentials['machine_type'] + "-" + credentials['machine_model']
    payload["asset_id"] = credentials['serial_number'][:2] + "-" + credentials['serial_number'][2:]
    payload["asset_virtual_id"] = "0000000000000000"
    payload["asset_type"] = "Power"
    payload["asset_vendor"] = "IBM"
    payload["country_code"] = credentials['country']
    payload["type"] = "eccnext_apisv1s"
    payload["version"] = "1.0.0.1"
    payload["analytics_event_source_type"] = "asset_event"
    payload["analytics_type"] = payload["asset"]
    payload["analytics_instance"] = payload["asset_id"]
    payload["analytics_virtual_id"] = "0000000000000000"
    payload["analytics_group"] = "IBM"
    payload["analytics_category"] = "Power"

    generate_event_details()
    payload["event_time"] = event_time
    payload["event_time_ms"] = event_time_ms

    software_level_info["name"] = "IBM_IBMi_Version"
    # Provide an IBM i release in 'software_level' base field to satisfy protocol
    release = 'V7R6M0'
    # Short release form such as "7.6" for "V7R6M0"
    software_level_info["vrmf"] = release[1] + "." + release[3]
    payload["software_level"] = software_level_info

    # Value of event_id = will be something like this: IBM_IBMi_Ansible_XXXX-XXX_XXXXXXXXXXXX_1687344006365
    payload["event_id"] = generate_event_id(payload["asset"], payload["asset_id"])

    events = generate_event(module, payload_type)
    payload["events"] = events

    dictionary_to_json(payload, payload_type)


def read_xml_file(filename):
    '''
    Read and parse an XML file into Element Tree (ET) and return the root element of ET.
    '''

    tree = ET.parse(filename)
    root = tree.getroot()

    return root


def extract_xml_file_info(module, filename):
    '''
    Extract the product ID, release information, PTF ID for the PTF from the XML file, <PTF ID>.dd.xml.

    Returns dict with entries {"ptf_id": <ptf_id>, "product_id": <product_id>, "release:" <release>}.
    '''

    info = {}

    root = read_xml_file(filename)
    if not (root is not None):
        results['msg'] = "Expected ET root with file: " + filename
        module.fail_json(**results)

    # Define utilized namespaces in PTF XML file
    ns_sdd_dd = 'http://docs.oasis-open.org/sdd/ns/deploymentDescriptor'
    ns_sdd_common = 'http://docs.oasis-open.org/sdd/ns/common'

    # Find element for "sdd-dd:InstallableUnit"
    IU_element = root.find(f'{{{ns_sdd_dd}}}InstallableUnit')
    if not (IU_element is not None):
        results['msg'] = "Expected defined InstallableUnit element"
        module.fail_json(**results)

    # Find element for "sdd-common:Identity"
    Identity_element = IU_element.find(f'{{{ns_sdd_dd}}}Identity')
    if not (Identity_element is not None):
        results['msg'] = "Expected defined Identity element"
        module.fail_json(**results)

    # Product ID is attribute of Identity element
    product_id = Identity_element.attrib.get('softwareID')
    if not (product_id is not None):
        results['msg'] = "Expected defined softwareID attribute for Identity element"
        module.fail_json(**results)

    # Grab release (Version) and PTF ID (Name) from children of Identity element
    Version_element = Identity_element.find(f'{{{ns_sdd_common}}}Version')
    release = Version_element.text

    ptf_id_element = Identity_element.find(f'{{{ns_sdd_common}}}Name')
    ptf_id = (ptf_id_element.text).split()[0]

    # results['msg'] += " Debug extract_xml_file_info. Product ID: " + product_id + " release: " + release + " ptf id: " + ptf_id
    info = {"ptf_id": ptf_id, "product": product_id, "release": release}

    return info


def download_fix(module, URLs):
    '''
    Function to download the fix(es) from the provided URL link(s).

    arguments:
        module (dict) - The Ansible module
        URLs (str) - fix URLs

    returns:
        Nothing
    '''

    global size_of_file

    size_of_file /= 1000000
    check_space(module, size_of_file)

    # Retreive expected file size and encoded checksum with hash type corresponding to URLs from response update
    fields = results["updates"]
    file_sizes = []
    file_enc_checksums = []
    hash_types = []
    download_list = []

    for fix_group in fields:
        for keys in fix_group["files"]:
            file_sizes.append(keys["size"])
            file_enc_checksums.append(keys['hash'])
            hash_types.append(keys['hashAlgorithm'])

    # Download each file
    for index, link in enumerate(URLs):
        filename = link.split('/')[-1]
        directory = module.params['directory']

        if directory[-1] != '/':
            directory += '/'
        location = directory

        location += filename

        # urlretrieve will be used to download the file from the retrieved URL.
        # TODO: error handling, timeout?
        urllib.request.urlretrieve(link, location)

        # Verify file sizes match (once cloud API bug is fixed)
        size = os.path.getsize(location)
        # results['msg'] += " Index " + str(index) + " File: " + location + " Expected size: " + str(file_sizes[index]) + " Size: " + str(size)

        # Assert "SHA-" hash algorithm is being used as expected, so we fall over if something unexpected is added.
        if not (hash_types[index][0:4] == "SHA-"):
            results['msg'] = "Expected checksum hash algorithm SHA-X, but instead got: " + hash_types[index]
            module.fail_json(**results)

        # Verify downloaded file checksum matches what the cloud API provided.
        sha_num = extract_number_after_char(hash_types[index], '-')
        checksum = sha_checksum(location, sha_num, 65536)
        base64_str = file_enc_checksums[index]
        decoded_bytes = base64.b64decode(base64_str)
        hex_string = decoded_bytes.hex()
        # results['msg'] += " File: " + location + " Provided checksum: " + hex_string + " checksum: " + checksum + " hash alg: " + hash_types[index]
        if checksum != hex_string:
            results['msg'] = " Downloaded file checksum mismatch. File: " + filename + " Expect checksum: " + hex_string + ", File checksum: " + checksum
            module.fail_json(**results)

        extension = Path(filename).suffix
        # Create symlink for expected cover letter name to transfer to IBM i system (<ptf_id>.50.txt -> Q<ptf_id>.MBR). Ignore if it already exists.
        if extension == ".txt":
            coverletter_name = "Q" + Path(Path(filename).stem).stem + ".MBR"
            try:
                os.symlink(directory + filename, directory + coverletter_name)
            except FileExistsError:
                pass

        # Extract PTF information for returned download list from the XML information file
        if extension == ".xml":
            xml_info = extract_xml_file_info(module, location)
            ptf_id = Path(Path(filename).stem).stem
            # results['msg'] += " extract_xml_file_info file ptf_id: " + ptf_id + " from filename ptf_id: " + xml_info["ptf_id"] + "."
            # Generate new entry for download_list
            savefile_name = "Q" + ptf_id + ".FILE"
            results['msg'] += " Adding PTF to download_list: " + ptf_id + "."
            download_list.append(xml_info | {"file_name" : savefile_name, "file_path" : directory})

        # Create symlink for expected save file name to transfer to IBM i system (<ptf_id>.savf -> Q<ptf_id>.FILE). Ignore if it already exists.
        if extension == ".savf":
            savefile_name = "Q" + Path(filename).stem + ".FILE"
            try:
                os.symlink(directory + filename, directory + savefile_name)
            except FileExistsError:
                pass

    results['download_list'] = download_list
    results['msg'] += " The fix has been downloaded and checksums verified."
    results['changed'] = True


####################################################################################
# Action Handler Functions
####################################################################################


def send_post(module):
    '''
    To send the POST software update event request to EFD portal including all the necessary information for previewing a fix.

    arguments:
        module (dict): The Ansible module.

    returns:
        Nothing
    '''

    generate_payload(module, "post")

    rc, stdout, stderr = module.run_command(curl_cmd)

    results['cmd'] = curl_cmd
    results['rc'] = rc
    results['stderr'] = stderr
    results['stdout'] = stdout

    if not check_response(stdout):
        results['msg'] = "POST software update event request unsuccessful."
        module.fail_json(**results)
    results['msg'] += "POST request successful."


def send_downloadpost(module):
    '''
    To send the POST request to EFD portal including all the necessary information required for getting the URLs and further downloading the fixes.
    Sends post for software update event to request specified fix to download with the cloud API.

    arguments:
        module (dict) : The Ansible module.

    returns:
        Nothing
    '''

    generate_payload(module, "downloadpost")

    rc, stdout, stderr = module.run_command(curl_cmd)

    results['cmd'] = curl_cmd
    results['rc'] = rc
    results['stderr'] = stderr
    results['stdout'] = stdout

    if not check_response(stdout):
        results['msg'] = "POST request for software update event is unsuccessful."
        module.fail_json(**results)

    results['msg'] += " POST request for software update event successful."


def get_fixes(module):
    '''
    To send the POST last contact event request(s) to EFD portal including all the necessary information (preview fix request)
    until response with fix URLs provided.

    arguments:
        module (dict): The Ansible module.

    returns:
        Nothing
    '''

    generate_payload(module, "geturl")

    wait_for_response(module)

    res = json.loads(results['stdout'])

    results["updates"] = res["response_state"]["transactions"][str(softwareupdate_event_id)]["response_object"]["updates"]
    results['msg'] += " Successfully retrieved information about fixes."


def confirm_json(module):
    '''
    To send the POST request to EFD portal including all the necessary information (post confirm response event
    to close out transaction initiated by software update event).

    arguments:
        module (dict): The Ansible module.

    returns:
        Nothing
    '''

    generate_payload(module, "confirm")

    rc, stdout, stderr = module.run_command(curl_cmd)

    results['cmd'] = curl_cmd
    results['rc'] = rc
    results['stderr'] = stderr
    results['stdout'] = stdout

    if not check_response(stdout):
        results['msg'] = "Could not send confirm response request."
        module.fail_json(**results)

    results['msg'] += " Response confirmed."


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ptf_id=dict(type='str', required=True),
            credentials=dict(type='dict', required=True),
            operation=dict(type='str', default='download', choices=['download', 'validate', 'preview']),
            directory=dict(type='str', required=True),
            clean_directory=dict(type='bool', default=False),
            include_requisites=dict(type='bool', default=False),
            time_out=dict(type='str', default='15m')
            # wait=dict(type='bool', default=True),
        ),
        supports_check_mode=True,
    )
    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    global curl_cmd
    global payload_file

    # Validate parameters
    if not module.params['ptf_id']:
        results['msg'] = "PTF id was not provided."
        module.fail_json(**results)
    if not module.params['credentials']:
        results['msg'] = "Credentials were not provided."
    credentials = module.params['credentials']
    required_credential_keys = ["machine_model", "machine_type", "serial_number", "country"]
    all_credential_keys = all(key in credentials for key in required_credential_keys)
    if not all_credential_keys:
        results['msg'] = "Credentials missing some required fields from machine_model, machine_type, serial_number, and country."
        module.fail_json(**results)
    operation = module.params['operation']
    if operation == 'download' and not module.params['directory']:
        results['msg'] = "Download directory was not specified."
        module.fail_json(**results)

    check_requirements(module)
    filter_credentials(credentials)

    # The final command will be something like this: /usr/bin/curl --request POST --header 'accept: application/json' --header
    # 'content-type: application/json' -d @payload.json
    # Currently include PID in payload file name to allow for concurrent download operations. Format is payloadfile_<pid>.json
    pid = os.getpid()
    payload_file = "payloadfile" + "_" + str(pid) + ".json"
    curl_cmd = "/usr/bin/curl --request POST --header 'accept: application/json' --header 'content-type: application/json' "
    curl_cmd += "-d @" + payload_file + " --url 'https://esupport.ibm.com/connect/api/v1' -S"

    startd = datetime.datetime.now()

    if operation == "preview":
        send_post(module)
        get_fixes(module)
        confirm_json(module)
    else:
        # download or validate operation
        if not (operation == "download" or operation == "validate"):
            results['msg'] = "Unexpected operation specified."
            module.fail_json(**results)
        if operation == "download":
            check_directory(module)
        send_downloadpost(module)
        URLs = get_URLs(module)
        # validate operation skips downloading fixes
        if operation == "download":
            download_fix(module, URLs)
        confirm_json(module)

    # Clean up payload file
    remove_json_file(module)

    endd = datetime.datetime.now()
    delta = endd - startd

    results.update({'delta': str(delta)})
    results.update({'start': str(startd)})
    results.update({'end': str(endd)})

    module.exit_json(**results)


if __name__ == '__main__':
    main()
