#!/bin/bash
cd tol_5e-1
sbatch run.sh
cd ../tol_1e-1
sbatch run.sh
cd ../tol_1e-2
sbatch run.sh
cd ../tol_1e-3
sbatch run.sh
cd ../tol_1e-4
sbatch run.sh
cd ../tol_1e-5
sbatch run.sh