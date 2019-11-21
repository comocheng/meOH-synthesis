#!/bin/bash
#SBATCH --job-name=MeOH
#SBATCH --error=error.log
#SBATCH --output=output.log
#SBATCH -n1
#SBATCH --partition=west,general,gpu,interactive,test
#SBATCH --exclude=c5003
#SBATCH --mem=55Gb
#SBATCH --time=1:00:00

echo $RMGpy
python  $RMGpy/rmg.py -p input.py
