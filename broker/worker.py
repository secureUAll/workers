from pymongo import MongoClient
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError

# converter files import
from nmap_converter import *
from vulscan_converter import *
from nikto_converter import *

import os 
import json
import logging
import time

import subprocess
import argparse
import json
import xmltodict
import random


# topics from colector
colector_topics=['INIT','SCAN_REQUEST','LOG']

# golbal variable 
WORKER_ID = 0

#logging.basicConfig(level=logging.DEBUG)

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

# consumer loop
for message in consumer:
    
    # initial message response to save WORKER_ID
    if message.topic == "INIT":
        # Get ID
        if message.key == random_id and "WORKER_ID" in message.value:
            # getting actual Worker ID
            logging.warning(message.value)
            WORKER_ID = message.value['WORKER_ID']

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
            os.system("docker container stop nikto_docker")
            os.system("docker container rm nikto_docker")
            os.system("docker container stop vulscan_docker")
            os.system("docker container rm vulscan_docker")
            os.system("docker container stop nmap_docker")
            os.system("docker container rm nmap_docker")

            # level 1
            if scrapping_level >= 1:

                # ------- NIKTO ------- #

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
                
                #getting json data from file
                json_nikto = nikto_converter(random_filename)
                output.append(json_nikto)
                os.system("rm " + random_filename)

                #producer.send(colector_topics[2], key=bytes([WORKER_ID]), value={"MACHINE":machine, "TOOL": "nikto", "LEVEL": 1, "RESULTS":json_nikto})
                #producer.flush()


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


            # level 2 (default)
            if scrapping_level >= 2:
                # pull image from registry
                os.system("docker pull localhost:5000/vulscan")
                # runn tool
                os.system("docker run --name=\"vulscan_docker\" --user \"$(id -u):$(id -g)\" --volume=`pwd`:`pwd` --workdir=`pwd` -t localhost:5000/vulscan -sV --script=vulscan/vulscan.nse " + machine + " -oX out_vulscan.xml")
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

            # level 3
            if scrapping_level >= 3:
                continue

            # level 4
            if scrapping_level >= 4:
                continue

            producer.send(colector_topics[2], key=bytes([WORKER_ID]), value={"MACHINE":machine,  "LEVEL": scrapping_level, "RESULTS":output})
            producer.flush()

#logging.warning(message.topic)
#logging.warning(message.value)


    


