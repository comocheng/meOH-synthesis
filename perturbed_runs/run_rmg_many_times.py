# script to do the 5000 RMG runs on discovery
# Sevy Harris 9/8/2021

import numpy as np
import job_manager
import os
import glob


# working_dir = "/scratch/westgroup/methanol/perturb5000/"
working_dir = "/home/moon/rmg/fake_rmg_runs/"
if not os.path.exists(working_dir):
    os.mkdir(working_dir)


reference_db = "/home/moon/rmg/RMG-database/"
if not os.path.exists(reference_db):
    raise OSError(f"Reference database does not exist {reference_db}")

# Find all of the files that have been copied 5000 times
perturbed_kinetics_rules = glob.glob(os.path.join(reference_db, 'input', 'kinetics', 'families', '*/rules0000.py'))
perturbed_thermo = glob.glob(os.path.join(reference_db, 'input', 'thermo', 'libraries', '*_0000.py'))
perturbed_kinetics_libs = glob.glob(os.path.join(reference_db, 'input', 'kinetics', 'libraries', '*_0000.py'))


M = 25  # total number of times to run RMG
N = 20  # number of jobs to run at a time
for i in range(0, M, N):
    sbatch_index = int(i / N)
    last_index = np.amin([i + N, M])
    job_indices = [a for a in range(i, last_index)]
    print(f'{sbatch_index}: running jobs {job_indices}')

    # Write the job file
    fname = f'rmg_runs_{i}-{last_index}.sh'
    jobfile = job_manager.SlurmJobFile(full_path=os.path.join(working_dir, fname))
    jobfile.settings['--array'] = f'{i}-{last_index}'
    jobfile.settings['--job-name'] = fname
    jobfile.settings['--error'] = f'error{sbatch_index}.log'
    jobfile.settings['--output'] = f'output{sbatch_index}.log'

    content = ['# Copy the files from the full database to the mostly symbolic one\n']

    for rule_file in perturbed_kinetics_rules:
        # TODO convert array job id to rmg run i and database N
        # $SLURM_ARRAY_JOB_ID
        rule_file_src = rule_file
        rule_file_dest = os.path.join(working_dir, 'db_' + "$(($SLURM_ARRAY_JOB_ID))")
        content.append('cp {rule_file_src} {rule_file_dest}')
    # For each perturbed parameter, copy it from the reference database to the Nth symbolic one.

    jobfile.content = content
    jobfile.write_file()
    # create an arrayjob to run RMG N times
    # copy the N sets of files to their respective databases - this should probably be part of the bash script

    # Create the RMGfolder -- do this in bash
