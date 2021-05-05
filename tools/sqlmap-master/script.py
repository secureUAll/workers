import os
import subprocess
import argparse

def main(domain, ops):
    os.system("docker pull localhost/sqlmap:v1")

    if ops == "nothing":
        os.system("docker  run --user \"$(id -u):$(id -g)\" -v `pwd`:`pwd` -w `pwd` -i -t localhost/sqlmap:v1 sqlmap.py -u " + domain)
    else:
        os.system("docker  run --user \"$(id -u):$(id -g)\" -v `pwd`:`pwd` -w `pwd` -i -t localhost/sqlmap:v1 sqlmap.py -u " + domain + " " + ops)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", help="host to scan")
    parser.add_argument("--options", help="sqlmap options", default="nothing")
    args = parser.parse_args()

    main(args.domain, args.options)
