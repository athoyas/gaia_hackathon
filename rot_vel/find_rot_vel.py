
###1/28
###Main code

import sys
import read_file
import calculate
import plot

overwrite = False

###Step 1: Get filtered dictionary of Gaia data with values we want
if overwrite:
    result_df = read_file.filter_file()
else:
    result_df = read_file.read_gaia()

###Step 2: Calculate rotational velocity data
result_df = calculate.get_rot_velocity(result_df)

###Step 3: Calculate distance from MW center
result_df = calculate.get_gc_distance(result_df)

#Step 4: Plot data
plot.create_plot(result_df)
