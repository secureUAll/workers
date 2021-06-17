from pymongo import MongoClient
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError

# converter files import
from nmap_converter import *
from vulscan_converter import *
from nikto_converter import *
from zap_converter import *
from malware_converter import *
from nmap_sql_converter import *

import os 
import json
import logging
import time

import subprocess
import argparse
import json
import xmltodict
import random



# ------------------------------------------------------------------------------- #
#                                 Global variables                                #
# ------------------------------------------------------------------------------- #

# topics from colector
colector_topics=['INIT','SCAN_REQUEST','LOG','UPDATE']

# golbal variable 
WORKER_ID = 0

malware_ports = {
                        1080: "mydoom",
                        2283: "dumaru",
                        2535: "beagle",
                        2745: "beagle",
                        3127: "mydoom",
                        3128: "mydoom",
                        3410: "backdoor",
                        5554: "sasser",
                        8866: "beagle",
                        9898: "dabber",
                        10000: "dumaru",
                        10080: "mydoom",
                        12345: "netbus",
                        17300: "kuang2",
                        27374: "subseven",
                        65506: "phatbot"
                    }

#logging.basicConfig(level=logging.DEBUG)



# ------------------------------------------------------------------------------- #
#                                 Read Domains                                    #
# ------------------------------------------------------------------------------- #

def read_and_send_domains():
    # Read file with default domains
    domains = []
    with open("domains.txt", "r") as f:
        # by line
        for line in f:
            # add domain to list
            line = line.strip('\n')
            domains.append(line)

    #random to init message 
    random_id = os.urandom(16)
    # message with domains
    message = {'CONFIG':{'ADDRESS_LIST':domains}}

    # Send address list
    producer.send(colector_topics[0], key=random_id , value=message)
    producer.flush()

    return random_id



# ------------------------------------------------------------------------------- #
#                                 Consume messages                                #
# ------------------------------------------------------------------------------- #

def consume_messages(random_id):
    
    global WORKER_ID
    
    # consumer loop
    for message in consumer:

        # ------------------------------- Initial topic ----------------------------------------- #
        
        # initial message response to save WORKER_ID
        if message.topic == "INIT":
            # Get ID
            if message.key == random_id and "WORKER_ID" in message.value:
                # getting actual Worker ID
                logging.warning(message.value)
                WORKER_ID = message.value['WORKER_ID']

        # ------------------------------- Update domains topic ----------------------------------------- #

        # topic to update domains
        elif message.topic == "UPDATE":
            logging.warning("UPDATE MESSAGE")
            logging.warning(message.value)
            # check if update is for this worker
            if int.from_bytes(message.key,"big") == WORKER_ID:

                # get new address list
                new_address_list = message.value["ADDRESS_LIST"]
                
                # write in domains file
                with open("domains.txt", "w") as f:
                    for dom in new_address_list:
                        f.write(dom)
                        f.write("\n")

                # update local variable with domains
                domains = new_address_list

        # ------------------------------- scrapping topic ----------------------------------------- #

        # scrapping request topic
        elif message.topic== colector_topics[1]:
            # logs
            logging.warning(int.from_bytes(message.key,"big"))
            logging.warning(WORKER_ID)

            # in case request is to this worker
            if int.from_bytes(message.key,"big") == WORKER_ID:

                output=[]
                logging.warning(message.value)
                # get machine to scan
                machine = message.value["MACHINE"]
                # get scrapping level
                scrapping_level = int(message.value["SCRAP_LEVEL"])


                # removing potential non-stopped containers from previous scan
                os.system("docker container stop vulscan_docker")
                os.system("docker container rm vulscan_docker")
                os.system("docker container stop nmap_docker")
                os.system("docker container rm nmap_docker")
                os.system("docker container stop nmap_docker_malware")
                os.system("docker container rm nmap_docker_malware")
                os.system("docker container stop zap_docker")
                os.system("docker container rm zap_docker")
                os.system("docker container stop nikto_docker")
                os.system("docker container rm nikto_docker")

                # level 1
                if scrapping_level >= 1:

                    # ------------------------------- Normal nmap tool ----------------------------------------- #

                    os.system("docker pull localhost:5000/nmap")
                    # run tool
                    os.system("docker run --name=\"nmap_docker\" --user \"$(id -u):$(id -g)\" --volume=`pwd`:`pwd` --workdir=`pwd` -t localhost:5000/nmap -A -T5 " + machine + " -oX nmap_output.xml")
                    #copy file to container
                    os.system("docker cp nmap_docker:/var/temp/nmap_output.xml .")
                    #stop and remove containers
                    os.system("docker container stop nmap_docker")
                    os.system("docker container rm nmap_docker")

                    nmap_output = nmap_converter("nmap_output.xml")
                    output.append(nmap_output)

                    # ------------------------------- Scanning for malwares common ports ----------------------------------------- #

                    os.system("docker pull localhost:5000/nmap")
                    # run tool
                    os.system("docker run --name=\"nmap_docker_malware\" --user \"$(id -u):$(id -g)\" --volume=`pwd`:`pwd` --workdir=`pwd` -t localhost:5000/nmap -p 1080,2283,2535,2745,3127,3128,3410,5554,8866,9898,10000,10080,12345,17300,27374,65506 " + machine + " -oX nmap_malware_output.xml")
                    #copy file to container
                    os.system("docker cp nmap_docker_malware:/var/temp/nmap_malware_output.xml .")
                    #stop and remove containers
                    os.system("docker container stop nmap_docker_malware")
                    os.system("docker container rm nmap_docker_malware")

                    malware_output = malware_converter("nmap_malware_output.xml")

                    output.append(malware_output)



                # level 2 (default)
                if scrapping_level >= 2:

                    # ------------------------------- Nmap with vulscan tool ----------------------------------------- #

                    # pull image from registry
                    os.system("docker pull localhost:5000/vulscan")
                    # runn tool
                    os.system("docker run --name=\"vulscan_docker\" --user \"$(id -u):$(id -g)\" --volume=`pwd`:`pwd` --workdir=`pwd` -t localhost:5000/vulscan:v2 -sV --script=vulscan/vulscan.nse " + machine + " -oX out_vulscan.xml")
                    #copy file to container
                    os.system("docker cp vulscan_docker:/var/temp/out_vulscan.xml .")
                    #stop and remove containers
                    os.system("docker container stop vulscan_docker")
                    os.system("docker container rm vulscan_docker")

                    # convert from xml to json
                    output_json = vulscan_converter("out_vulscan.xml")

                    output.append(output_json)
                    #logging.warning("vai mandar")
                    #producer.send(colector_topics[2], key=bytes([WORKER_ID]), value={"MACHINE":machine, "TOOL": "vulscan", "LEVEL": 2, "RESULTS":output_json})
                    #producer.flush()

                    # ------------------------------- Zaproxy tool ----------------------------------------- #

                    os.system("docker pull localhost:5000/zap")

                    if machine.find("http://") != -1 or machine.find("https://") != -1:
                        logging.warning(machine)
                        os.system("docker run --name=\"zap_docker\" --user \"$(id -u):$(id -g)\" -v $(pwd):/zap/wrk/:rw -t localhost:5000/zap zap-baseline.py -t " + machine + " -J out_zap.json")
                    else:
                        logging.warning("entrou")
                        logging.warning("http://" + machine)
                        os.system("docker run --name=\"zap_docker\" --user \"$(id -u):$(id -g)\" -v $(pwd):/zap/wrk/:rw -t localhost:5000/zap zap-baseline.py -t http://" + machine + " -J out_zap.json")

                    os.system("docker cp zap_docker:/zap/wrk/out_zap.json .")

                    os.system("docker container stop zap_docker")
                    os.system("docker container rm zap_docker")

                    zap_output = zap_converter("out_zap.json")

                    output.append(zap_output)
                    
                    

                # level 3
                if scrapping_level >= 3:
                    # ------------------------------- Nikto tool ----------------------------------------- #

                    # pull image from registry
                    os.system("docker pull localhost:5000/nikto")
                    # erase output file
                    random_filename = str(random.randint(0, 100000)) + ".json"
                    # run tool
                    os.system("docker run --name=\"nikto_docker\" --user \"$(id -u):$(id -g)\" --volume=`pwd`:`pwd` --workdir=`pwd` -t localhost:5000/nikto -h " + machine + " -o " + random_filename)
                    #copy file to container
                    os.system("docker cp nikto_docker:/var/temp/" + random_filename + " .")

                    #stop and remove containers
                    os.system("docker container stop nikto_docker")
                    os.system("docker container rm nikto_docker")
                    os.system("ls -l " + random_filename)
                    #getting json data from file
                    json_nikto = nikto_converter(random_filename)
                    output.append(json_nikto)
                    
                    os.system("rm " + random_filename)

                    #producer.send(colector_topics[2], key=bytes([WORKER_ID]), value={"MACHINE":machine, "TOOL": "nikto", "LEVEL": 1, "RESULTS":json_nikto})
                    #producer.flush()

                # level 4
                # if scrapping_level >= 4:
                if scrapping_level < 4:

                    os.system("docker pull localhost:5000/nmap")
                    # run tool
                    os.system("docker run --name=\"nmap_sql_docker\" --user \"$(id -u):$(id -g)\" --volume=`pwd`:`pwd` --workdir=`pwd` -t localhost:5000/nmap -sV --script http-sql-injection " + machine + " -p 80 -oX nmap_sql_output.xml")
                    #copy file to container
                    os.system("docker cp nmap_sql_docker:/var/temp/nmap_sql_output.xml .")
                    os.system("cat nmap_sql_output.xml")
                    #stop and remove containers
                    os.system("docker container stop nmap_sql_docker")
                    os.system("docker container rm nmap_sql_docker")

                    nmap_sql_output = nmap_sql_converter("nmap_sql_output.xml")

                    os.system("docker pull localhost:5000/sqlmap")


                    if "script" in nmap_sql_output["ports"]:
                        if len(nmap_sql_output["ports"]) > 0:

                            for vuln_link in nmap_sql_output["ports"]["script"]:
                                # run tool
                                os.system("docker run --name=\"sql_docker\" --user \"$(id -u):$(id -g)\" --volume=`pwd`:/root/.local/share/sqlmap/output/ -t localhost:5000/sqlmap -u " + vuln_link + " --dbs")
                                #copy file to container
                                os.system("docker cp sql_docker:/root/.local/share/sqlmap/output/ .")
                                os.system("ls")
                                #os.system("cat nmap_sql_output.xml")
                                #stop and remove containers
                                os.system("docker container stop nmap_sql_docker")
                                os.system("docker container rm nmap_sql_docker")


                    #output.append(nmap_sql_output)
                    continue

                # ------------------------------- Send all outputs to colector ----------------------------------------- #

                producer.send(colector_topics[2], key=bytes([WORKER_ID]), value={"MACHINE":machine, "MACHINE_ID": message.value["MACHINE_ID"], "LEVEL": scrapping_level, "RESULTS":output})
                producer.flush()

#logging.warning(message.topic)
#logging.warning(message.value)



# ------------------------------------------------------------------------------- #
#                                 Main function                                   #
# ------------------------------------------------------------------------------- #

if __name__ == "__main__":
    
    # ------------------------------- Initial configs ----------------------------------------- #

    #kafka producer
    producer = KafkaProducer(bootstrap_servers='kafka:9092',
                            security_protocol='SASL_SSL',
                            ssl_cafile='./worker_certs/CARoot.pem',
                            ssl_certfile='./worker_certs/certificate.pem',
                            ssl_keyfile='./worker_certs/key.pem',
                            sasl_mechanism='PLAIN',
                            sasl_plain_username='worker',
                            sasl_plain_password='worker',
                            ssl_check_hostname=False,
                            api_version=(2,7,0),
                            value_serializer=lambda m: json.dumps(m).encode('latin'))


    #kafka consumer
    consumer = KafkaConsumer(bootstrap_servers='kafka:9092',
                            auto_offset_reset='earliest',
                            security_protocol='SASL_SSL',
                            ssl_cafile='./worker_certs/CARoot.pem',
                            ssl_certfile='./worker_certs/certificate.pem',
                            ssl_keyfile='./worker_certs/key.pem',
                            sasl_mechanism='PLAIN',
                            sasl_plain_username='worker',
                            sasl_plain_password='worker',
                            ssl_check_hostname=False,
                            api_version=(2,7,0),
                            value_deserializer=lambda m: json.loads(m.decode('latin')),
                            fetch_max_wait_ms=0)

    #subscription to the kafka topics
    consumer.subscribe(colector_topics)

    # logs
    logging.warning("worker")
    logging.warning(consumer.subscription())

    # ------------------------------- Read domains ----------------------------------------- #

    random_id = read_and_send_domains()

    # ------------------------------- Consume messages ----------------------------------------- #

    consume_messages(random_id)





    


