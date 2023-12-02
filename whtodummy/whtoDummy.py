# 
# copyright 2023- Mark McIntyre
#
# This script consumes data from rtl_433 and from my service to read data from a BMP/BME280
# and writes it out into a single-line json file to be consumed by my dummy driver for pywws

# The locations of the source files and target file are defined in whConfig

import json 

from whConfig import loadConfig


def loadAndSave(whfile, bpfile, targfile):
    whdata = None
    bpdata = None
    try:
        lis = open(whfile, 'r').readlines()
        whdata = json.loads(lis[-1])
    except Exception:
        pass
    try:
        lis = open(bpfile, 'r').readlines()
        bpdata = json.loads(lis[-1])
    except Exception:
        pass
    #print(whdata, bpdata)
    if whdata and bpdata:
        whdata.update(bpdata)
        #print(whdata)
        with open(targfile,'w') as outf:
            outf.write('{}'.format(json.dumps(whdata)))


if __name__ == '__main__':
    whfile, bpfile, targfile = loadConfig()
    loadAndSave(whfile, bpfile, targfile)
