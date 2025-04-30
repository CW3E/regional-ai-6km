#!/bin/bash

#SBATCH --account=bduu-dtai-gh
#SBATCH --job-name=v3
#SBATCH --partition=ghx4
#SBATCH --reservation=sup-11248
#SBATCH --mem=0
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=1
##SBATCH --cpus-per-task=8
#SBATCH --time=48:00:00
#SBATCH --output=../logs/v3_%j.log
#SBATCH --error=../logs/v3_%j.err

## Info here: https://docs.ncsa.illinois.edu/systems/deltaai/en/latest/user-guide/running-jobs.html

## Working directory
workdir=/work/nvme/bduu/jbanomedina/regional-ai/data/STRETCHED-6km-v3/scripts/
cd ${workdir}

## Load conda environment
source /u/jbanomedina/miniconda3/etc/profile.d/conda.sh
conda activate /projects/bduu/jbanomedina/envs2/regional-ai

## Parameters
lead_time=174 # 10-hour forecast
epoch=40
stage=B2
version=v3
vars=2t,z_1000,sp,msl,tp,10u,10v,ivt,iwv
# vars=$(paste -sd, < list-vars.txt)

## Path 4-km lats and lons to interpolate outputs to PRISM
lats_path=../../latsCoords_2kmDomain.npy 
lons_path=../../lonsCoords_2kmDomain.npy

## Generate list of dates based on the above parameters
init_interval=24
# Last date not included as per Python way to generate lists
# python generate-dates-txt.py 2020-11-01T00 2021-04-01T00 $init_interval list-dates-2021.txt # Winter 20-21
# python generate-dates-txt.py 2021-11-01T00 2022-04-01T00 $init_interval list-dates-2022.txt # Winter 21-22
# python generate-dates-txt.py 2022-11-01T00 2023-04-01T00 $init_interval list-dates-2023.txt # Winter 22-23
# python merge_list_dates_txt.py list-dates-2021.txt list-dates-2022.txt list-dates-2023.txt  # Concatenate winters
# rm list-dates-2021.txt list-dates-2022.txt list-dates-2023.txt
dates=$(<list-dates.txt)

## Create directory in case it does not exist
mkdir -p ../outputs/epoch-$epoch/
mkdir -p ../outputs/epoch-$epoch/6km/
# mkdir -p ../outputs/epoch-$epoch/4km-prism/

## Loop over the initial conditions 
for date in $dates; do

    ## Output file
    file_found=false
    for winter_season in 20-21 21-22 22-23; do
        file="../outputs/epoch-$epoch/6km/$winter_season/tp_${date:0:13}.nc"
        if [ -f "$file" ]; then
            echo "File found: $file"
            file_found=true
        fi
    done

    # There is a bug in anemoi-inference. ALTERNATIVE: Python script below.
    if ! $file_found; then
        ## Information about forecast
        echo "Running STRETCHED model (6km) at EPOCH $epoch to generate a $lead_time-hour forecast with initial condition: $date." 

        python runner_stretched.py \
        $epoch \
        $date \
        $lead_time \
        $stage \
        $version

        ## Post-process (e.g., subset variables of interest, compute ivt and interpolate to 4km-prism). 
        python postprocess-anemoi-output.py \
        ../outputs/epoch-$epoch/ \
        $date \
        $lead_time \
        $vars \
        $lats_path \
        $lons_path \
        ../outputs/epoch-$epoch/temp.nc
        
        ## Delete temporary file
        rm ../outputs/epoch-$epoch/temp.nc
    fi
done

## Remove list of dates
# rm list-dates.txt

