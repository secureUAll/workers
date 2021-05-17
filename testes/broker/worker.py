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

# runn image
#os.system("touch out.xml")
#os.system("chmod ugo+rwx out.xml")
os.system("docker  run --user \"$(id -u):$(id -g)\" --rm -v `pwd`:`pwd` -w `pwd` -t teste_vulscan -sV --script=vulscan/vulscan.nse deti-cismob.ua.pt -oX out.xml")
#os.system("cd broker")
os.system("ls -la")
#os.system("cat out.xml")
output_json = convert_to_json("out.xml")

       
    
#logging.warning(message.topic)
#logging.warning(message.value)


    


