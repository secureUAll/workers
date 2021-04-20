import os
import subprocess
import argparse

os.system("docker pull localhost/nikto:v1")

os.system("docker  run --user \"$(id -u):$(id -g)\" -v `pwd`:`pwd` -w `pwd` -i -t localhost/nikto:v1 pwd -h {args.arg1} -o {args.arg2}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-h", help="Host to scan")
    parser.add_argument("-o", help="output file", default="out.json")

    args = parser.parse_args()


