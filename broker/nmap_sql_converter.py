import json
import xmltodict
import logging

def nmap_sql_converter(filename):

    f = open(filename)
    content = f.read()
    f.close()

    data = xmltodict.parse(content)

    logging.warning(json.dumps(data,indent = 2))

    ##print(data["nmaprun"]["host"]["ports"]["port"]["script"]["@output"].split("\n")[2][4:])


    output_json = dict()

    # --------------------- adding command executed --------------------- #
    output_json["command"] = data["nmaprun"]["@args"] if ("@args" in data["nmaprun"]) else None

    # --------------------------- adding date --------------------------- #
    output_json["date"] = data["nmaprun"]["@startstr"] if ("@startstr" in data["nmaprun"]) else None

    # ------------------------ adding scan_info ------------------------- #

    if "scaninfo" in data["nmaprun"]:
        output_json["scan_info"] = dict()
        output_json["scan_info"]["type"] = data["nmaprun"]["scaninfo"]["@type"] if ("@type" in data["nmaprun"]["scaninfo"]) else None
        output_json["scan_info"]["protocol"] = data["nmaprun"]["scaninfo"]["@protocol"] if ("@protocol" in data["nmaprun"]["scaninfo"]) else None
        output_json["scan_info"]["services_number"] = data["nmaprun"]["scaninfo"]["@numservices"] if ("@numservices" in data["nmaprun"]["scaninfo"]) else None

    # ------------------------ adding host info ------------------------- #

    if "hosthint" in data["nmaprun"]:
        output_json["address"] = dict()

        output_json["address"]["address_ip"]= data["nmaprun"]["hosthint"]["address"]["@addr"] if ("@addr" in data["nmaprun"]["hosthint"]) else None
        output_json["address"]["address_type"] = data["nmaprun"]["hosthint"]["address"]["@addrtype"] if ("@addrtype" in data["nmaprun"]["hosthint"]) else None

        if "hostnames" in data["nmaprun"]["hosthint"]:
            if data["nmaprun"]["hosthint"]["hostnames"] != None:
                if "hostname" in data["nmaprun"]["hosthint"]["hostnames"]:
                    output_json["address"]["address_name"] = data["nmaprun"]["hosthint"]["hostnames"]["hostname"]["@name"] if ("@name" in data["nmaprun"]["hosthint"]["hostnames"]["hostname"]) else None

    # ------------------------ adding host ports------------------------- #
    if "host" in data["nmaprun"]:
        if "ports" in data["nmaprun"]["host"]:
            if "port" in data["nmaprun"]["host"]["ports"]:

                output_json["ports"] = dict()

                output_json["ports"]["protocol"] = data["nmaprun"]["host"]["ports"]["port"]["@protocol"] if ("@protocol" in data["nmaprun"]["host"]["ports"]["port"]) else None
                output_json["ports"]["id"] = data["nmaprun"]["host"]["ports"]["port"]["@portid"] if ("@portid" in data["nmaprun"]["host"]["ports"]["port"]) else None
                output_json["ports"]["name"] = data["nmaprun"]["host"]["ports"]["port"]["service"]["@name"] if ("@name" in data["nmaprun"]["host"]["ports"]["port"]["service"]) else None
                output_json["ports"]["product"] = data["nmaprun"]["host"]["ports"]["port"]["service"]["@product"] if ("@product" in data["nmaprun"]["host"]["ports"]["port"]["service"]) else None
                output_json["ports"]["version"] = data["nmaprun"]["host"]["ports"]["port"]["service"]["@version"] if ("@version" in data["nmaprun"]["host"]["ports"]["port"]["service"]) else None
                output_json["ports"]["os"] = data["nmaprun"]["host"]["ports"]["port"]["service"]["@ostype"] if ("@ostype" in data["nmaprun"]["host"]["ports"]["port"]["service"]) else None
                output_json["ports"]["method"] = data["nmaprun"]["host"]["ports"]["port"]["service"]["@method"] if ("@method" in data["nmaprun"]["host"]["ports"]["port"]["service"]) else None

                output_json["ports"]["script"] = list()

                if "script" in data["nmaprun"]["host"]["ports"]["port"]:
                    for link in data["nmaprun"]["host"]["ports"]["port"]["script"]["@output"].split("\n"):
                        #print(link)
                        if link != '' and link != '  Possible sqli for queries:':
                            output_json["ports"]["script"].append(link.strip())







    # -------------------------- adding run stats -------------------------- #
    output_json["run_stats"] = dict()
    output_json["run_stats"]["time"] = data["nmaprun"]["runstats"]["finished"]["@timestr"] if ("@timestr" in data["nmaprun"]["runstats"]["finished"]) else None
    output_json["run_stats"]["summary"] = data["nmaprun"]["runstats"]["finished"]["@summary"] if ("@summary" in data["nmaprun"]["runstats"]["finished"]) else None
    output_json["run_stats"]["elapsed_time"] = data["nmaprun"]["runstats"]["finished"]["@elapsed"] if ("@elapsed" in data["nmaprun"]["runstats"]["finished"]) else None
    output_json["run_stats"]["exit_code"] = data["nmaprun"]["runstats"]["finished"]["@exit"] if ("@exit" in data["nmaprun"]["runstats"]["finished"]) else None

    output_json["run_stats"]["host"] = dict()
    output_json["run_stats"]["host"]["up"] = data["nmaprun"]["runstats"]["hosts"]["@up"] if ("@up" in data["nmaprun"]["runstats"]["hosts"]) else None
    output_json["run_stats"]["host"]["down"] = data["nmaprun"]["runstats"]["hosts"]["@down"] if ("@down" in data["nmaprun"]["runstats"]["hosts"]) else None
    output_json["run_stats"]["host"]["total"] = data["nmaprun"]["runstats"]["hosts"]["@total"] if ("@total" in data["nmaprun"]["runstats"]["hosts"]) else None


    logging.warning(json.dumps(output_json, indent = 2))
    return output_json

