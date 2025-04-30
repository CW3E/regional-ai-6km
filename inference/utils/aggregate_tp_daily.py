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

