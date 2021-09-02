###############################################################################
# Sevy Harris 2021-09-02
# This script takes a handful of families and perturbs the E0 and alpha values
# Based off of Bjarne's Parametric Uncertainty Paper 10.1021/jacsau.1c00276
###############################################################################

import os
from torch.quasirandom import SobolEngine
from rmgpy.data.kinetics.database import KineticsDatabase


# Define the uncertainty ranges based on the paper
DELTA_ALPHA_MAX = 0.15
DELTA_E0_MAX = 30  # 3 eV is about 30 kJ/mol

# Define the number of perturbations to run
N = 5

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
