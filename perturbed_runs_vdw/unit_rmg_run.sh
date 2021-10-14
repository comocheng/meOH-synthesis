#!/bin/bash
#SBATCH --job-name=practice_job          <-----
#SBATCH --error=error.log
#SBATCH --output=output.log
#SBATCH --nodes=1
#SBATCH --partition=west,short
#SBATCH --exclude=c5003
#SBATCH --mem=20Gb
#SBATCH --time=1:00:00
#SBATCH --cpus-per-task=4
#SBATCH --ntasks=1
#SBATCH --array=1-20                     <-----

echo "Running perturbation i on database n"
# where n is the array number and i is the perturbation number

# copy files from perturbation i into database n

# run rmg
echo "$SLURM_ARRAY_JOB_ID:$SLURM_ARRAY_TASK_ID" > "$SLURM_ARRAY_TASK_ID.txt"
