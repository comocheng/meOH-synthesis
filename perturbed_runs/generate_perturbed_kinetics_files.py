###############################################################################
# Sevy Harris 2021-09-02
# This script takes a handful of families and perturbs the E0 and alpha values
# Based off of Bjarne's Parametric Uncertainty Paper 10.1021/jacsau.1c00276
###############################################################################

import os
from torch.quasirandom import SobolEngine
import numpy as np
from rmgpy.data.kinetics.rules import KineticsRules

from rmgpy.data.kinetics.database import KineticsDatabase
from rmgpy.data.rmg import RMGDatabase
from rmgpy import settings


kd = KineticsDatabase()
kd.load_families(
    path="/home/moon/rmg/RMG-database/input/kinetics/families/",
    families=['Surface_Abstraction'],
)

#         self.kinetics.library_order = library_order
#         self.kinetics.load(path,
#                            families=kinetics_families,
#                            libraries=kinetics_libraries,
#                            depositories=kinetics_depositories
#                            )

# database = RMGDatabase()
# database.load_kinetics(
#     path="/home/moon/rmg/RMG-database/input/kinetics/",
#     kinetics_families=['Surface_Abstraction'],
# )

# database.load(
#     path="/home/moon/rmg/RMG-database/input/",
#     kinetics_families=['Surface_Abstraction'],
# )


# database.kinetics.families['Surface_Abstraction'].rules.entries
print(kd)
exit(0)

def read_entries(rules_path):
    """Read the entries from the rules path and return the E0 and alpha values
    """
    # I'm going to assume that the base library has the correct reference values
    E0s = []
    alphas = []

    rules = open(rules_path, 'r')
    for line in rules:
        if "alpha = " in line:
            print(line)
        if "E0 = " in line:
            print(line)
    rules.close()

    return alphas, E0s


# Define the uncertainty ranges based on the paper
DELTA_ALPHA_MAX = 0.2
DELTA_E0_MAX = 0.15

# Define the number of perturbations to run
N = 5000

# Create the pseudo randoms
sobol = SobolEngine(dimension=80, scramble=True, seed=100)
x_sobol = sobol.draw(N)

# List the families you want to perturb:
families = ['Surface_Abstraction']

# Specify the path to the libraries
families_dir = "/home/moon/rmg/RMG-database/input/kinetics/families/"

# for family in families:
#     rules_path = os.path.join(families_dir, family, 'rules.py')
#     if not os.path.exists(rules_path):
#         raise OSError(f'Path to rules does not exist:\n{rules_path}')

#     # I should use the existing rmg code for reading rule entrie
#     alphas, E0s = read_entries(rules_path)

#     kr = KineticsRules()
#     """
#     A class for working with a set of "rate rules" for a RMG kinetics family. 
#     """

#     def __init__(self, label='', name='', short_desc='', long_desc='',auto_generated=False):
#         Database.__init__(self, label=label, name=name, short_desc=short_desc, long_desc=long_desc)
#         self.auto_generated = auto_generated
        
#     def __repr__(self):
#         return '<KineticsRules "{0}">'.format(self.label)

#     def load_entry(self,