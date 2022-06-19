#!/bin/sh
#
#SBATCH --job-name="summary"
#SBATCH --partition=compute
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=10G
#SBATCH --output=/dev/null
#SBATCH --error=/dev/null

module load 2022r1 
module load compute
module load python/3.8.12-p6aunbm
module load py-numpy

#srun  python /home/mghorn/mlbp/summary.py /scratch/mghorn/20220530/data/* > /scratch/mghorn/20220530/20220530.sum 2> /scratch/mghorn/20220530/20220530.err
srun python $1 $2 > $3 2> $4

