import json
import logging
import time

import subprocess
import argparse
import json
import xmltodict

f = open("nmap_output.xml")
content = f.read()
f.close()

data = xmltodict.parse(content)

#print(json.dumps(data,indent = 2))

output_json = dict()

# --------------------- adding command executed --------------------- #
output_json["command"] = data["nmaprun"]["@args"] if ("@args" in data["nmaprun"]) else None

# --------------------------- adding date --------------------------- #
output_json["date"] = data["nmaprun"]["@startstr"] if ("@startstr" in data["nmaprun"]) else None

# ------------------------ adding scan_info ------------------------- #

output_json["scan_info"] = dict()
output_json["scan_info"]["type"] = data["nmaprun"]["scaninfo"]["@type"] if ("@type" in data["nmaprun"]["scaninfo"]) else None
output_json["scan_info"]["protocol"] = data["nmaprun"]["scaninfo"]["@protocol"] if ("@protocol" in data["nmaprun"]["scaninfo"]) else None
output_json["scan_info"]["services_number"] = data["nmaprun"]["scaninfo"]["@numservices"] if ("@numservices" in data["nmaprun"]["scaninfo"]) else None

# ------------------------ adding host_info ------------------------- #

output_json["address"] = dict()

output_json["address"]["address_ip"]= data["nmaprun"]["hosthint"]["address"]["@addr"] if ("@addr" in data["nmaprun"]["hosthint"]) else None
output_json["address"]["address_type"] = data["nmaprun"]["hosthint"]["address"]["@addrtype"] if ("@addrtype" in data["nmaprun"]["hosthint"]) else None

output_json["address"]["address_name"] = data["nmaprun"]["hosthint"]["hostnames"]["hostname"]["@name"] if ("@name" in data["nmaprun"]["hosthint"]["hostnames"]["hostname"]) else None

# ------------------------ adding host ports------------------------- #
if isinstance(data["nmaprun"]["host"]["ports"]["port"], list):
    output_json["ports"] = list()

    for l in data["nmaprun"]["host"]["ports"]["port"]:
        element = dict()
        element["protocol"] = l["@protocol"] if ("@protocol" in l) else None
        element["id"] = l["@portid"] if ("@portid" in l) else None
        element["name"] = l["service"]["@name"] if ("@name" in l["service"]) else None
        element["product"] = l["service"]["@product"] if ("@product" in l["service"]) else None
        element["version"] = l["service"]["@version"] if ("@version" in l["service"]) else None
        element["os"] = l["service"]["@ostype"] if ("@ostype" in l["service"]) else None
        element["method"] = l["service"]["@method"] if ("@method" in l["service"]) else None

        output_json["ports"].append(element)

else:
    output_json["ports"] = dict()

    output_json["ports"]["protocol"] = data["nmaprun"]["host"]["ports"]["port"]["@protocol"] if ("@protocol" in data["nmaprun"]["host"]["ports"]["port"]) else None
    output_json["ports"]["id"] = data["nmaprun"]["host"]["ports"]["port"]["@portid"] if ("@portid" in data["nmaprun"]["host"]["ports"]["port"]) else None
    output_json["ports"]["name"] = data["nmaprun"]["host"]["ports"]["port"]["service"]["@name"] if ("@name" in data["nmaprun"]["host"]["ports"]["port"]["service"]) else None
    output_json["ports"]["product"] = data["nmaprun"]["host"]["ports"]["port"]["service"]["@product"] if ("@product" in data["nmaprun"]["host"]["ports"]["port"]["service"]) else None
    output_json["ports"]["version"] = data["nmaprun"]["host"]["ports"]["port"]["service"]["@version"] if ("@version" in data["nmaprun"]["host"]["ports"]["port"]["service"]) else None
    output_json["ports"]["os"] = data["nmaprun"]["host"]["ports"]["port"]["service"]["@ostype"] if ("@ostype" in data["nmaprun"]["host"]["ports"]["port"]["service"]) else None
    output_json["ports"]["method"] = data["nmaprun"]["host"]["ports"]["port"]["service"]["@method"] if ("@method" in data["nmaprun"]["host"]["ports"]["port"]["service"]) else None












print(json.dumps(output_json, indent = 2))