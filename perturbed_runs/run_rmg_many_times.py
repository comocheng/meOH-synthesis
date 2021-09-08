# script to do the 5000 RMG runs on discovery
# Sevy Harris 9/8/2021

import numpy as np
import job_manager
import os


# working_dir = "/scratch/westgroup/methanol/perturb5000/"
working_dir = "/home/moon/rmg/fake_rmg_runs/"
if not os.path.exists(working_dir):
    os.mkdir(working_dir)

M = 25  # total number of times to run RMG
N = 20  # number of jobs to run at a time
for i in range(0, M, N):
    last_index = np.amin([i + N, M])
    job_indices = [a for a in range(i, last_index)]
    print(f'running jobs {job_indices}')

    # Write the job file -- this should probably be part of the job manager...
    slurm_job_file = open(os.path.join(working_dir, f'slurm_array_{i}-{last_index}.sh'), "w")
    slurm_job_file.close()

    # create an arrayjob to run RMG N times
    # copy the N sets of files to their respective databases - this should probably be part of the bash script

    # Create the RMGfolder -- do this in bash
