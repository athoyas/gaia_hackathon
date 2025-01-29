#!/bin/bash
#
#SBATCH --job-name=test
#SBATCH --output=/work/submit/athoyas/results/res_%j.txt
#SBATCH --error=/work/submit/athoyas/results/err_%j.txt
#
#SBATCH --time=10:00


python3 find_rot_vel.py