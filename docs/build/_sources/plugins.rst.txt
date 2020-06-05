.. ...........................................................................
.. © Copyright IBM Corporation 2020                                          .
.. ...........................................................................

Plugins
=======

Plugins that come with the **Power IBM i collection** augment Ansible's core
functionality. Ansible uses a plugin architecture to enable a rich, flexible
and expandable feature set.

Action
------

* ``ibmi_copy``: A fork of Ansible `copy.py`_ action plugin that is modified to allow copy a SAVF file to remote IBM i nodes.

* ``ibmi_fetch``: A fork of Ansible `fetch.py`_ action plugin that is modified to allow fetch objects from IBM i nodes .

* ``ibmi_reboot``: A fork of Ansible `reboot.py`_ action plugin that is modified to reboot IBM i nodes.

* ``ibmi_script``: A fork of Ansible `script.py`_ action plugin that is modified to allow run CL scripts and SQL scripts on IBM i nodes .

* ``ibmi_synchronize``: A fork of Ansible `synchronize.py`_ action plugin that is modified to allow synchronize SAVF objects.

.. _copy.py:
   https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/action/copy.py
.. _fetch:
   https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/action/fetch.py
.. _reboot.py:
   https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/action/reboot.py
.. _script:
   https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/action/script.py
.. _synchronize.py:
   https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/action/synchronize.py


