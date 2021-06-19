import json
import logging
import re

def sqlmap_converter(filename):

    f = open(filename)
    content = f.read()
    f.close()
    text= content.replace("\n","\t")
    query= re.findall(r'(?:Parameter:)(.*?)\(.*?\)(.*?)(---)',text)
    d =dict()
    for p in query:
        for r in re.findall(r'(?:Type\:)(.*?)\t',p[1]):
            if r in d and p[0] not in d[r]:
                d[r].add(p[0])
            else:
                d[r]=[p[0]]
    return d
    



    