#!/usr/bin/python
# coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = r'''
---
module: ibmi_powervc_add_license_key
short_description: add a license key to an existing IBM i Instances from PowerVC
version_added: "2.0"
author: "Li Jun Zhu (@zhuljbj)"
description:
   - Create an image from an existing compute instance from PowerVC.
     This module returns an Image object.
options:
   server:
     description:
        - Name or ID of the instance
     type: str
     required: true
   license_key:
     description:
       - The license key to be injected. Its length has to be 101.
     type: str
     required: true
   availability_zone:
     description:
       - Ignored. Present for backwards compatibility
     type: str
requirements:
    - "python >= 2.7"
    - "openstacksdk"
'''

EXAMPLES = r'''
- ibmi_powervc_add_license_key:
      license_key: "1191028013241RCHASC015770SS1V7R4M05050 XXXXXXX9990001001221224        XXXXXXXXXXXXXXXXXX1191028013241"
      auth:
        auth_url: https://identity.example.com
        username: admin
        password: admin
        project_name: admin
      server: vm1
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.openstack import openstack_full_argument_spec, openstack_module_kwargs, openstack_cloud_from_module
try:
    import simplejson
    JSONDecodeError = simplejson.scanner.JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError


def _action_url(server_id):
    return '/servers/{server_id}/action'.format(server_id=server_id)


def _json_response(sdk, response, result_key=None, error_message=None):
    """Temporary method to use to bridge from ShadeAdapter to SDK calls."""
    sdk.exceptions.raise_from_response(response, error_message=error_message)

    if not response.content:
        # This doesn't have any content
        return response

    # Some REST calls do not return json content. Don't decode it.
    if 'application/json' not in response.headers.get('Content-Type'):
        return response

    try:
        result_json = response.json()
    except JSONDecodeError:
        return response
    return result_json


def main():
    argument_spec = openstack_full_argument_spec(
        server=dict(type='str', required=True),
        license_key=dict(tyep='str', required=True),
    )

    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, supports_check_mode=False,
                           **module_kwargs)

    sdk, cloud = openstack_cloud_from_module(module)
    license_key = module.params['license_key']

    try:
        server = cloud.get_server(module.params['server'])
        if not server:
            module.fail_json(msg='Could not find server %s' % server)

        if len(license_key) != 101:
            module.fail_json(msg='An invalid license key is provided %s. Its length is not 101.' % license_key)

        action = {}
        action['licenseKey'] = license_key
        body = {'IBMiServerAddLicense': action}

        data = _json_response(sdk, cloud.compute.post(
            _action_url(server.id),
            json=body))

        module.exit_json(
            changed=False, server_id=server.id, license_key=license_key, data=data)

    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e), extra_data=e.extra_data)


if __name__ == '__main__':
    main()
