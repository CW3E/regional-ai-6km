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




