#
# SPDX-License-Identifier: Apache-2.0
#

all:
	rm -rf ../plugins/modules/ibmi_powervc_os_server_capture.py
	ansible-doc-extractor --template templates/module.rst.j2 source/modules ../plugins/modules/*.py
	sphinx-build -b html source build
	touch build/.nojekyll

clean:
	rm -rf build
	rm -rf source/modules/*.rst