#!/usr/bin/env python

# Script: calcAreaComp.py
# Author: Mario Orsi (orsimario at gmail.com, www.soton.ac.uk/~orsi)
# Purpose: Reads a file containing the time evolution of the interfacial
#          area of a lipid bilayer (usually the xy area )and calculates
#          the corresponding area compressibility (stretch) modulus
# Syntax: calcAreaComp.py inputFile temperature
# Note: input area data are in Angstrom^2
# Example: calcAreaComp.py xyArea.dat 303.15
# Reference: - Orsi et al, J Phys Condens Matter 22: 155106 (2010),
#              section 5.1.2
#            - Waheed & Edholm, Biophys J 97: 2754 (2009)

import sys, string
from math import sqrt

kB = 1.3806505e-23 # Boltzmann constant [J / K]
A2_in_nm2 = 1e-2 # 1 Angstrom^2 = 10^(-2) nm^2
A4_in_nm4 = 1e-4 # 1 Angstrom^4 = 10^(-4) nm^4
J_nm2__in__dyn_cm = 1e21 # 1 J/nm^2 = 10^21 dyn/cm

if len(sys.argv) != 3:
  print "Syntax: calcAreaComp.py inputFile temperature"
  sys.exit()

inFileName = sys.argv[1]
T = float(sys.argv[2])
inFile = open(inFileName, "r")
lines = inFile.readlines()
inFile.close()

nLines = 0 # total number of lines in the file
lineCounter = 0

areaSum = squareAreaSum = 0
areaSum1 = squareAreaSum1 = 0
areaSum2 = squareAreaSum2 = 0

nData = nData1 = nData2 = 0 # counter for number of data (measurements)

for line in lines:
    if line[0] != '#': # ignore comments
        nData += 1

for line in lines: 
    if line[0] != '#': # ignore comments
        lineCounter = lineCounter + 1
        words = string.split( line )
        area = string.atof(words[1]);
        areaSum += area
        squareAreaSum += area**2
        if lineCounter <= nData/2 : # first half of lines
            nData1 += 1
            areaSum1 += area
            squareAreaSum1 += area**2
        else: # second half of lines
            nData2 += 1
            areaSum2 += area
            squareAreaSum2 += area**2
            
# check:
if nData != nData1+nData2:
    print "ERROR: wrong scanning of data - check script"

# Calc modulus considering all data:
meanArea = areaSum / nData;
print "meanArea = %4.2f A^2" % meanArea
meanSquaredAreaFluct = squareAreaSum / nData - meanArea**2
print "meanSquaredAreaFluct = %6.3f A^4" % meanSquaredAreaFluct
# convert A -> nm:
meanArea *= A2_in_nm2 
meanSquaredAreaFluct *= A4_in_nm4
# computing modulus:
KA = kB*T * meanArea / meanSquaredAreaFluct # [ J / nm^2 ]
# convert J/nm^2 -> 10^21 dyn/cm:
KA *= J_nm2__in__dyn_cm
print "KA_total = %6.1f dyn/cm\n" % KA

# Calc modulus considering only first half of data:
meanArea1 = areaSum1 / nData1;
print "meanArea1 = %4.2f A^2" % meanArea1
print "squareAreaSum1 / nData1= %4.2f A^2" % (squareAreaSum1/ nData1)
print "meanArea1**2 = %4.2f A^2" % (meanArea1**2)
meanSquaredAreaFluct1 = squareAreaSum1 / nData1 - meanArea1**2
print "meanSquaredAreaFluct1 = %6.3f A^4" % meanSquaredAreaFluct1
# convert A -> nm:
meanArea1 *= A2_in_nm2 
meanSquaredAreaFluct1 *= A4_in_nm4
# computing modulus:
KA1 = kB*T * meanArea1 / meanSquaredAreaFluct1 # [ J / nm^2 ]
# conversion considering that J/nm^2 = 10^21 dyn/cm
KA1 *= J_nm2__in__dyn_cm
print "KA_1 = %6.1f dyn/cm\n" % ( KA1 )

# Calc modulus considering only second half of data:
meanArea2 = areaSum2 / nData2;
print "meanAreaSecond2 = %4.2f A^2" % meanArea2
print "squareAreaSum2/ nData2 = %4.2f A^2" % (squareAreaSum2/ nData2)
print "meanArea2**2 = %4.2f A^2" % (meanArea2**2)
meanSquaredAreaFluct2 = squareAreaSum2 / nData2 - meanArea2**2
print "meanSquaredAreaFluct2 = %6.3f A^4" % meanSquaredAreaFluct2
# convert A -> nm:
meanArea2 *= A2_in_nm2 
meanSquaredAreaFluct2 *= A4_in_nm4
# computing modulus:
KA2 = kB*T * meanArea2 / meanSquaredAreaFluct2 # [ J / nm^2 ]
# conversion considering that J/nm^2 = 10^21 dyn/cm
KA2 *= J_nm2__in__dyn_cm
print "KA_2 = %6.1f dyn/cm\n" % ( KA2 )

# Calc average:
KA_avg12 = 0.5 * ( KA1 + KA2 )
print "KA_avg12 = %6.1f dyn/cm" % KA_avg12
standardDeviation = sqrt( ( KA1 - KA_avg12 )**2 + ( KA2 - KA_avg12 )**2 )
standardError = standardDeviation / sqrt(2)
print "Standard error = %6.1f dyn/cm\n" % standardError
