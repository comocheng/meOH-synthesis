import job_manager
import time
import glob
import os


working_dir = "/scratch/westgroup/methanol/perturb_5000/"

print("Collecting SLURM scripts")
slurm_scripts = glob.glob(os.path.join(working_dir, "rmg_runs_*.sh"))

print("Running job 0")

rmg_job = job_manager.SlurmJob()
my_cmd = f'sbatch "{slurm_scripts[0]}"'
rmg_job.submit(my_cmd)

#practice_job.submit(my_cmd)
#time.sleep(3)
#if practice_job.completed():
#    print("practice job has completed")
#else:
#    print(f'practice job is {practice_job.status}')

#print(slurm_scripts)

