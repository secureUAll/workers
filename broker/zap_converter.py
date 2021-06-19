import json

def zap_converter(filename):

    f = open(filename)
    file_data = f.read()
    f.close()

    output_json = dict()

    data = json.loads(file_data)

    #print(json.dumps(data, indent=2))
    #print(json.dumps(data, indent=2))

    output_json["TOOL"] = "zap"
     
    # ----------------------------------------- adding date -----------------------------------------
    output_json["date"] = data["@generated"] if ("@generated" in data) else None

    # ----------------------------------------- adding ports scan -----------------------------------------

    # getting scan
    script_list = data["site"] if ("site" in data) else None

    # output list 
    output_json["ports"] = list()

    # if is list
    if isinstance(script_list, list):

        # for each port
        for port in script_list:
            
            # generate eacj dict to each port
            output_port = dict()
            output_port["host"] = port["@host"] if ("@host" in port) else None
            output_port["port"] = port["@port"] if ("@port" in port) else None
            output_port["ssl"] = port["@ssl"] if ("@ssl" in port) else None
            output_port["alerts"] = list()

            # if contains vulns
            if "alerts" in port:

                # if list
                if isinstance(port["alerts"], list):

                    # for each vuln
                    for alert in port["alerts"]:

                        # generate each vuln
                        output_port_alerts = dict()
                        output_port_alerts["alert"] = alert["alert"] if ("alert" in alert) else None
                        output_port_alerts["risk"] = alert["riskcode"] if ("riskcode" in alert) else None
                        output_port_alerts["description"] = alert["desc"] if ("desc" in alert) else None
                        output_port_alerts["instances"] = list()

                        #if list
                        if isinstance(alert["instances"], list):

                            #generate instance list
                            ins_list = list()

                            # for each instance
                            for ins in alert["instances"]:
                                ins_list.append(ins["uri"])

                            # add instance list 
                            output_port_alerts["instances"] = ins_list
                        
                        # add each alert to the port
                        output_port["alerts"].append(output_port_alerts)

                        # added solution
                        output_port_alerts["solution"] = alert["solution"] if ("solution" in alert) else None

            # add each port to output list
            output_json["ports"].append(output_port)

    if len(output_json["ports"])==0 or (len(output_json["ports"])==1 and output_json["ports"][0]["alerts"]==[]) :
        output_json["state"] = "down"
    else:
        output_json["state"] = "up"



    #print(json.dumps(output_json, indent=2))
    return output_json
