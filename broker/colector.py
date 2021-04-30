from pymongo import MongoClient
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError
import logging
import time


#mongo_client = MongoClient("mongodb://localhost:27017/")
#print(mongo_client)



#time.sleep(10)

#logging.basicConfig(level=logging.DEBUG)

producer = KafkaProducer(bootstrap_servers='kafka:9092',
                          security_protocol='SASL_SSL',
                          ssl_cafile='./worker_certs/CARoot.pem',
                          ssl_certfile='./worker_certs/certificate.pem',
                          ssl_keyfile='./worker_certs/key.pem',
                          sasl_mechanism='PLAIN',
                          sasl_plain_username='worker',
                          sasl_plain_password='worker',
                          ssl_check_hostname=False,
                          api_version=(2,7,0))

# Write hello world to test topic
p=producer.send('test', b'ESTA A DAR ZE')
producer.flush()
print(p)
consumer = KafkaConsumer('test',bootstrap_servers='kafka:9092',
                          security_protocol='SASL_SSL',
                          ssl_cafile='./worker_certs/CARoot.pem',
                          ssl_certfile='./worker_certs/certificate.pem',
                          ssl_keyfile='./worker_certs/key.pem',
                          sasl_mechanism='PLAIN',
                          sasl_plain_username='worker',
                          sasl_plain_password='worker',
                          ssl_check_hostname=False,
                          api_version=(2,7,0))
for msg in consumer:
    print("AAAAAAAAAAAAAAAAAAAAAAAA" +msg)
    break


