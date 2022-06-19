#!/bin/sh
#
#SBATCH --job-name="test"
#SBATCH --partition=compute
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=10G
#SBATCH --output=/dev/null

LINE=$(( $2 + ${SLURM_ARRAY_TASK_ID} ))
CMD=$(sed -n ${LINE}p $1)
#echo ${CMD}
eval "srun ${CMD}"
