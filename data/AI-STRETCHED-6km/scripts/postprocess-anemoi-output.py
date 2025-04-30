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
exec(open(path+'./interpCoords_4km.py').read())
exec(open(path+'./get_info_from_date.py').read())
exec(open(path+'./aggregate_tp_daily.py').read())

## Parameters
path_output = str(sys.argv[1])
date = sys.argv[2]
lead_time = int(sys.argv[3])
vars = list(sys.argv[4].split(','))
lats_path = str(sys.argv[5])
lons_path = str(sys.argv[6])
file_temp = str(sys.argv[7])
# lats = [int(item) for item in sys.argv[5].split(',')]
# lons = [int(item) for item in sys.argv[6].split(',')]


# ## Load temporary prediction at ../outputs/temp.nc --> direct output from anemoi-inference
# ds = xr.open_dataset("../outputs/temp.nc")
ds = xr.open_dataset(file_temp)

## Select domain (to avoid saving the entire output which could be very demanding in terms of storage)
# idx_lon = np.where((ds.longitude >= lons[0]) & (ds.longitude <= lons[1]))[0]
# idx_lat = np.where((ds.latitude >= lats[0]) & (ds.latitude <= lats[1]))[0]
# idx = np.intersect1d(idx_lon, idx_lat)
# ds = ds.isel(values = idx)

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


# ####### Save 24-hour accumulated precipitation totals over the PRISM 4-km resolution and only over a domain similar to the 2-km domain #######
# if "tp" in vars:
#     print("Accumulating precipitation (24-hour accumulated)")
#     ## Create output directory?
#     output_dir="%s/4km-prism/%s" % (path_output, winter_season)
#     if not os.path.exists(output_dir):
#         os.mkdir(output_dir)
#     ## 4-km PRISM latitude and longitude gridpoints over a domain similar to the 2-km one
#     lats = np.load(lats_path)
#     lons = np.load(lons_path)
#     # lat_grid, lon_grid = np.meshgrid(lats, lons)
#     # target_coords = np.stack((lat_grid.flatten(), lon_grid.flatten()), axis = 0)
#     ## Select variable
#     dsv6 = ds[["tp"]]
#     ## Add latitude and longitude as coordinates
#     dsv6 = dsv6.assign_coords({"lat": ds.latitude, "lon": ds.longitude})
#     ## Add stationID
#     dsv6 = dsv6.rename({"values": "stationID"})
#     dsv6 = dsv6.assign_coords({"stationID": np.arange(dsv6["tp"].values.shape[1])})
#     ## Problem with precipitation at t=0
#     dsv6["tp"].isel(time=0)[:] = 0
#     ## Aggregate 24-hour precipitation
#     dsv24 = aggregate_tp_daily(dsv6, lead_time, time_resolution = 6)
#     ## Interpolate to PRISM 4-km
#     # lons = [-180, 179, -50, 0] # Random points to test the function find_nearest_station
#     # lats = [-90, -30, 40, 45] # Random points to test the function find_nearest_station
#     # lons = np.load("%s/../PRISM/lonsCoords_2kmDomain.npy" % (workdir))
#     # lats = np.load("%s/../PRISM/latsCoords_2kmDomain.npy" % (workdir))
#     # lons = np.load(lons_path)
#     # lats = np.load(lats_path)
#     # lat_grid, lon_grid = np.meshgrid(lats, lons)
#     # dsv24i = find_nearest_station(ds = dsv24, target_latitudes = lat_grid.flatten(), target_longitudes = lon_grid.flatten())
#     ## Save files
#     dsv24.to_netcdf("%s/%s_%s.nc" % (output_dir, "tp", date_str_24))
#     ## Remove file from memory
#     dsv6.close()
#     dsv24.close()
#     # dsv24i.close()
#     del dsv6, dsv24
#     gc.collect()


print("Postprocessing... done!")

