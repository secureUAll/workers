import os
import subprocess
import argparse

def main(domain, out, filename):
    os.system("docker pull localhost/zap:v1")
    os.system("docker  run --user \"$(id -u):$(id -g)\" -v $(pwd):/zap/wrk/:rw --rm -t localhost/zap:v1 " + filename + " -t " + domain + " -J " + out)
    # usage ex: docker run --user $(id -u):$(id -g) -v $(pwd):/zap/wrk/:rw --rm -t owasp/zap2docker-stable zap-baseline.py -t https://hack.me/ -J out.json

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", help="host to scan")
    parser.add_argument("--out", help="output file", default="out.json")
    parser.add_argument("--type", help="scan type file (zap-baseline.py | zap-full-scan.py)", default="zap-baseline.py")
    args = parser.parse_args()

    main(args.domain, args.out, args.type)