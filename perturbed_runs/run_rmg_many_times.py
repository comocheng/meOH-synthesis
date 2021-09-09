# script to do the 5000 RMG runs on discovery
# Sevy Harris 9/8/2021

import numpy as np
import job_manager
import os
import glob


working_dir = "/scratch/westgroup/methanol/perturb_5000/"
# working_dir = "/home/moon/rmg/fake_rmg_runs/"
if not os.path.exists(working_dir):
    os.mkdir(working_dir)


# reference_db = "/home/moon/rmg/RMG-database/"
reference_db = "/scratch/westgroup/methanol/perturb_5000/RMG-database/"
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
    range_max = np.amin([i + N, M])
    last_index = range_max - 1
    job_indices = [a for a in range(i, range_max)]
    print(f'{sbatch_index}: running jobs {job_indices}')

    # Write the job file
    fname = f'rmg_runs_{i}-{last_index}.sh'
    jobfile = job_manager.SlurmJobFile(full_path=os.path.join(working_dir, fname))
    jobfile.settings['--array'] = f'{i}-{last_index}'
    jobfile.settings['--job-name'] = fname
    jobfile.settings['--error'] = f'error{sbatch_index}.log'
    jobfile.settings['--output'] = f'output{sbatch_index}.log'

    content = ['# Copy the files from the full database to the mostly symbolic one\n']

    content.append('RUN_i=$(printf "%04.0f" $SLURM_ARRAY_TASK_ID)\n')
    content.append(f'DATABASE_n=$(printf "%04.0f" $(($SLURM_ARRAY_TASK_ID % {N})))\n')
    for rule_file in perturbed_kinetics_rules:
        # TODO convert array job id to rmg run i and database N
        # $SLURM_ARRAY_JOB_ID
        rule_file_src = rule_file.replace('rules0000.py', 'rules${RUN_i}.py')
        file_name_parts = rule_file.split('RMG-database/')
        if len(file_name_parts) != 2:
            raise OSError(f'Bad source rules.py file path {rule_file}')
        rule_file_dest = os.path.join(working_dir, 'db_' + '${DATABASE_n}', file_name_parts[1].replace('rules0000.py', 'rules.py'))
        content.append(f'cp "{rule_file_src}" "{rule_file_dest}"\n')
        break
    # For each perturbed parameter, copy it from the reference database to the Nth symbolic one.
    content.append('\n')
    jobfile.content = content
    

    # make the directory for the rmg run
    #rmg_run_dir = os.path.join(working_dir, "run"
    #content.append(f'mkdir "{workin}"')
    
    jobfile.write_file()
    # copy the N sets of files to their respective databases - this should probably be part of the bash script
    
    # Create the RMGfolder -- do this in bash
