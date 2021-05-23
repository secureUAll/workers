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
#data = json.dumps(xmltodict.parse(xml_content), indent=4, sort_keys=True)
data = xmltodict.parse(xml_content)

print(json.dumps(data, indent=2))

output_json = dict()



# ----------------------------------------- adding command executed -----------------------------------------
output_json["command"] = data["nmaprun"]["@args"] if ("@args" in data["nmaprun"]) else None

# ----------------------------------------- adding date -----------------------------------------
output_json["date"] = data["nmaprun"]["@startstr"] if ("@startstr" in data["nmaprun"]) else None

# if host is up
if data["nmaprun"]["runstats"]["hosts"]["@up"] != '0':

    # ----------------------------------------- adding state of host -----------------------------------------
    output_json["state"] = "up"

    # ----------------------------------------- adding address infos -----------------------------------------
    output_json["address"] = dict()
    output_json["address"]["addr"] = data["nmaprun"]["host"]["address"]["@addr"] if ("@addr" in data["nmaprun"]["host"]["address"]) else None
    output_json["address"]["addrtype"] = data["nmaprun"]["host"]["address"]["@addrtype"] if ("@addrtype" in data["nmaprun"]["host"]["address"]) else None
    output_json["address"]["addrname"] = data["nmaprun"]["host"]["hostnames"]["hostname"][0]["@name"] if ("@name" in data["nmaprun"]["host"]["hostnames"]["hostname"][0]) else None

    # ----------------------------------------- adding closed ports -----------------------------------------
    output_json["closed_ports"] = data["nmaprun"]["host"]["ports"]["extraports"]["@count"] if ("extraports" in data["nmaprun"]["host"]["ports"]) else None

    # ----------------------------------------- adding output from each port -----------------------------------------
    output_json["scan"] = list()

    # getting scanned ports list
    scan_list = data["nmaprun"]["host"]["ports"]["port"]

    # for each port
    for port in scan_list:
        # adding port infos
        element = dict()
        element["portid"] = port["@portid"] if ("@portid" in port) else None
        element["protocol"] = port["@protocol"] if ("@protocol" in port) else None
        element["state"] = port["state"]["@state"] if ("@state" in port["state"]) else None

        # adding port service info
        element["service"] = dict()
        for service_elem in port["service"]:
            element["service"]["method"] = port["service"]["@method"] if ("@method" in port["service"]) else None
            element["service"]["connection"] = port["service"]["@name"] if ("@name" in port["service"]) else None
            element["service"]["os"] = port["service"]["@ostype"] if ("@ostype" in port["service"]) else None
            element["service"]["product"] = port["service"]["@product"] if ("@product" in port["service"]) else None
            element["service"]["version"] = port["service"]["@version"] if ("@version" in port["service"]) else None

        # in case port isn't closed
        if "script" in port:
            # output list
            element["output"] = list()

            # in case output is list (has more that 1 sub scripts)
            if isinstance(port["script"], list):
                # each subscript
                each_response = dict()
                # for each subscript
                for response in port["script"]:
                    # subscript id
                    each_response["id"] = response["@id"]
                    # spliting vulnerability lines
                    str_vulns = response["@output"]
                    str_list = str_vulns.split("\n")
                    # list of vulnerabilities
                    each_response["list_vulns"] = list()
                    # for each vulnerability
                    for x in str_list:
                        each_response["list_vulns"].append(x)
                    # append each subscript to output
                    element["output"].append(each_response)

            # in case output is only 1 subscript
            else:
                # subscript id
                str_id = port["script"]["@id"]
                # spliting vulnerability lines
                str_vulns = port["script"]["@output"]
                str_list = str_vulns.split("\n")
                # for each vulnerability
                for x in str_list:
                    element["output"].append(x)
        # adding each port
        output_json["scan"].append(element)

    # adding finished info
    output_json["stats"] = dict()
    output_json["stats"]["execution_time"] = data["nmaprun"]["runstats"]["finished"]["@elapsed"]


# if host is down
else:
    output_json["state"] = "down"





#print(output_json)
#json_object = json.loads(output_json)

print(json.dumps(output_json, indent=2))

#print(data)

