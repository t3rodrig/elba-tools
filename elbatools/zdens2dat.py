#!/usr/bin/env python

# Script: zdens2dat.py
# Syntax: python zdens2dat.py inFile outFile

import sys

if len(sys.argv) != 3:
    print("Syntax: python zdens2dat.py inFile outFile")
    sys.exit()

inFileName = sys.argv[1]
inFile = open(inFileName, "r")
lines = inFile.readlines()
inFile.close()

outFileName = sys.argv[2]
outFile = open(outFileName, "w")
# read input data:
for line in lines:
    if line[0] != '#': # ignore comments
        words = line.split()
        if len(words) == 3:
            nBins = int(words[1])
        if len(words) == 4:
            outFile.write("{0} {1}\n".format(words[1], words[3])) # print coord, ydens
outFile.close()
