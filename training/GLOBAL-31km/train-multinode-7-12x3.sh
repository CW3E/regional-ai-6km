#!/bin/bash

#SBATCH --account=bduu-dtai-gh
#SBATCH --job-name=A2-7123
#SBATCH --partition=ghx4
#SBATCH --reservation=sup-11248-2
#SBATCH --mem=0
#SBATCH --nodes=16
#SBATCH --ntasks-per-node=4
#SBATCH --gpus-per-node=4
##SBATCH --cpus-per-task=4
#SBATCH --time=48:00:00
#SBATCH --output=./logs_sh/A2-7123_%j.log
#SBATCH --error=./logs_sh/A2-7123_%j.err

## Info here: https://docs.ncsa.illinois.edu/systems/deltaai/en/latest/user-guide/running-jobs.html

## Working directory
workdir=/work/hdd/bduu/jbanomedina/regional-ai/training/GLOBAL-31km/
cd ${workdir}


## Load conda environment
source /u/jbanomedina/miniconda3/etc/profile.d/conda.sh
conda activate /projects/bduu/jbanomedina/envs2/regional-ai

nodes=( $( scontrol show hostnames $SLURM_JOB_NODELIST ) )
nodes_array=($nodes)
head_node=${nodes_array[0]}
head_node_ip=$(srun --nodes=1 --ntasks=1 -w "$head_node" hostname -I | awk '{print $1}')
echo "Head node: $head_node"
echo "Head node IP: $head_node_ip"

## Load ncll
# export NCCL_DEBUG=INFO
# export NCCL_SOCKET_IFNAME=hsn
# module load nccl # loads the nccl built with the AWS nccl plugin for Slingshot11
# module list
echo "Job is starting on `hostname`"

# Check the Installed CUDA Version
nvcc --version

## Run script
srun anemoi-training train --config-name=config-2A-resume-7-12x3.yaml

 
## Estimate number of iterations to update the scheduler in rollout 1-12 (stage A2)
# import pandas as pd
# # Define the start and end dates
# start_date = "2012-09-01"
# end_date = "2020-04-01"
# # Create a date range with hourly frequency, but we only want values at 0, 6, 12, and 18 UTC
# date_range = pd.date_range(start=start_date, end=end_date, freq='6H')
# # Count the number of samples
# num_samples = len(date_range)
# print(num_samples)
# num_iterations = num_samples/16
# print(num_iterations)