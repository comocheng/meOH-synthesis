#!/bin/bash
#SBATCH --job-name=perturb_params
#SBATCH --partition=west
#SBATCH --exclude=c5003


python /scratch/westgroup/methanol/meOH-synthesis/perturbed_runs/generate_perturbed_files.py

