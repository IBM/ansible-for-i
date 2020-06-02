..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_uninstall_product.py


ibmi_uninstall_product -- delete the objects that make up the licensed program(product)
=======================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

the ``ibmi_uninstall_product`` module delete the objects that make up the product on the target ibmi node.






Parameters
----------

  release (optional, str, *ONLY)
    Specifies which version, release, and modification level of the licensed program is deleted


  product (True, str, None)
    Specifies the seven-character identifier of the licensed program that is deleted


  option (optional, str, *ALL)
    Specifies which of the parts of the licensed program specified on the Product prompt (LICPGM parameter) are deleted


  language (optional, str, *ALL)
    Specifies which national language version (NLV) objects are deleted for the licensed program specified on the LICPGM parameter

    It's the IBM-supplied language feature codes, like German is 2924, English is 2924







See Also
--------

.. seealso::

   :ref:`ibmi_install_product_from_savf, ibmi_save_product_to_savf_module`
      The official documentation on the **ibmi_install_product_from_savf, ibmi_save_product_to_savf** module.


Examples
--------

.. code-block:: yaml+jinja

    
    - name: Deleting all Licensed Program Objects
      ibmi_uninstall_product:
        product: 5770QU1

    - name: Deleting only the German (NLV 2929) objects for all options of the licensed program 5770QU1
      ibmi_uninstall_product:
        product: 5770QU1
        language: 2929



Return Values
-------------

  stderr_lines (always, list, ['Product 5733D10 option *ALL release *ONLY language *ALL not installed'])
    The standard error split in lines


  stdout_lines (always, list, ['Product 5733D10 option 11 release *ONLY language *ALL deleted.'])
    The standard output split in lines


  stdout (always, str, Product 5733D10 option 11 release *ONLY language *ALL deleted.)
    The standard output


  stderr (When rc as non-zero(failure), str, Product 5733D10 option *ALL release *ONLY language *ALL not installed)
    The standard error


  rc (always, int, 255)
    The task return code (0 means success, non-zero means failure)





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Chang Le (@changlexc)

