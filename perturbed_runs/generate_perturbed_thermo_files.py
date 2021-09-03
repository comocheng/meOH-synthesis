###############################################################################
# Sevy Harris 2021-09-03
# This script takes a handful of thermo parameters and perturbs E0
# Based off of Bjarne's Parametric Uncertainty Paper 10.1021/jacsau.1c00276
###############################################################################

import os
from torch.quasirandom import SobolEngine
from rmgpy.data.kinetics.database import KineticsDatabase


from rmgpy.data.base import Database, Entry, make_logic_node, DatabaseError
from rmgpy.ml.estimator import MLEstimator
from rmgpy.molecule import Molecule, Bond, Group
from rmgpy.species import Species
from rmgpy.data.thermo import ThermoDatabase  #, NASAPolynomial, NASA, ThermoData, Wilhoit

from rmgpy import constants

# looks like E0 is the same as NASA polynomial coefficient 5
# H(0) = R(a0*T + 1/2 a1 * T^2 + 1/3 a2 * T^3 + 1/4 a3 * T^4 + 1/5 a4 * T^5 + a5) = a5


DELTA_E0_MAX = 30  # 3 eV is about 30 kJ/mol

# Define the number of perturbations to run
N = 5

# Create the pseudo randoms
sobol = SobolEngine(dimension=80, scramble=True, seed=100)
x_sobol = sobol.draw(N)


# Specify the path to the thermo library
library_path = "/home/moon/rmg/RMG-database/input/thermo/"
if not os.path.exists(library_path):
    raise OSError(f'Path to rules does not exist:\n{library_path}')

thermo_database = ThermoDatabase()
thermo_database.load(
    library_path,
    libraries=[
        'surfaceThermoPt111',
    ],
    depository=False,
    surface=True)

# make the map of sobol columns
# TODO combine this with the kinetic parameter script to keep indexing consistent
sobol_map = {}
sobol_col_index = 0
for library_key in thermo_database.libraries:
    label = library_key + '/E0'
    sobol_map[label] = sobol_col_index
    sobol_col_index += 1

for library_key in thermo_database.libraries:
    thermo_lib = thermo_database.libraries[library_key]
    sobol_key = library_key + '/E0'
    sobol_col_index = sobol_map[sobol_key]

    for i in range(0, N):
        delta_E0 = DELTA_E0_MAX - 2.0 * x_sobol[i, sobol_col_index] * DELTA_E0_MAX

        for entry_key in thermo_lib.entries.keys():
            entry = thermo_lib.entries[entry_key]
            # Don't perturb the energy level if it's just a vacant site
            if entry_key is 'vacant':
                continue
            if entry.item.is_isomorphic(Molecule().from_adjacency_list("1 X  u0 p0 c0")):
                continue

            # Perturb the E0 value, which is a5 in the NASA polymial
            if entry.data.poly1 is not None:
                E0_ref = entry.data.poly1.c5  # not sure about this conversion factor
                E0_perturbed = E0_ref + delta_E0 / (constants.R / 1000.0)  # 8.314e-3
                entry.data.poly1.c5 = E0_perturbed
            if entry.data.poly2 is not None:
                E0_ref = entry.data.poly2.c5
                E0_perturbed = E0_ref + delta_E0 / (constants.R / 1000.0)  # 8.314e-3
                entry.data.poly2.c5 = E0_perturbed
            if entry.data.poly3 is not None:
                E0_ref = entry.data.poly3.c5
                E0_perturbed = E0_ref + delta_E0 / (constants.R / 1000.0)  # 8.314e-3
                entry.data.poly3.c5 = E0_perturbed

        thermo_lib.save(os.path.join(library_path, 'libraries', library_key + '_' + str(i).zfill(4) + '.py'))
