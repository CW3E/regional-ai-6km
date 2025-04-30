## Import libraries
import os
import sys
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# File paths
file1 = sys.argv[1]
file2 = sys.argv[2]
file3 = sys.argv[3]
output_file = 'list-dates.txt'

# Open the output file in write mode
with open(output_file, 'w') as outfile:
    # List of input files
    input_files = [file1, file2, file3]   
    # Iterate over each file
    for idx, fname in enumerate(input_files):
        with open(fname, 'r') as infile:
            # Write the content of the file to the output file
            # If it's not the first file, avoid writing extra newlines
            if idx > 0:
                # Avoid adding a new line at the start
                outfile.write(infile.read())
            else:
                # For the first file, write its content directly
                outfile.write(infile.read())