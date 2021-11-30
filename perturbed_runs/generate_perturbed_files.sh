#!/bin/bash
#SBATCH --job-name=perturb_params
#SBATCH --partition=west
#SBATCH --exclude=c5003

source activate rmg_julia_env
python-jl /scratch/westgroup/methanol/meOH-synthesis/perturbed_runs/generate_perturbed_files.py

