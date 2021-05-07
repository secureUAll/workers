from pymongo import MongoClient
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError
import os 
import json
import logging
import time


#time.sleep(30)
colector_topics=['INIT','SCAN_REQUEST']

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

consumer.subscribe(colector_topics)

logging.warning("worker")
logging.warning(consumer.subscription())
print("1")


#init message 
random = os.urandom(16)

print("2")
# Read file with default domains
domains = []
with open("domains.txt", "r") as f:
    # by line
    for line in f:
        # add domain to list
        line = line.strip('\n')
        domains.append(line)

print("3")

# message with domains
message = {'CONFIG':{'ADDRESS_LIST':domains}}

print("hello1")
# Send address list
producer.send(colector_topics[0], key=random , value=message)
producer.flush()

print("hello")
for message in consumer:
    print(message)
    
    if message.topic == "INIT":
        # Get ID
        print(message)
        #if message.key == random:
            #WORKER_ID = message.value['WORKER_ID']

    else:
        if message.key == WORKER_ID:
            machine = message.value["MACHINE"]
            if message.value["SCRAP_LEVEL"] == 2:
                continue
            elif message.value["SCRAP_LEVEL"] == 3:
                continue
            elif message.value["SCRAP_LEVEL"] == 4:
                continue
            
            producer.send(colector_topics[1], key=WORKER_ID, value=message)
            producer.flush()
    
#logging.warning(message.topic)
#logging.warning(message.value)

    


