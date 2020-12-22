#!/usr/bin/python
# coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: ibmi_powervc_os_server_capture
short_description: Create an image from an existing Compute Instances from OpenStack
version_added: "2.8.0"
author: "Li Jun Zhu (@zhuljbj)"
description:
   - Create an image from an existing compute instance from OpenStack.
     This module returns an Image object.
options:
   server:
     description:
        - Name or ID of the instance
     type: str
     required: true
   wait:
     description:
        - If the module should wait for the instance action to be performed.
     type: bool
     default: 'yes'
   timeout:
     description:
        - The amount of time the module should wait for the instance to perform
          the requested action.
     type: int
     default: 180
   name:
     description:
       - Name of image to be created
     type: str
     required: true
   metadata:
     description:
       - the metadata to create the image
     type: dict
     default: {}
   availability_zone:
     description:
       - Ignored. Present for backwards compatibility
     type: str
requirements:
    - "python >= 2.7"
    - "openstacksdk"
'''

EXAMPLES = r'''
- ibmi_powervc_os_server_capture:
      name: new_image
      auth:
        auth_url: https://identity.example.com
        username: admin
        password: admin
        project_name: admin
      server: vm1
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.openstack import openstack_full_argument_spec, openstack_module_kwargs, openstack_cloud_from_module


def _action_url(server_id):
    return '/servers/{server_id}/action'.format(server_id=server_id)


def main():
    argument_spec = openstack_full_argument_spec(
        server=dict(type='str', required=True),
        wait=dict(type='bool', default=True),
        timeout=dict(type='int', default=180),
        name=dict(tyep='str', required=True),
        metadata=dict(type='dict', default={})
    )

    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, supports_check_mode=False,
                           **module_kwargs)

    sdk, cloud = openstack_cloud_from_module(module)
    name = module.params['name']
    metadata = module.params['metadata']
    wait = module.params['wait']
    timeout = module.params['timeout']

    try:
        server = cloud.get_server(module.params['server'])
        if not server:
            module.fail_json(msg='Could not find server %s' % server)

        action = {'name': name}
        if metadata is not None:
            action['metadata'] = metadata
        body = {'createImage': action}

        response = cloud.compute.post(
            _action_url(server.id),
            json=body)

        module.debug("repsonse is %s" % (response))

        body = None
        try:
            # There might be body, might be not
            body = response.json()
            module.debug("body is %s" % (body))
        except Exception:
            pass
        if body and 'image_id' in body:
            image_id = body['image_id']
        else:
            image_id = response.headers['Location'].rsplit('/', 1)[1]

        image = cloud.get_image(image_id)

        if wait:
            image = cloud.wait_for_image(image, timeout=timeout)

        module.exit_json(
            changed=False, server_id=server.id, image=image)

    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e), extra_data=e.extra_data)


if __name__ == '__main__':
    main()
