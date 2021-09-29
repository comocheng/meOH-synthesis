#!/bin/bash
#SBATCH --job-name=rmg_runs_0-19.sh
#SBATCH --error=error0.log
#SBATCH --output=output0.log
#SBATCH --nodes=1
#SBATCH --partition=west,short
#SBATCH --exclude=c5003
#SBATCH --mem=8Gb
#SBATCH --time=1:00:00
#SBATCH --cpus-per-task=4


# Copy the files from the full database to the mostly symbolic one
python /scratch/westgroup/methanol/meOH-synthesis/perturbed_runs/make_slurm_scripts.py



