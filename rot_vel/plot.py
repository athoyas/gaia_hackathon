#this code should create a plot using the numbers I have calculated

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.stats import histogram

def create_plot(data):###FIX THIS
    '''
    create a rot vel curve for objects
    '''
    print("Beginning plotting")

    #get bins and median rot vel for each bin
    df_plot = create_bins(data)

    distance = df_plot["bin_center"]
    speed = df_plot["med_rot_vel"]

    #create plot
    plt.figure(figsize=(8,6))
    plt.scatter(distance, speed)

    #label plot
    plt.xlabel("Distance from MW center (pc)")
    plt.ylabel("Rotational Speed around MW (km/s)")
    plt.title("Rotational Speed vs Distance for object orbiting the galactic center")

    #save plot
    plt.savefig("/work/submit/athoyas/spd_vs_distance.png", dpi=300, bbox_inches='tight')

    print("Finished plotting!!")

def create_bins(data):
    '''
    computes radial distance on a logarithmic scale to create bins, finds median rot vel in each bin and saves these values
    param:
    data: df that includes d_gc and rot_vel
    '''
    #gets columns we need
    d_gc = data["d_gc"].to_numpy()
    rot_vel = data["rot_vel"].to_numpy()

    #create histogram w/ certain parameters
    num_bins = 20
    d_gc_min = d_gc.min()
    d_gc_max = d_gc.max()
    lin_bins = np.linspace(d_gc_min, d_gc_max, num_bins+1)
    hist, bin_edges = histogram(d_gc, bins=lin_bins)

    #figures out bins and median rot vel in each bin
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    bin_indices = np.digitize(d_gc, bin_edges) - 1
    medians_v_rot = np.array([np.median(rot_vel[bin_indices == i]) if np.any(bin_indices == i) else np.nan for i in range(len(bin_edges) - 1)])

    #saves info to new df and returns it
    df_to_plot = pd.DataFrame({"bin_center": bin_centers, "med_rot_vel": medians_v_rot})
    return df_to_plot

