import os
import sys
import pandas as pd
import numpy as np
import yaml
import cantera as ct
from multiprocessing import Pool

# insert at 1, 0 is the script path (or '' in REPL)
# this is messy and should be revised when uncertainty analysis is a real package
sys.path.append( 
    '/work/westgroup/ChrisB/_01_MeOH_repos/uncertainty_analysis/uncertainty_cantera/Spinning_basket_reactor'
)
from sbr import MinSBR

cti_file_path = "/work/westgroup/ChrisB/_01_MeOH_repos/meOH-synthesis/base/cantera/chem_annotated.cti"
# cti_file_path = sys.argv[1]
rmg_model_folder = os.path.dirname(cti_file_path)
csv_path = os.path.join(rmg_model_folder, "ct_analysis.csv")


# generate settings array
settings_yaml = '/work/westgroup/ChrisB/_01_MeOH_repos/uncertainty_analysis/uncertainty_cantera/Spinning_basket_reactor/all_experiments_reorg_sbr.yaml'
with open(settings_yaml, 'r') as f:
    settings = yaml.safe_load(f)

def run_reactor(condts):

    # initialize reactor
    sbr_ss = MinSBR(
        cti_file_path,
        reac_config = condts,
        rtol=1.0e-11,
        atol=1.0e-22,
    )

    results = sbr_ss.run_reactor_ss_memory()
    return results


# Too much memory? is that why it's slow?
with Pool() as p:
    result = p.map(run_reactor, settings)

df = pd.DataFrame(result)
df.to_csv(csv_path)

# end = time.time()
# print(f"Completed {len(settings)} processes in {end-start} seconds")

# post process results after pool is finished running
# we will only use runs where intraparticle diffusion limitations
# are not an issue, i.e. T < 518K
df_graaf = df[(df['T (K)'] < 518) & (df['experiment'] == 'graaf_1988')]
obj_func = df_graaf['obj_func'].sum()
print("objective function: ", obj_func)

obj_func_log = df_graaf['log10(RMG/graaf) TOF'].sum()
print("objective function log: ", obj_func_log)

# this is naive, but currently saving the objective function to a text file 
# so we can parse all of them after. 
obj_func_file = os.path.join(rmg_model_folder, "objective_function.txt")
with open(obj_func_file, "w") as f:
    f.write(cti_file_path + ":" + str(obj_func))

# make log_obj_func file
obj_func_file_log = os.path.join(rmg_model_folder, "objective_function_log.txt")
with open(obj_func_file_log, "w") as f:
    f.write(cti_file_path + ":" + str(obj_func_log))