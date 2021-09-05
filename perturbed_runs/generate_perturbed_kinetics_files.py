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

# Specify the path to the libraries
kinetic_libraries_dir = "/home/moon/rmg/RMG-database/input/kinetics/libraries/Surface/"
if not os.path.exists(kinetic_libraries_dir):
    raise OSError(f'Path to kinetic libraries does not exist:\n{kinetic_libraries_dir}')

kinetics_database = KineticsDatabase()
kinetics_database.load_families(
    path=families_dir,
    families=['Surface_Abstraction'],  # list the families to perturb
)

kinetics_database.load_libraries(
    kinetic_libraries_dir,
    libraries=[
        'Example',  # just checking if this connects
        # 'Ni111',
    ]
)

# pick which entries to perturb in the kinetics library
# WARNING: does not handle overlap of entries in different libraries
lib_entries_to_perturb = [
    "OCX + OX <=> CO2 + Ni + Ni",
    # "CO2X + Ni <=> OCX + OX"
]

# make the map of sobol columns
sobol_map = {}
sobol_col_index = 0
for family_key in kinetics_database.families:
    family = kinetics_database.families[family_key]
    for entry_key in family.rules.entries.keys():
        label = family_key + '/' + entry_key + '/alpha'
        sobol_map[label] = sobol_col_index
        sobol_col_index += 1
        label = family_key + '/' + entry_key + '/E0'
        sobol_map[label] = sobol_col_index
        sobol_col_index += 1
for klib_key in kinetics_database.libraries:
    kinetics_lib = kinetics_database.libraries[klib_key]
    for klib_entry_key in kinetics_lib.entries.keys():
        kinetics_lib_entry = kinetics_lib.entries[klib_entry_key]
        if kinetics_lib_entry.label in lib_entries_to_perturb:
            label = klib_key + '/' + str(klib_entry_key) + '/' + entry_key + '/' + kinetics_lib_entry.label
            sobol_map[label] = sobol_col_index
            sobol_col_index += 1


for klib_key in kinetics_database.libraries:
    kinetics_lib = kinetics_database.libraries[klib_key]
    for i in range(0, N):
        for klib_entry_key in kinetics_lib.entries.keys():
            kinetics_lib_entry = kinetics_lib.entries[klib_entry_key]
            for label in lib_entries_to_perturb:
                if kinetics_lib_entry.label == label:  # something madeup from the example
                    if kinetics_lib_entry.data.Ea.units != 'J/mol':
                        raise NotImplementedError('Not yet implemented for units other than J/mol')
                    Ea_ref = kinetics_lib_entry.data.Ea.value
                    sobol_key = klib_key + '/' + str(klib_entry_key) + '/' + entry_key + '/' + kinetics_lib_entry.label
                    sobol_col_index = sobol_map[sobol_key]
                    delta_E0 = (DELTA_E0_MAX - 2.0 * x_sobol[i, sobol_col_index] * DELTA_E0_MAX) * 1000.0  # convert from kJ/mol to J/mol
                    Ea_perturbed = Ea_ref + delta_E0
                    kinetics_lib_entry.data.Ea.value = Ea_perturbed
        kinetics_lib.save(os.path.join(kinetic_libraries_dir, klib_key, 'reactions_' + str(i).zfill(4) + '.py'))

for key in kinetics_database.families:
    family = kinetics_database.families[key]
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
            if entry[0].data.E0.units != 'kJ/mol':
                raise NotImplementedError('Not yet implemented for units other than kJ/mol')
            E0_ref = entry[0].data.E0.value
            sobol_key = family_key + '/' + entry_key + '/E0'
            sobol_col_index = sobol_map[sobol_key]
            delta_E0 = DELTA_E0_MAX - 2.0 * x_sobol[i, sobol_col_index] * DELTA_E0_MAX
            E0_perturbed = E0_ref + delta_E0
            entry[0].data.E0.value = E0_perturbed

        family.rules.save(os.path.join(families_dir, key, 'rules' + str(i).zfill(4) + '.py'))
