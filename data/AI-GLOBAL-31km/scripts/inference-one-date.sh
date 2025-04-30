#!/bin/bash

#SBATCH --account=bduu-dtai-gh
#SBATCH --job-name=test
#SBATCH --partition=ghx4
#SBATCH --mem=0
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=1
##SBATCH --cpus-per-task=8
#SBATCH --time=00:05:00
#SBATCH --output=../logs/test_%j.log
#SBATCH --error=../logs/test_%j.err

## Info here: https://docs.ncsa.illinois.edu/systems/deltaai/en/latest/user-guide/running-jobs.html

## Working directory
workdir=/work/nvme/bduu/jbanomedina/regional-ai/data/GLOBAL-31km/scripts/
cd ${workdir}

## Load conda environment
source /u/jbanomedina/miniconda3/etc/profile.d/conda.sh
conda activate /projects/bduu/jbanomedina/envs2/regional-ai

## Parameters
lead_time=174 # 10-hour forecast
epoch=45
# vars=2t,z_1000,tp,ivt
vars=$(paste -sd, < list-vars.txt)
input=test
date=2020-11-01T00:00:00
stage=A1

## Path 4-km lats and lons to interpolate outputs to PRISM
lats_path=../../latsCoords_2kmDomain.npy 
lons_path=../../lonsCoords_2kmDomain.npy

## Create directory in case it does not exist
mkdir -p ../outputs/epoch-$epoch/
mkdir -p ../outputs/epoch-$epoch/31km/
mkdir -p ../outputs/epoch-$epoch/4km-prism/

## Run script anemoi inference
anemoi-inference run config.yaml \
    date=$date \
    input=$input \
    checkpoint=../../../models/GLOBAL-31km/epoch-$epoch/inference/$stage-epoch$epoch.ckpt \
    lead_time=$lead_time

## Post-process (e.g., subset variables of interest, compute ivt and interpolate to 4km-prism). 
python postprocess-anemoi-output.py \
    ../outputs/epoch-$epoch/ \
    $date \
    $lead_time \
    $vars \
    $lats_path \
    $lons_path 
