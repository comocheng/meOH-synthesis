#!/bin/bash
#SBATCH --job-name=perturb_params
#SBATCH --partition=west
#SBATCH --exclude=c5003
#SBATCH --error=error_be.log
#SBATCH --output=outputbe.log


source activate rmg_julia_env
python /scratch/westgroup/methanol/meOH-synthesis/perturbed_runs/generate_perturbed_BEs.py

