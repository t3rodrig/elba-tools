# Copyright (C) 2011 Mario Orsi

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#---------------------------------------------------------------------------
# Purpose: this script reads a LAMMPS ".trj" trajectory (dump) file and 
#          extracts information on the simulation box.
# Output: 'vol.dat': box volume [angstrom^3]
#         'numDens.dat': number density [1/angstrom^3] 
#         'watDens.dat': number density [g/cm^3] 
# Usage:   python box.py dump.trj

import sys, string, linecache
from math import sqrt

A3_IN_cm3 = 1e-24; # conversion factor: Angstrom^3 -> cm^3
#watMass_g = 3e-23; # water molecular mass in grams
watMass_g = 18.01528/6.0221367e23; # water molecular mass in grams

inFileName = sys.argv[1]
inFile = open(inFileName, "r")

print "Processing file %s ..." % inFileName
line = linecache.getline(inFileName, 4)
words = string.split(line)
nAtoms = int(words[0])
print "Number of atoms: %d" % nAtoms

outVolFile = open("vol.dat", "w")
outNumDensFile = open("numDens.dat", "w")
outWatDensFile = open("watDens.dat", "w")

lineNum=0; # line counter
snapNum=1;
boxLine=5; # first instance of 'ITEM: BOX BOUNDS pp pp pp'
lines = inFile.readlines()
for line in lines:
    lineNum = lineNum + 1
    words = string.split(line)
    if len(words) == 6:
        if words[1]=="BOX":
            boxLine=lineNum
    if lineNum==boxLine+1:
        xSize = float(words[1]) - float(words[0])
    if lineNum==boxLine+2:
        ySize = float(words[1]) - float(words[0])
    if lineNum==boxLine+3:
        zSize = float(words[1]) - float(words[0])
        volume = xSize * ySize * zSize
        outVolFile.write("%f\n" % volume)
        outNumDensFile.write("%f\n" % (nAtoms/volume))
        outWatDensFile.write("%f\n" % (nAtoms*watMass_g/(volume*A3_IN_cm3)))
        
