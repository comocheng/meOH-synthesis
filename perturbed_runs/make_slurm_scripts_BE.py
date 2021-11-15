# script to do the 5000 RMG runs on discovery
# Sevy Harris 9/8/2021

import numpy as np
import job_manager
import os
import glob


# WARNING - this will fail if M%N != 0


skip_completed_runs = False # set to false to overwrite RMG runs that completed

working_dir = "/scratch/westgroup/methanol/perturb_5000/"
# working_dir = "/home/moon/rmg/fake_rmg_runs/"
if not os.path.exists(working_dir):
    os.mkdir(working_dir)


# reference_db = "/home/moon/rmg/RMG-database/"
reference_db = "/scratch/westgroup/methanol/perturb_5000/RMG-database/"
if not os.path.exists(reference_db):
    raise OSError(f"Reference database does not exist {reference_db}")

reference_input = "/scratch/westgroup/methanol/meOH-synthesis/perturbed_runs/input.py"
if not os.path.exists(reference_input):
    raise OSError(f"Cannot find reference rmg input.py file {reference_input}")

# Find all of the files that have been copied 5000 times
perturbed_kinetics_rules = glob.glob(os.path.join(reference_db, 'input', 'kinetics', 'families', '*/rules_0000.py'))
perturbed_thermo = glob.glob(os.path.join(reference_db, 'input', 'thermo', 'libraries', '*_0000.py'))
perturbed_kinetics_libs = glob.glob(os.path.join(reference_db, 'input', 'kinetics', 'libraries', '*_0000.py'))
perturbed_thermo_groups = glob.glob(os.path.join(reference_db, 'input', 'thermo', 'groups', '*_0000.py'))


M = 5000  # total number of times to run RMG
N = 50  # number of jobs to run at a time
for i in range(0, M, N):
    sbatch_index = int(i / N)
    range_max = np.amin([i + N, M])
    last_index = range_max - 1
    job_indices = [a for a in range(i, range_max)]
    # print(f'{sbatch_index}: running jobs {job_indices}')

    # max slurm array index is 1000, so after that, subtract multiples of 1000
    task_id_offset = int(i/1000) * 1000
    
    # Write the job file
    fname = f'rmg_runs_{i}-{last_index}.sh'
    jobfile = job_manager.SlurmJobFile(full_path=os.path.join(working_dir, "rmg_run_scripts", fname))
    jobfile.settings['--array'] = f'{i - task_id_offset}-{last_index - task_id_offset}'
    jobfile.settings['--job-name'] = fname
    jobfile.settings['--error'] = os.path.join(working_dir, f'error{sbatch_index}.log')
    jobfile.settings['--output'] = os.path.join(working_dir, f'output{sbatch_index}.log')
    jobfile.settings['--mem'] = f'20Gb'

    content = ['# Define useful bash variables\n']

    
    content.append(f'SLURM_TASK_ID_OFFSET={task_id_offset}\n')
    content.append('RUN_i=$(printf "%04.0f" $(($SLURM_ARRAY_TASK_ID + $SLURM_TASK_ID_OFFSET)))\n')
    rmg_run_dir = os.path.join(working_dir, "run_${RUN_i}")
    
    # content.append(f'DATABASE_n=$(printf "%04.0f" $(($(($SLURM_ARRAY_TASK_ID + $SLURM_TASK_ID_OFFSET)) % {N})))\n')
    
    # skip if RMG already ran and not the force option
    if skip_completed_runs:
        content.append('match_str="MODEL GENERATION COMPLETED"\n')
        RMG_log = os.path.join(rmg_run_dir, 'RMG.log')
        content.append(f'completion_status=$(cat {RMG_log} | grep "$match_str")\n')
        content.append('if [ "$completion_status" == "$match_str" ];\n')
        content.append('then echo "skipping completed run ${RUN_i}"; exit 0\n')
        content.append('fi\n\n')
    
    # make the directory for the rmg run
    content.append('# Prepare the directory for the RMG run\n')
    content.append(f'mkdir "{rmg_run_dir}"\n')
    
    # copy the RMG input file
    # dest_input_file = os.path.join(rmg_run_dir, "input.py")
    # content.append(f'cp "{reference_input}" "{dest_input_file}"\n')
 
    # make the RMGRC file
    # content.append(f'echo "database.directory {dest_db_dir}/input/" > "{rmg_run_dir}/rmgrc"\n')

    # run RMG
    content.append('# Run RMG\n')
    content.append(f'cd {rmg_run_dir} \n')
    # content.append(f'if RMG_RUN COMPLETED {rmg_run_dir} \n')

   
    # aliasing "rmg" to "source activate <whatever your rmg env is>"
    content.append(f'rmg\n')
    # adding in environment variable for $RMG to the RMG-Py/rmg.py in bashrc so we don't have to change path
    content.append(f'python-jl $RMG input_BE.py\n')
    #content.append(f'python /scratch/westgroup/methanol/perturb_5000/RMG-Py/rmg.py {rmg_run_dir}/input.py\n')

    jobfile.content = content
    jobfile.write_file()
   
 
