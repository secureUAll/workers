import os
import subprocess

os.environ['TARGET'] = 'http://hack.me'

os.system("docker pull localhost/nikto:v1")

os.system("docker run --user \"$(id -u):$(id -g)\" localhost/nikto:v1 -h $TARGET -o out.json")
