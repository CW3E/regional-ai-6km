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
from scipy.interpolate import griddata
import xarray as xr
import numpy as np
import warnings
warnings.filterwarnings("ignore")

## Source auxiliary functions
path = "/work/nvme/bduu/jbanomedina/regional-ai/data/utils/"
exec(open(path+'./get_info_from_date.py').read())
exec(open(path+'./aggregate_tp_daily.py').read())

## Parameters
path_output = str(sys.argv[1])
date = sys.argv[2]
lead_time = int(sys.argv[3])
vars = list(sys.argv[4].split(','))
file_temp = str(sys.argv[5])

## Load temporary prediction at ../outputs/temp.nc --> direct output from anemoi-inference
ds = xr.open_dataset(file_temp)

## Get info initial condition
yyyy, mm, dd, winter_season = get_info_from_date(date)
date_str = "%s-%s-%sT%s" % (yyyy, mm, dd, str(date)[11:13])
date_str_24 = "%s-%s-%s" % (yyyy, mm, dd)

####### Save each variable individually in a .nc file (instant time) #######
## Create output directory?
output_dir="%s/6km/%s" % (path_output, winter_season)
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

for var in vars:
    ## Integrated vapor transport?
    if var == "ivt":
        dsv = np.sqrt(ds["ivt_u"]**2 + ds["ivt_v"]**2)
        ds_ = xr.Dataset({"ivt": (("time", "values"), dsv.values)},
                          coords={dim: ds.coords[dim] for dim in dsv.dims})
    else:
        ds_ = ds
    ## Select variable
    dsv = ds_[[var]]
    ## Add latitude and longitude as coordinates
    dsv = dsv.assign_coords({"lat": ds.latitude, "lon": ds.longitude})
    ## Add stationID
    dsv = dsv.rename({"values": "stationID"})
    dsv = dsv.assign_coords({"stationID": np.arange(dsv[var].values.shape[1])})
    ## Problem with precipitation at t=0
    if var == "tp":
        dsv["tp"].isel(time=0)[:] = 0
    ## Save files
    dsv.to_netcdf("%s/%s_%s.nc" % (output_dir, var, date_str))
    ## Remove file from memory
    dsv.close()
    ds_.close()
    del dsv, ds_
    gc.collect()

print("Postprocessing... done!")

