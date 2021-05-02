import os
import subprocess
import argparse

def main(domain, out):
    os.system("docker pull localhost/wapiti:v1")
    os.system("docker  run --user \"$(id -u):$(id -g)\" -v `pwd`:`pwd` -w `pwd` -i -t localhost/wapiti:v1 \"" + domain + "/\"" + " -f json -o" + out)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", help="Host to scan")
    parser.add_argument("--out", help="output file", default="out.json")

    args = parser.parse_args()

    main(args.domain, args.out)
