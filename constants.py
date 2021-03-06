#######################################################
# Scalar constants
#######################################################

import numpy as np

# Acceleration due to gravity (m/s^2)
gravity = 9.81
# Density of freshwater (kg/m^3)
rho_fw = 1e3
# Density of ice (kg/m^3)
rho_ice = 917.
# Seconds per day
sec_per_day = 24*60*60.
# Seconds per year
sec_per_year = 365.25*sec_per_day
# Months per year
months_per_year = 12
# Degrees to radians conversion factor
deg2rad = np.pi/180.0
# Radius of Earth
rEarth = 6.371e6
# Celsius to Kelvins intercept
temp_C2K = 273.15
# Latent heat of vapourisation (J/kg)
Lv = 2.5e6
# Ideal gas constant for water vapour (J/K/kg)
Rv = 461.5
# Reference saturation vapour pressure (Pa)
es0 = 611
# Coefficient for specific humidity calculation
sh_coeff = 0.62197
# Specific heat of seawater (J/K/kg)
Cp_sw = 4180.

# Degrees formatted nicely in a string
deg_string = r'$^{\circ}$'

# Dictionary of bounds on different regions - some in 2 parts
# lon_min, lon_max, lat_min, lat_max
region_bounds = {
    'fris_plot': [-85., -29., -84., -74.],
    'fris_pster_plot': [-1.6e6, -5e5, 1.2e5, 1.365e6],
    'fris1': [-85., -45., -84., -74.4],
    'fris2': [-45., -29., -84., -77.85],
    'ewed': [-30., 40., -77., -65.],
    'wed_gyre': [-60., 30., -90., -50.],
    'sws_shelf': [-70., -30., -79., -72.],
    'a23a': [-47., -38., -77., -75.],
    'berkner_island': [-55, -41, -81, -77],
    'pine_island_bay': [-105, -101, -75.2, -74.2],
    'dotson_front': [-114, -110.5, -74.1, -73.2],
    'getz': [-135., -114.7, -75.2, -73.5],
    'dotson_crosson': [-114.7, -109., -75.4, -74.1],
    'thwaites': [-109., -103., -75.4, -74.6],
    'pig': [-103., -99., -75.4, -74.],
    'cosgrove': [-102., -98.5, -73.8, -73.2],
    'abbot1': [-104., -99., -73.2, -71.5],
    'abbot2': [-99., -88.9, -73.4, -71.5],
    'venable': [-88.9, -85.6, -73.4, -72.7]
}
# Names corresponding to some keys
region_names = {
    'fris': 'Filchner-Ronne Ice Shelf',
    'ewed': 'Eastern Wedddell ice shelves',
    'getz': 'Getz Ice Shelf',
    'dotson_crosson': 'Dotson and Crosson Ice Shelves',
    'thwaites': 'Thwaites Ice Shelf',
    'pig': 'Pine Island Glacier Ice Shelf',
    'cosgrove': 'Cosgrove Ice Shelf',
    'abbot': 'Abbot Ice Shelf',
    'venable': 'Venable Ice Shelf',
    'all': 'all ice shelves'
}
# Regions that are in two parts
region_split = ['fris', 'abbot']
# Threshold bathymetry delineating shelf
shelf_h0 = -1250

# Resolution of SOSE grid in degrees
sose_res = 1/6.

# BEDMAP2 grid parameters
bedmap_dim = 6667    # Dimension
bedmap_bdry = 3333000    # Polar stereographic coordinate (m) on boundary
bedmap_res = 1000    # Resolution (m)
bedmap_missing_val = -9999    # Missing value for bathymetry north of 60S


