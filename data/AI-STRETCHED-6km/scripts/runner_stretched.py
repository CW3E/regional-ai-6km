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
# date = datetime.datetime(1979, 1, 3, 6)
lead_time = int(sys.argv[3])
stage = str(sys.argv[4])
version = str(sys.argv[5])
###########################################
################ INFERENCE ################ 
###########################################
# Create a runner with the checkpoint file
# path_model = "/work/nvme/bduu/jbanomedina/regional-ai/models/STRETCHED-6km/inference/epoch-%s/inference-last-5vars-b.ckpt" % (epoch)
path_model = "../../../models/STRETCHED-6km-%s/epoch-%s/inference/%s-epoch%s.ckpt" % (version, epoch, stage, epoch)
runner = SimpleRunner(path_model)

## Input
path_global = "../../zarrs/era5-31km.zarr"
path_lam = "../../zarrs/cw3e-6km-test.zarr"
# path_global = "/work/hdd/bduu/jbanomedina/regional-ai/data/zarrs/1979-01-era5-31km.zarr"
# path_lam = "/work/hdd/bduu/jbanomedina/regional-ai/data/zarrs/1979-01-cw3e-6km.zarr"
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

## Taken from Lines 119-120 in anemoi-inference/src/anemoi/inference/inputs/dataset.py to check order of multi-input.
## Based on code below the order is t-6, t.
# date = np.datetime64(date)
# [date + np.timedelta64(h) for h in runner.checkpoint.lagged]
