#!/bin/bash
#SBATCH --job-name=MeOH
#SBATCH --error=error.log
#SBATCH --output=output.log
#SBATCH --nodes=1
#SBATCH --partition=west,short
#SBATCH --exclude=c5003
#SBATCH --mem=20Gb
#SBATCH --time=1:00:00
#SBATCH --cpus-per-task=4
#SBATCH --ntasks=1

source activate rmg_env
echo $RMGpy
python  $RMGpy/rmg.py -p input.py
