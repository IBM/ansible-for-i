#!/usr/bin/env bash

set -eux

export ANSIBLE_ROLES_PATH=../

ansible-playbook -i ../../inventory -v runme.yml "$@"
