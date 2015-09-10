#!/usr/bin/env python

# Script: calcIsothermComp.py
# Author: Mario Orsi (m.orsi at qmul.ac.uk, www.orsi.sems.qmul.ac.uk)
# Purpose: Calculates isothermal compressibility (kappa_T) [1]
# Syntax: python calcIsothermComp.py rho1 rho2 P1 P2
#         rho1 = density at P1
#         rho2 = density at P2
#         P1 = pressure [atm]
#         P2 = pressure [atm]
# Examples: python calcIsothermComp.py 0.95 1.05 -1150 2550
# Notes: Experimental value is 4.58 * 10^(-5) / atm [2]
# References: [1] Glattli et al, J Chem Phys 2002, 116, 9811
#             [2] Kell, J Chem Eng Data 12, 66 (1967)
#             [3] Ding et al, Molecular Simulation, 
#                 DOI: 10.1080/08927022.2015.1047367 

import sys, math

if len(sys.argv) != 5:
  print "Syntax: python calcIsothermComp.py rho1 rho2 P1 P2"
  sys.exit()

rho1 = float(sys.argv[1])
rho2 = float(sys.argv[2])
P1 = float(sys.argv[3])
P2 = float(sys.argv[4])

print "%f *10^(-5) / atm" % (10**5 * math.log(rho2/rho1)/(P2-P1))
