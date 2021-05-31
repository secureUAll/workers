# read json file
import os 
import json
import logging
import time

import subprocess
import argparse
import json


def nikto_converter(filename):


    # read and load json from file
    f = open(filename)
    file_data = f.read()
    data = json.loads(file_data)

    #print(json.dumps(data, indent=2))

    # final output
    output_json = dict()

    # address info dict output
    output_json["address"] = dict()
    output_json["address"]["address_ip"] = data["ip"] if ("ip" in data) else None
    output_json["address"]["address_name"] = data["host"] if ("host" in data) else None
    output_json["port"] = data["port"] if ("port" in data) else None
    output_json["banner"] = data["banner"] if ("banner" in data) else None

    # list vulns output
    output_vulns = list()

    # if more than 1 vuln 
    if isinstance(data["vulnerabilities"], list):

        # for each vuln
        for vuln in data["vulnerabilities"]:
            each_vuln_dict = dict()
            each_vuln_dict["method"] = vuln["method"] if ("method" in vuln) else None
            each_vuln_dict["url"] = vuln["url"] if ("url" in vuln) else None
            each_vuln_dict["message"] = vuln["msg"] if ("msg" in vuln) else None

            # append each vuln to list
            output_vulns.append(each_vuln_dict)
    
    # if only 1 vuln
    elif isinstance(data["vulnerabilities"], dict):
        
        vuln = dict()
        vuln["method"] = vuln["method"] if ("method" in vuln) else None
        vuln["url"] = vuln["url"] if ("url" in vuln) else None
        vuln["message"] = vuln["msg"] if ("msg" in vuln) else None

        # append vuln to list
        output_vulns.append(vuln)
    
    # append vulns to final output
    output_json["scan"] = output_vulns

    # append tool name
    output_json["TOOL"] = "nikto"


    print(json.dumps(output_json, indent=2))
    
    
    return json.dumps(output_json, indent=2)