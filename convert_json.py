import json
import logging
import time

import subprocess
import argparse
import json
import xmltodict

f = open("teste_vul.xml")
xml_content = f.read()
f.close()
#write_file = open("out_json.json", "w")
#write_file.write(json.dumps(xmltodict.parse(xml_content), indent=4, sort_keys=True))
data = json.dumps(xmltodict.parse(xml_content), indent=4, sort_keys=True)

print(data)

