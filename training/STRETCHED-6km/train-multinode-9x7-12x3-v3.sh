#!/bin/bash

#SBATCH --account=bduu-dtai-gh
#SBATCH --job-name=B2-v3-2
#SBATCH --partition=ghx4
#SBATCH --reservation=sup-11248
#SBATCH --mem=0
#SBATCH --nodes=16
#SBATCH --ntasks-per-node=4
#SBATCH --gpus-per-node=4
##SBATCH --cpus-per-task=4
#SBATCH --time=48:00:00
#SBATCH --output=./logs_sh/B2-v3-2_%j.log
#SBATCH --error=./logs_sh/B2-v3-2_%j.err

## Info here: https://docs.ncsa.illinois.edu/systems/deltaai/en/latest/user-guide/running-jobs.html

## Working directory
workdir=/work/hdd/bduu/jbanomedina/regional-ai/training/STRETCHED-6km/
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
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True,garbage_collection_threshold:0.8

# Check the Installed CUDA Version
nvcc --version

## Run script
srun anemoi-training train --config-name=config-B2-resume-9x7-12x3-v3-2.yaml

 

