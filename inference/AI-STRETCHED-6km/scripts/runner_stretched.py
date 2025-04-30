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

## Import libraries
import os
import sys
import gc
import xarray as xr
import numpy as np
import warnings
import datetime
from anemoi.inference.inputs.dataset import DatasetInput
from anemoi.inference.outputs.netcdf import NetCDFOutput
from anemoi.inference.runners.simple import SimpleRunner
warnings.filterwarnings("ignore")

## Parameters
epoch = str(sys.argv[1])
date = str(sys.argv[2])
lead_time = int(sys.argv[3])
stage = str(sys.argv[4])
version = str(sys.argv[5])
###########################################
################ INFERENCE ################ 
###########################################
# Create a runner with the checkpoint file
path_model = "../../../models/STRETCHED-6km-%s/epoch-%s/inference/%s-epoch%s.ckpt" % (version, epoch, stage, epoch)
runner = SimpleRunner(path_model)

## Input
path_global = "../../zarrs/era5-31km.zarr"
path_lam = "../../zarrs/cw3e-6km-test.zarr"
kwargs = {"cutout": [
                     {"dataset": path_lam}, 
                     {"dataset": path_global}
                     ],
          "adjust": "all",
          "min_distance_km": 3
         }
input = DatasetInput(runner, [], kwargs)

## Forcing and diagnostic variables
vars_forcing = ["cos_julian_day", "cos_local_time", "cos_longitude", "cos_latitude", 
                "sin_julian_day", "sin_local_time", "sin_longitude", "sin_latitude", 
                "lsm", "z_sfc"]
vars_diagnostic = ["tp"]
vars_metadata = ["latitude", "longitude"]

## Run the model and write the output to a temporary file
date = np.datetime64(date)
# time_delta = datetime.timedelta(hours=6)
time_delta = np.timedelta64(6, "h")
for iter in range(int(lead_time/6)):
    ## Out
    path_output = "../outputs/epoch-%s/temp-%i.nc" % (epoch, iter)
    output = NetCDFOutput(runner, path_output)
    ## Get/update date 
    if iter > 0:
        date = date + time_delta
    print("Iteration: %i ... Forecasting: %s" % (iter, str(date)))
    # Load initial state
    input_state = input.create_input_state(date = date)
    ## ALTERNATIVE: Update initial state due to bug in anemoi-inference
    if iter > 0:
        # Load outputs from the previous step
        input_prev = xr.open_dataset(path_output_prev)
        # Replace variables in initial state with forecasted variables
        vars_complete = list(input_prev.keys()) 
        for var in vars_complete: 
            if not var in vars_forcing and not var in vars_diagnostic and not var in vars_metadata: # Replace prognostic
                input_state["fields"][var] = input_prev[var].values
            if var in vars_diagnostic:
                input_state["fields"].pop(var, None)
    # Write the initial state to the output file
    output.write_initial_state(input_state)
    for state in runner.run(input_state=input_state, lead_time=6):
        output.write_state(state)
    path_output_prev = path_output
    ## Close the output file
    output.close()
    print("Inference... done!")

## Merge all temp-%i files into a single one:
ds_series = []
for iter in range(int(lead_time/6)):
    ## Load data
    path_output = "../outputs/epoch-%s/temp-%i.nc" % (epoch, iter)
    ds = xr.open_dataset(path_output)
    if iter > 0:
        ds = ds.isel(time = 1)
    ds_series.append(ds)
## Concatenate by time
ds_series = xr.concat(ds_series, dim = "time")
## Remove time in latitude and longitude
ds_series['latitude'] = ds_series['latitude'].isel(time=0)
ds_series['longitude'] = ds_series['longitude'].isel(time=0)
## Save
ds_series.to_netcdf("../outputs/epoch-%s/temp.nc" % (epoch))
    
## Delete previous temporal files
for iter in range(int(lead_time/6)):
    path_output = "../outputs/epoch-%s/temp-%i.nc" % (epoch, iter)
    os.remove(path_output)

