import json
import logging


def sqlmap_converter(filename):

    f = open(filename)
    content = f.read()
    f.close()

    return content

    