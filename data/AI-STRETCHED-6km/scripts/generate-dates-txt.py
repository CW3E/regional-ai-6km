## Import libraries
import os
import sys
import numpy as np
import warnings
warnings.filterwarnings("ignore")

## Auxiliary function to retrieve yyyy, mm, dd, hh given a date string
def get_info_date(date):
    yyyy = date[0:4]
    mm = date[5:7]
    dd = date[8:10]
    hh = date[11:13]
    return yyyy, mm, dd, hh

## Parameters
date_first_str = sys.argv[1]
date_last_str = sys.argv[2]
init_interval = int(sys.argv[3])
path_txt = str(sys.argv[4])

## To numpy format
date_first_np = np.datetime64('%s:00:00' % (date_first_str))
date_last_np = np.datetime64('%s:00:00' % (date_last_str))
step = np.timedelta64(init_interval, 'h')

## Numpy list of dates
dates = np.arange(date_first_np, date_last_np, step)

## Print list of dates in .txt
with open(path_txt, 'w') as file:
    # Loop over the dates and write each one on a new line
    for date in dates:
        file.write(str(date) + '\n')  # Convert date to string and add a newline

print("Dates from %s to %s with a step of %i hours have been written to 'list-dates.txt'." % (date_first_str, date_last_str, init_interval))




