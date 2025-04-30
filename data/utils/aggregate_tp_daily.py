import math
def aggregate_tp_daily(dsv6, lead_time, time_resolution = 6):
    ## Initial condition
    date_init = dsv6.isel(time = 0).time.values
    ### Since predictions were accumulated since the beginning of the simulation, de-transform into 6-hourly accumulated totals
    # data_file_increment = get_(dsv6)
    data_file_increment = dsv6
    ## Generate 24-hourly accumulated totals
    data_file_step = []
    num_days = int(math.floor(lead_time/24))
    for day in range(num_days): # 7-day forecast
        # Select 6-hourly intervals
        start_step = (day * 4) + 1
        end_step = (day + 1) * 4 + 1
        # print(np.arange(start_step, end_step, 1))
        aux = data_file_increment.isel(time = np.arange(start_step, end_step, 1))
        # Aggregate the 6-hourly forecasts into a 24-hour precipitation value
        aux = aux.sum("time")
        # Update date of forecast
        date_forecast = date_init + day * np.timedelta64(24, 'h')
        aux = aux.assign_coords({"time": date_forecast})
        data_file_step.append(aux)
    ## Concatenate the 7-day totals into one
    dsv24 = xr.concat(data_file_step, dim = "time")
    ## Return 24-hour aggregated precipitation
    return dsv24

