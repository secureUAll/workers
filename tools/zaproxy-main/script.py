import os
import subprocess
import argparse

def main(domain, out, file_name):
    os.system("docker pull localhost/zap:v1")
    print("docker  run --user \"$(id -u):$(id -g)\" -v `pwd`:`pwd` -w `pwd` -i -t localhost/zap:v1 " + file_name + " -t " + domain + " -J " + out)
    os.system("docker  run --user \"$(id -u):$(id -g)\" -v $(pwd):/zap/wrk/:rw --rm -t localhost/zap:v1 " + file_name + " -t " + domain + " -J " + out)
    #docker run --user $(id -u):$(id -g) -v $(pwd):/zap/wrk/:rw --rm -t owasp/zap2docker-stable zap-baseline.py -t https://hack.me/ -J out.json
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", help="Host to scan")
    parser.add_argument("--out", help="output file", default="out.json")
    parser.add_argument("--type", help="scan type file", default="zap-baseline.py")
    args = parser.parse_args()

    main(args.domain, args.out, args.type)
