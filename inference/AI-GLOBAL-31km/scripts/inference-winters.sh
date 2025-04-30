################ LICENSE ######################################
# This software is Copyright © 2025 The Regents of the University of California.
# All Rights Reserved. Permission to copy, modify, and distribute this software and its documentation
# for educational, research and non-profit purposes, without fee, and without a written agreement is
# hereby granted, provided that the above copyright notice, this paragraph and the following three paragraphs
# appear in all copies. Permission to make commercial use of this software may be obtained by contacting:
#
# Office of Innovation and Commercialization 9500 Gilman Drive, Mail Code 0910 University of California La Jolla, CA 92093-0910 innovation@ucsd.edu
# This software program and documentation are copyrighted by The Regents of the University of California. The software program and documentation are
# supplied “as is”, without any accompanying services from The Regents. The Regents does not warrant that the operation of the program will
# be uninterrupted or error-free. The end-user understands that the program was developed for research purposes and is advised not to rely exclusively on the program for any reason.
#
# IN NO EVENT SHALL THE UNIVERSITY OF CALIFORNIA BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
# INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE
# AND ITS DOCUMENTATION, EVEN IF THE UNIVERSITY OF CALIFORNIA HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE. THE UNIVERSITY OF CALIFORNIA SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER
# IS ON AN “AS IS” BASIS, AND THE UNIVERSITY OF CALIFORNIA HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT,
# UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
################################################################

#!/bin/bash

#SBATCH --account=bduu-dtai-gh
#SBATCH --job-name=pred-31km
#SBATCH --partition=ghx4
#SBATCH --mem=0
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=1
##SBATCH --cpus-per-task=8
#SBATCH --time=12:00:00
#SBATCH --output=../logs/pred-31km_%j.log
#SBATCH --error=../logs/pred-31km_%j.err

## Working directory
workdir=/work/nvme/bduu/jbanomedina/regional-ai/data/GLOBAL-31km/scripts/
cd ${workdir}

## Load conda environment
source /u/jbanomedina/miniconda3/etc/profile.d/conda.sh
conda activate /projects/bduu/jbanomedina/envs2/regional-ai

## Parameters
lead_time=174 # 10-hour forecast
epoch=78
vars=2t,z_1000,sp,msl,tp,10u,10v,ivt,iwv
# vars=$(paste -sd, < list-vars.txt)
input=test
stage=A2

## Generate list of dates based on the above parameters
init_interval=24
# Last date not included as per Python way to generate lists
python generate-dates-txt.py 2020-11-01T00 2021-04-01T00 $init_interval list-dates-2021.txt # Winter 20-21
python generate-dates-txt.py 2021-11-01T00 2022-04-01T00 $init_interval list-dates-2022.txt # Winter 21-22
python generate-dates-txt.py 2022-11-01T00 2023-04-01T00 $init_interval list-dates-2023.txt # Winter 22-23
python merge_list_dates_txt.py list-dates-2021.txt list-dates-2022.txt list-dates-2023.txt  # Concatenate winters
rm list-dates-2021.txt list-dates-2022.txt list-dates-2023.txt
dates=$(<list-dates.txt)

## Create directory in case it does not exist
mkdir -p ../outputs/epoch-$epoch/
mkdir -p ../outputs/epoch-$epoch/31km/

## Loop over the initial conditions 
for date in $dates; do
    
    ## Information about forecast
    echo "Running GLOBAL model (31km) at EPOCH $epoch to generate a $lead_time-hour forecast with initial condition: $date ($input set)"

    ## Run script anemoi inference
    anemoi-inference run config.yaml \
     date=$date \
     input=$input \
     checkpoint=../../../models/GLOBAL-31km/epoch-$epoch/inference/$stage-epoch$epoch.ckpt \
     lead_time=$lead_time
     output.netcdf=../outputs/temp-$epoch.nc

    ## Post-process (e.g., subset variables of interest, compute ivt and interpolate to 4km-prism). 
    python postprocess-anemoi-output.py \
     ../outputs/epoch-$epoch/ \
     $date \
     $lead_time \
     $vars \
     ../outputs/temp-$epoch.nc

    ## Delete temporary file
    rm ../outputs/temp-$epoch.nc

done

## Remove list of dates
# rm list-dates.txt

