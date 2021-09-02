###############################################################################
# Sevy Harris 2021-09-02
# This script takes a handful of families and perturbs the E0 and alpha values
# Based off of Bjarne's Parametric Uncertainty Paper 10.1021/jacsau.1c00276
###############################################################################

import os
from torch.quasirandom import SobolEngine
from rmgpy.data.kinetics.database import KineticsDatabase


# Define the uncertainty ranges based on the paper
DELTA_ALPHA_MAX = 0.2
DELTA_E0_MAX = 0.15

# Define the number of perturbations to run
N = 5000

# Create the pseudo randoms
sobol = SobolEngine(dimension=80, scramble=True, seed=100)
x_sobol = sobol.draw(N)

# Specify the path to the families
families_dir = "/home/moon/rmg/RMG-database/input/kinetics/families/"
if not os.path.exists(families_dir):
    raise OSError(f'Path to rules does not exist:\n{families_dir}')

database = KineticsDatabase()
database.load_families(
    path=families_dir,
    families=['Surface_Abstraction'],  # list the families to perturb
)

for key in database.families:
    family = database.families[key]
    for key in family.rules.entries.keys():
        entry = family.rules.entries[key]
        E0 = entry[0].data.E0.value
        alpha = entry[0].data.alpha.value



