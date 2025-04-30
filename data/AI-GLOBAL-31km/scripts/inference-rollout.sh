#!/bin/bash

#SBATCH --account=bduu-dtai-gh
#SBATCH --job-name=B2-rollout
#SBATCH --partition=ghx4
##SBATCH --reservation=sup-11248-2
#SBATCH --mem=0
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=1
##SBATCH --cpus-per-task=8
#SBATCH --time=12:00:00
#SBATCH --output=../logs/pred-31km_%j.log
#SBATCH --error=../logs/pred-31km_%j.err
#SBATCH --array=0-1

## Info here: https://docs.ncsa.illinois.edu/systems/deltaai/en/latest/user-guide/running-jobs.html

## Working directory
workdir=/work/nvme/bduu/jbanomedina/regional-ai/data/GLOBAL-31km/scripts/
cd ${workdir}

## Load conda environment
source /u/jbanomedina/miniconda3/etc/profile.d/conda.sh
conda activate /projects/bduu/jbanomedina/envs2/regional-ai

## Parameters
lead_time=174 # 10-hour forecast
vars=tp,ivt
# vars=$(paste -sd, < list-vars.txt)
input=test
stage=A2

# Define the list of epochs
epochs=(79 80 82 83 84 85 86 87 88 89 90)
epoch=${epochs[$SLURM_ARRAY_TASK_ID]}

## Path 4-km lats and lons to interpolate outputs to PRISM
lats_path=../../latsCoords_2kmDomain.npy 
lons_path=../../lonsCoords_2kmDomain.npy

## Generate list of dates based on the above parameters
init_interval=24
# Last date not included as per Python way to generate lists
python generate-dates-txt.py 2020-11-01T00 2021-04-01T00 $init_interval list-dates-2021.txt # Winter 20-21
python generate-dates-txt.py 2021-11-01T00 2022-04-01T00 $init_interval list-dates-2022.txt # Winter 21-22
python generate-dates-txt.py 2022-11-01T00 2023-04-01T00 $init_interval list-dates-2023.txt # Winter 22-23
python merge_list_dates_txt.py list-dates-2021.txt list-dates-2022.txt list-dates-223.txt  # Concatenate winters
# rm list-dates-2021.txt list-dates-2022.txt list-dates-2023.txt
dates=$(<list-dates.txt)

## Create directory in case it does not exist
mkdir -p ../outputs/epoch-$epoch/
mkdir -p ../outputs/epoch-$epoch/31km/
mkdir -p ../outputs/epoch-$epoch/4km-prism/

## Loop over the initial conditions 
for date in $dates; do
    
    ## Information about forecast
    echo "Running GLOBAL model (31km) at EPOCH $epoch to generate a $lead_time-hour forecast with initial condition: $date ($input set)"

    ## Run script anemoi inference
    anemoi-inference run config.yaml \
     date=$date \
     input=$input \
     checkpoint=../../../models/GLOBAL-31km/epoch-$epoch/inference/$stage-epoch$epoch.ckpt \
     lead_time=$lead_time \
     output.netcdf=../outputs/temp-$epoch.nc

    ## Post-process (e.g., subset variables of interest, compute ivt and interpolate to 4km-prism). 
    python postprocess-anemoi-output.py \
     ../outputs/epoch-$epoch/ \
     $date \
     $lead_time \
     $vars \
     $lats_path \
     $lons_path \
     ../outputs/temp-$epoch.nc

    ## Delete temporary file
    rm ../outputs/temp-$epoch.nc

done

## Remove list of dates
# rm list-dates.txt

