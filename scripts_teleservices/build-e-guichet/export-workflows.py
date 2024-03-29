# USAGE : docker exec -ti [COMMUNE]teleservices_[COMMUNE]teleservices_1 sudo -u  wcs wcs-manage runscript --vhost=[COMMUNE]-formulaires.[DOMAIN] /opt/publik/scripts/scripts_teleservices/build-e-guichet/export-workflows.py [COMMUNE]

import os
import sys
import xml.etree.ElementTree as ET

from django.template.defaultfilters import slugify
from qommon import misc
from wcs.workflows import Workflow

for wf in Workflow.select():
    xml = wf.export_to_xml(include_id=True)
    misc.indent_xml(xml)
    xml_str = ""
    try:
        xml_str = ET.tostring(xml)
    except UnicodeDecodeError:
        try:
            from importlib import reload
        except ImportError:
            pass
        import sys

        reload(sys)
        sys.setdefaultencoding("utf8")
        xml_str = ET.tostring(xml)
    folder_store_wf = "/var/lib/wcs/xml_wf_{}".format(sys.argv[1])
    if not os.path.exists(folder_store_wf):
        os.mkdir(folder_store_wf)
    with open("{}/{}.wcs".format(folder_store_wf, slugify(wf.name)), "w+") as myfile:
        myfile.write(xml_str)
