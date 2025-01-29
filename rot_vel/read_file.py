
###reads gaia data file and saves it

import pandas as pd

def get_gaia():
    '''
    gets the gaia data and saves it into a pandas file
    '''
    print("Reading Gaia Data")
    df = pd.read_hdf("/ceph/submit/data/group/gaia/dr3/kinematics/all_w_rv_kin.h5")

    return df

def filter_file():
    '''
    gets gaia data and filters for the data we want (ra, dec, radvel, l, b, pmra, pmdec)
    '''
    #step 1: get data
    data = get_gaia() 

    #step 2: get a random 500,000 points from the gaia data
    smallerdf = data.sample(n=500_000, random_state=42)

    #step 3: choose columns that we want
    columns_to_keep_and_rename = [
        'ra',
        'dec',
        'l',
        'b',
        'parallax',
        'parallax_error',
        'radial_velocity',
        'pmra',
        'pmdec',
    ]

    #step 4: select columns
    filtered_df = smallerdf[list(columns_to_keep_and_rename)]

    #step 5: continue filtering for stars with small parallax error
    filtered_df = filtered_df[(filtered_df["parallax_error"]/filtered_df["parallax"] < 0.2) & 
                              (filtered_df["parallax"] > 0) &
                              (filtered_df["parallax"] > 0.1)
                              ]

    #step 6: save df so we dont have to get the data every time
    file_path = "/work/submit/athoyas/filtered_data.csv"
    filtered_df.to_csv(file_path, index=False)

    print("Created, filtered, and saved Dictionary!")
    return filtered_df

def read_gaia():
    '''
    reads filtered gaia data and returns a dictionary
    '''
    
    file_path = "/work/submit/athoyas/filtered_data.csv"
    df = pd.read_csv(file_path)

    print("Read filtered Gaia data!")
    return df