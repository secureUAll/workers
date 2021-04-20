import os 

os.system("export TARGET=http://hack.me")

os.system("docker build -t teste .")

os.system("docker run teste -host $TARGET")