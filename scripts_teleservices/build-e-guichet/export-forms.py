# USAGE : docker exec -ti [COMMUNE]teleservices_[COMMUNE]teleservices_1 sudo -u  wcs wcs-manage runscript --vhost=[COMMUNE]-formulaires.[DOMAIN] /opt/publik/scripts/scripts_teleservices/build-e-guichet/export-forms.py [COMMUNE]

import os
import sys
import xml.etree.ElementTree as ET

from qommon import misc
from wcs.formdef import FormDef

for formdef in FormDef.select():
    xml = formdef.export_to_xml(include_id=True)
    misc.indent_xml(xml)
    xml_str = ET.tostring(xml)
    folder_store_forms = "/var/lib/wcs/xml_forms_{}".format(sys.argv[1])
    if not os.path.exists(folder_store_forms):
        os.mkdir(folder_store_forms)
    with open("{}/{}.wcs".format(folder_store_forms, formdef.internal_identifier), "w+") as myfile:
        myfile.write(xml_str)
