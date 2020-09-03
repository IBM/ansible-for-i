Power IBM i collection for Ansible
==============================================

The IBM i collection includes modules. action plugins, sample playbooks to automate tasks on IBM i.

Ansible is a radically simple IT automation system. It handles configuration management, application 
deployment, cloud provisioning, ad-hoc task execution, network automation, and multi-node orchestration. 
Ansible makes complex changes like zero-downtime rolling updates with load balancers easy.

IBM i systems can be managed nodes of Ansible. This project is to enrich IBM i support on Ansible, like 
providing more IBM i modules and examples to manage IBM i nodes.

Getting Started Articles
========================
You may want to check out below articles first if you are new to Ansible for IBM i support.

https://developer.ibm.com/linuxonpower/2020/05/01/ansible-automation-for-ibm-power-systems/

https://ibm.github.io/cloud-i-blog/archivers/2020_0602_automate_your_ibm_i_tasks_with_ansible

:Dependencies on IBM i node:
 - 5733SC1 Base and Option 1
 - 5770DG1
 - python3
 - python3-itoolkit
 - python3-ibm_db


Features
========

The IBM i collection includes `action plugins`_, `modules`_, `sample playbooks`_, and
`ansible-doc`_ to automate tasks on IBM i.

.. _action plugins:
   https://github.com/IBM/ansible-for-i/tree/devel/plugins/action/
.. _modules:
    https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/
.. _sample playbooks:
    https://github.com/IBM/ansible-for-i/tree/devel/examples/playbooks/
.. _ansible-doc:
    https://github.com/IBM/ansible-for-i/tree/devel/docs/


Copyright
=========

© Copyright IBM Corporation 2020

License
=======

Some portions of this collection are licensed under
`GNU General Public License, Version 3.0`_, and other portions of this
collection are licensed under `Apache License, Version 2.0`_.

See individual files for applicable licenses.

.. _GNU General Public License, Version 3.0:
    https://opensource.org/licenses/GPL-3.0

.. _Apache License, Version 2.0:
    https://opensource.org/licenses/Apache-2.0

Author Information
==================

This Ansible collection is maintained by IBM i development team. 

.. toctree::
   :maxdepth: 2
   :caption: Getting Started
   :hidden:

   installation

.. toctree::
   :maxdepth: 3
   :caption: Reference
   :hidden:
  
   plugins
   modules

