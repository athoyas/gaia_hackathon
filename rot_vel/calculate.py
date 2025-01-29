
###This file should get all the information from the data set and find the rotational velocity of the stars / distance from galactic center

import pandas as pd
import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u

def get_rot_velocity(data):
    '''
    get a rotational velocity for every value in the dataframe, add it to the df, and return both
    param:
    data: the dataframe of filtered stars
    '''

    #get specific columns
    ra=data["ra"].to_numpy()
    dec=data["dec"].to_numpy()
    l=data["l"].to_numpy()
    b=data["b"].to_numpy()
    parallax=data["parallax"].to_numpy()
    radial_velocity=data["radial_velocity"].to_numpy()
    pmra=data["pmra"].to_numpy()
    pmdec=data["pmdec"].to_numpy()

    print("Starting to calculate rotational velocity for each data point")

    #step 1: find distance
    d = abs(1000/parallax)

    #step 2: constant
    sun_position = np.array([-8178, 0, 0])
    v_sun = np.array([-11.1, 12.24+220, 7.25])

    #step 3: convert proper motions to galactic frame
    coord = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, distance=d*u.pc, pm_ra_cosdec=pmra*u.mas/u.yr, pm_dec=pmdec*u.mas/u.yr, 
                     radial_velocity=radial_velocity*u.km/u.s, frame='icrs')
    coords_galactic = coord.transform_to('galactic')
    
    #step 4: convert to cartesian coordinates and account for sun's motion relative to LSR
    v_xyz = coords_galactic.velocity.d_xyz.to(u.km/u.s).value
    v_cor = v_xyz.T - v_sun
    v_cor = v_cor.T

    #step 5: compute rotational velocity
    x, y = coords_galactic.cartesian.x.value + sun_position[0], coords_galactic.cartesian.y.value
    rot_vel = (x * v_cor[1] - y * v_cor[0]) / np.sqrt(x**2 + y**2)

    #step 6: add numpy array to dataframe
    data["rot_vel"] = rot_vel

    print("Finished calculating rotational velocity")
    return data

def get_gc_distance(data):
    '''
    get distance to center of the galaxy for each star
    param:
    data: the dataframe of filtered stars
    '''

    print("Finding distance to MW center")

    #get specific columns
    l=data["l"].to_numpy()
    b=data["b"].to_numpy()
    parallax=data["parallax"].to_numpy()

    #constant
    R0 = 8.3*1000

    #step 1: heliocentric distance
    d_sun = abs(1000/parallax)
    print("maximum parallax distance from Earth:", max(d_sun))
    print("minimum parallax angle:", min(abs(parallax)))
    print("maximum parallax angle:", max(parallax))

    #step 2: convert to radians
    l_rad = np.radians(l)
    b_rad = np.radians(b)

    #step 3: calculate distance to mw center
    d_gc = np.sqrt(R0**2 + d_sun**2 - 2 * R0 * d_sun * np.cos(l_rad) * np.cos(b_rad))

    #step 4: add numpy array to df
    data["d_gc"] = d_gc

    print("Finished finding distance to MW Center")
    return data


