###############################################################################
# Sevy Harris 2021-09-02
# This script takes a handful of kinetics families, kinetics libraries, and
# thermo libraries and perturbs the E0, alpha, and Ea values
# Based off of Bjarne's Parametric Uncertainty Paper 10.1021/jacsau.1c00276
###############################################################################

import os
import copy
from torch.quasirandom import SobolEngine
from rmgpy.data.kinetics.database import KineticsDatabase
from rmgpy.molecule import Molecule
from rmgpy.data.thermo import ThermoDatabase
from rmgpy import constants
from tqdm import tqdm  # this is for the progress bar cause copying stuff takes a while


# WARNING - right now you need to copy this to /scratch/westgroup/methanol/perturb_5000/RMG-Py and run from there


# Define the uncertainty ranges based on the paper
DELTA_ALPHA_MAX = 0.15
# DELTA_E0_MAX = 30  # 3 eV is about 30 kJ/mol
DELTA_E0_MAX_J_MOL = 30000  # 3 eV is about 30000 J/mol

# Define the number of perturbations to run
N = 10

# Create the pseudo randoms
# number of params by # of runs in aggregate. 
sobol = SobolEngine(dimension=80, scramble=True, seed=100)
x_sobol = sobol.draw(N)


# Specify the path to the families
# families_dir = "/scratch/westgroup/methanol/perturb_5000/RMG-database/input/kinetics/families/"
# if not os.path.exists(families_dir):
#     raise OSError(f'Path to rules does not exist:\n{families_dir}')

# # Specify the path to the libraries
# kinetic_libraries_dir = "/scratch/westgroup/methanol/perturb_5000/RMG-database/input/kinetics/libraries/Surface/"
# if not os.path.exists(kinetic_libraries_dir):
#     raise OSError(f'Path to kinetic libraries does not exist:\n{kinetic_libraries_dir}')

# Specify the path to the thermo library
library_path = "/home/blais.ch/_02_RMG_envs/meoh_h2_rmg/RMG-database/input/thermo/"
if not os.path.exists(library_path):
    raise OSError(f'Path to rules does not exist:\n{library_path}')

# # Load the databases
# kinetics_database = KineticsDatabase()
# kinetics_database.load_families(
#     path=families_dir,
#     families=[  # list the families to perturb
#         'Surface_Dissociation',
#         'Surface_Dissociation_Beta',
#         'Surface_Abstraction',
#         'Surface_Abstraction_Beta',
#         'Surface_Adsorption_Dissociative',
#         'Surface_Dissociation_vdW',
#         # These aren't recognized
#         # 'Surface_Dissociation_Double',
#         # 'Surface_Dissociation_Beta_vdW',
#         # 'Surface_Abstraction_Beta_Dual_vdW',
#         # 'Surface_Abstraction_Beta_vdW',
#         #
#         # This was the only substitute I could find
#         'Surface_Abstraction_Beta_double_vdW',
#     ],
# )

# kinetics_database.load_libraries(
#     kinetic_libraries_dir,
#     libraries=[
#         'Example',  # just checking if this connects
#         #'Ni111',
#     ]
# )
thermo_database = ThermoDatabase()
thermo_database.load(
    library_path,
    libraries=[
        'surfaceThermoCu111',
        'surfaceThermoPt111',
        # 'surfaceThermoPt_H',
        # 'surfaceThermoPt_O',
        # 'surfaceThermoPt_vdW',
    ],
    depository=False,
    surface=True)

# pick which entries to perturb in the kinetics library
# WARNING: does not handle overlap of entries in different libraries
# lib_entries_to_perturb = [
#     # "OCX + OX <=> CO2 + Ni + Ni",
#     "CO2X + Ni <=> OCX + OX",
# ]

# make the map of sobol columns
sobol_map = {}
sobol_col_index = 0
# for family_key in kinetics_database.families:
#     family = kinetics_database.families[family_key]
#     for entry_key in family.rules.entries.keys():
#         label = family_key + '/' + entry_key + '/alpha'
#         sobol_map[label] = sobol_col_index
#         sobol_col_index += 1
#         label = family_key + '/' + entry_key + '/E0'
#         sobol_map[label] = sobol_col_index
#         sobol_col_index += 1
# for klib_key in kinetics_database.libraries:
#     kinetics_lib = kinetics_database.libraries[klib_key]
#     for klib_entry_key in kinetics_lib.entries.keys():
#         kinetics_lib_entry = kinetics_lib.entries[klib_entry_key]
#         if kinetics_lib_entry.label in lib_entries_to_perturb:
#             label = klib_key + '/' + str(klib_entry_key) + '/' + entry_key + '/' + kinetics_lib_entry.label
#             sobol_map[label] = sobol_col_index
#             sobol_col_index += 1
for library_key in thermo_database.libraries:
    label = library_key + '/E0'
    sobol_map[label] = sobol_col_index
    sobol_col_index += 1


# # Perturb the values in the kinetics library
# print("Creating kinetics library files")
# for klib_key in kinetics_database.libraries:
#     kinetics_lib = kinetics_database.libraries[klib_key]
#     kinetics_lib_ref = copy.deepcopy(kinetics_lib)
#     for i in tqdm(range(0, N)):
#         for klib_entry_key in kinetics_lib.entries.keys():
#             kinetics_lib_entry = kinetics_lib.entries[klib_entry_key]
#             for label in lib_entries_to_perturb:
#                 if kinetics_lib_entry.label == label:  # something madeup from the example
#                     # if kinetics_lib_entry.data.Ea.units != 'J/mol':
#                     #    raise NotImplementedError('Not yet implemented for units other than J/mol')
#                     Ea_ref = kinetics_lib_ref.entries[klib_entry_key].data.Ea.value_si
#                     sobol_key = klib_key + '/' + str(klib_entry_key) + '/' + entry_key + '/' + kinetics_lib_entry.label
#                     sobol_col_index = sobol_map[sobol_key]
#                     # delta_E0 = (DELTA_E0_MAX - 2.0 * x_sobol[i, sobol_col_index] * DELTA_E0_MAX) * 1000.0  # convert from kJ/mol to J/mol
#                     delta_E0 = (DELTA_E0_MAX_J_MOL - 2.0 * x_sobol[i, sobol_col_index] * DELTA_E0_MAX_J_MOL)
#                     Ea_perturbed = Ea_ref + delta_E0
#                     kinetics_lib_entry.data.Ea.value_si = Ea_perturbed
#         kinetics_lib.save(os.path.join(kinetic_libraries_dir, klib_key, 'reactions_' + str(i).zfill(4) + '.py'))

# # Perturb the values in the kinetics families
# print("Generating kinetics family files")
# for family_key in kinetics_database.families:
#     family = kinetics_database.families[family_key]
#     family_ref = copy.deepcopy(family)
#     for i in tqdm(range(0, N)):
#         for entry_key in family.rules.entries.keys():
#             entry = family.rules.entries[entry_key]

#             # Perturb the alpha value
#             alpha_ref = family_ref.rules.entries[entry_key][0].data.alpha.value
#             sobol_key = family_key + '/' + entry_key + '/alpha'
#             sobol_col_index = sobol_map[sobol_key]
#             delta_alpha = DELTA_ALPHA_MAX - 2.0 * x_sobol[i, sobol_col_index] * DELTA_ALPHA_MAX
#             alpha_perturbed = alpha_ref + delta_alpha
#             # TODO check that alpha is unitless
#             entry[0].data.alpha.value = alpha_perturbed

#             # Perturb the E0 value
#             # if entry[0].data.E0.units != 'kJ/mol':
#             #    print(f'units: {entry[0].data.E0.units}')
#             #    print(f'value: {entry[0].data.E0.value}')
#             #    print(f'value_si: {entry[0].data.E0.value_si}')
#             #    raise NotImplementedError('Not yet implemented for units other than kJ/mol')
#             E0_ref = family_ref.rules.entries[entry_key][0].data.E0.value_si
#             sobol_key = family_key + '/' + entry_key + '/E0'
#             sobol_col_index = sobol_map[sobol_key]
#             delta_E0 = DELTA_E0_MAX_J_MOL - 2.0 * x_sobol[i, sobol_col_index] * DELTA_E0_MAX_J_MOL
#             E0_perturbed = E0_ref + delta_E0
#             entry[0].data.E0.value_si = E0_perturbed

#         family.rules.save(os.path.join(families_dir, family_key, 'rules_' + str(i).zfill(4) + '.py'))

# Create the thermo files
print("generating thermo files")
for library_key in thermo_database.libraries:
    thermo_lib = thermo_database.libraries[library_key]
    thermo_lib_ref = copy.deepcopy(thermo_lib)
    sobol_key = library_key + '/E0'
    sobol_col_index = sobol_map[sobol_key]

    for i in tqdm(range(0, N)):
        delta_E0 = DELTA_E0_MAX_J_MOL - 2.0 * x_sobol[i, sobol_col_index] * DELTA_E0_MAX_J_MOL

        for entry_key in thermo_lib.entries.keys():
            entry = thermo_lib.entries[entry_key]
            # Don't perturb the energy level if it's just a vacant site
            if entry_key is 'vacant':
                continue
            if entry.item.is_isomorphic(Molecule().from_adjacency_list("1 X  u0 p0 c0")):
                continue

            # Perturb the E0 value, which is a5 in the NASA polymial

            # check units for NASA in RMG. 
            if entry.data.poly1 is not None:
                E0_ref = thermo_lib_ref.entries[entry_key].data.poly1.c5
                E0_perturbed = E0_ref + delta_E0 / (constants.R / 1000.0)  # 8.314e-3
                E0_perturbed = E0_ref + delta_E0 / constants.R  # 8.314
                entry.data.poly1.c5 = E0_perturbed
            if entry.data.poly2 is not None:
                E0_ref = thermo_lib_ref.entries[entry_key].data.poly2.c5
                E0_perturbed = E0_ref + delta_E0 / constants.R  # 8.314
                entry.data.poly2.c5 = E0_perturbed
            if entry.data.poly3 is not None:
                E0_ref = thermo_lib_ref.entries[entry_key].data.poly3.c5
                E0_perturbed = E0_ref + delta_E0 / constants.R  # 8.314
                entry.data.poly3.c5 = E0_perturbed

        thermo_lib.save(os.path.join(library_path, 'libraries', library_key + '_' + str(i).zfill(4) + '.py'))