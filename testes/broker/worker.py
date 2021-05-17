import os 
import json
import json
import xmltodict



def convert_to_json(output_file):

    f = open(output_file)
    xml_content = f.read()
    f.close()

    #write_file = open("out_json.json", "w")
    #write_file.write(json.dumps(xmltodict.parse(xml_content), indent=4, sort_keys=True))
    return json.dumps(xmltodict.parse(xml_content), indent=4, sort_keys=True)


    





#os.system("docker pull localhost:5000/vulscan")


os.system("docker  run --name=\"vulscan_docker\" --user \"$(id -u):$(id -g)\" --volume=`pwd`:`pwd` --workdir=`pwd` -t teste_vulscan -sV --script=vulscan/vulscan.nse deti-cismob.ua.pt -oX out.xml")

os.system("docker cp vulscan_docker:/var/temp/out.xml .")

os.system("docker container stop teste_cp")
os.system("docker container rm teste_cp")
#os.system("cat out.xml")
output_json = convert_to_json("out.xml")
print(output_json)

       
    
#logging.warning(message.topic)
#logging.warning(message.value)


    


