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

database = ThermoDatabase()
database.load(
    library_path,
    libraries=[
        'surfaceThermoPt111',
        # 'surfaceThermoPt_C',
    ],
    depository=False,
    surface=True)

database.libraries['surfaceThermoPt111']
database.libraries['surfaceThermoPt111'].entries
database.libraries['surfaceThermoPt111'].entries['vacant']
database.libraries['surfaceThermoPt111'].entries['vacant'].data

database.libraries['surfaceThermoPt111'].entries['vacant'].data.poly1  # and poly2 and poly3, looks like hardcoded limit of 3
database.libraries['surfaceThermoPt111'].entries['vacant'].data.poly1.coeffs[5]
print("done")
exit(0)

# make the map of sobol columns
sobol_map = {}
sobol_col_index = 0
for family_key in database.families:
    family = database.families[family_key]
    for entry_key in family.rules.entries.keys():
        label = family_key + '/' + entry_key + '/alpha'
        sobol_map[label] = sobol_col_index
        sobol_col_index += 1
        label = family_key + '/' + entry_key + '/E0'
        sobol_map[label] = sobol_col_index
        sobol_col_index += 1

for key in database.families:
    family = database.families[key]
    for i in range(0, N):
        for entry_key in family.rules.entries.keys():
            entry = family.rules.entries[entry_key]

            # Perturb the alpha value
            alpha_ref = entry[0].data.alpha.value
            sobol_key = family_key + '/' + entry_key + '/alpha'
            sobol_col_index = sobol_map[sobol_key]
            delta_alpha = DELTA_ALPHA_MAX - 2.0 * x_sobol[i, sobol_col_index] * DELTA_ALPHA_MAX
            alpha_perturbed = alpha_ref + delta_alpha
            entry[0].data.alpha.value = alpha_perturbed

            # Perturb the E0 value
            E0_ref = entry[0].data.E0.value
            sobol_key = family_key + '/' + entry_key + '/E0'
            sobol_col_index = sobol_map[sobol_key]
            delta_E0 = DELTA_E0_MAX - 2.0 * x_sobol[i, sobol_col_index] * DELTA_E0_MAX
            E0_perturbed = E0_ref + delta_E0
            entry[0].data.E0.value = E0_perturbed

        family.rules.save(os.path.join(families_dir, key, 'rules' + str(i).zfill(4) + '.py'))
