import os
import subprocess

os.environ['TARGET'] = 'hack.me'

os.system("docker pull localhost/nikto:v1")

# os.system("docker run --user \"$(id -u):$(id -g)\" localhost/nikto:v1 -h $TARGET -o response.json")

# os.system("docker run localhost/nikto:v1 -h $TARGET -o response.json")

os.system("docker  run --user \"$(id -u):$(id -g)\" -v `pwd`:`pwd` -w `pwd` -i -t localhost/nikto:v1 pwd -h hack.me -o testinho.json")
