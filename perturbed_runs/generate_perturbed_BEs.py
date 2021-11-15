###############################################################################
# Sevy Harris and Chris Blais 2021-10-26
# This script takes a handful of kinetics families, kinetics libraries, and
# thermo libraries and perturbs the E0, alpha, and Ea values
# Based off of Bjarne's Parametric Uncertainty Paper 10.1021/jacsau.1c00276
###############################################################################

import os
import copy
from torch.quasirandom import SobolEngine
# from rmgpy.data.kinetics.database import KineticsDatabase
# from rmgpy.molecule import Molecule
# from rmgpy.data.thermo import ThermoDatabase
# from rmgpy import constants
from tqdm import tqdm  # this is for the progress bar cause copying stuff takes a while
import glob
import numpy as np

# WARNING - right now you need to copy this to /scratch/westgroup/methanol/perturb_5000/RMG-Py and run from there

# DFT uncertainty is about +/- 0.3 eV according to Bjarne's paper (may be smaller for atomic BEs)
DELTA_E0_MAX_eV= 0.30


# Define the number of perturbations to run
N = 5000

# Create the pseudo randoms
sobol = SobolEngine(dimension=80, scramble=True, seed=100)
x_sobol = sobol.draw(N)

# make the map of sobol columns
sobol_map = {}
sobol_col_index = 0

# These are my reference binding energies on copper
Eb_H_ref= -2.58 #eV
Eb_O_ref= -4.20 #eV
Eb_C_ref= -4.96 #eV


#This is the perturbation I want to apply
Delta=0.3 #eV

#Create Delta's within +-0.3 eV
Delta_Eb=Delta-2*x_sobol*Delta

#Add or subtract the delta from the reference binding energy
Eb_H=Eb_H_ref+Delta_Eb[:,0]
Eb_O=Eb_O_ref+Delta_Eb[:,1]
Eb_C=Eb_C_ref+Delta_Eb[:,2]

print(Eb_H)
directory='File_'
#Read in the input file, change the binding energy for H, O, C
for i, name in enumerate(glob.glob('/scratch/westgroup/methanol/perturb_BE_5000/run_****/')):
# for i, name in enumerate(glob.glob('/scratch/westgroup/methanol/perturb_5000/run_000*/')):
    s=open("input.py",'r')
    new_file_content=""    
    for line in s:
     if line.startswith("                       'H':"):
         old=line.strip()
         modified="".join(("'H': (",str(float(Eb_H[i])), ", 'eV/molecule'),"))
         new_line=line.replace(old,modified)
         new_file_content += new_line 
     elif line.startswith("                       'O':"):
         old=line.strip()
         modified="".join(("'O': (",str(float(Eb_O[i])), ", 'eV/molecule'),"))
         new_line=line.replace(old,modified)
         new_file_content += new_line 
         print
     elif line.startswith("                       'C':"):
         old=line.strip()
         modified="".join(("'C': (",str(float(Eb_C[i])), ", 'eV/molecule'),"))
         new_line=line.replace(old,modified)  
         new_file_content += new_line     
     else:
          old=line.strip()
          new_line=line.replace(old,old)
          new_file_content += new_line 

    # change rmgrc to 
    rmgrc = "database.directory /scratch/westgroup/methanol/perturb_5000/RMG-database/input/"
    rmgrc_new_file = open(name + "rmgrc", "w")
    rmgrc_new_file.write(rmgrc)
    rmgrc_new_file.close()

    #Close the file   
    s.close()
    
    #Create a new folder for the new input file and write the input file

    Name_writer="".join((name, "input_BE.py"))
    writing_file = open(Name_writer, "w")
    writing_file.write(new_file_content)
    writing_file.close()
    print(i, name)


