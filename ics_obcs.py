###########################################################
# Generate initial conditions and open boundary conditions.
###########################################################

from grid import Grid, SOSEGrid
from utils import real_dir, xy_to_xyz
from file_io import read_binary, write_binary, NCfile
from interpolation import interp_reg, extend_into_mask

import numpy as np


# Calculate a monthly climatology of the given variable in SOSE, from its monthly output over the entire 6-year reanalysis.

# Arguments:
# in_file: binary SOSE file (.data) containing one record for each month of the SOSE period
# out_file: desired path to output file
# dimensions: 'xy' or 'xyz' for 2D and 3D variables respectively
def make_sose_climatology (in_file, out_file, dimensions):

    sose_dim = [sose_nx, sose_ny, sose_nz]
    data = read_binary(in_file, sose_dim, dimensions+'t')    
    climatology = np.zeros(tuple([12]) + data.shape[1:])
    for month in range(12):
        climatology[month,:] = np.mean(data[month::12,:], axis=0)
    write_binary(climatology, out_file)


def sose_ics (grid_file, sose_dir, output_dir, nc_out=None, split=180):

    sose_dir = real_dir(sose_dir)
    output_dir = real_dir(output_dir)

    # 3D fields to interpolate
    fields_3d = ['THETA', 'SALT']
    # 2D fields to interpolate
    fields_2d = ['SIarea', 'SIheff']
    # End of filenames for input
    infile_tail = '_climatology.data'
    # End of filenames for output
    outfile_tail = '_SOSE.ini'

    # Number of iterations to remove coastal points from SOSE
    coast_iters = 10
    
    print 'Building grids'
    # First build the model grid and check that we have the right value for split
    if split == 180:
        model_grid = Grid(grid_file)
        if model_grid.lon_1d[0] > model_grid.lon_1d[-1]:
            print 'Error (sose_ics): Looks like your domain crosses 180E. Run this again with split=0.'
            sys.exit()
    elif split == 0:
        model_grid = Grid(grid_file, max_lon=360)
        if model_grid.lon_1d[0] > model_grid.lon_1d[-1]:
            print 'Error (sose_ics): Looks like your domain crosses 0E. Run this again with split=180.'
            sys.exit()
    else:
        print 'Error (sose_ics): split must be 180 or 0'
        sys.exit()
    # Now build the SOSE grid
    sose_grid = SOSEGrid(sose_dir+'grid/', model_grid, split=split)

    print 'Building mask for SOSE points to discard'
    # Figure out which points we don't trust
    # (1) Closed cells according to SOSE
    sose_mask = sose_grid.hfac == 0
    # (2) Closed cells according to model, interpolated to SOSE grid
    # Only consider a cell to be open if all the points used to interpolate it are open. But, there are some oscillatory interpolation errors which prevent some of these cells from being exactly 1. So set a threshold of 0.99 instead.
    # Use a fill_value of 1 so that the boundaries of the domain are still considered ocean cells (since sose_grid is slightly larger than model_grid). Boundaries which should be closed will get masked in the next step.
    model_open = interp_reg(model_grid, sose_grid, np.ceil(model_grid.hfac), dim=3, fill_value=1)
    model_mask = model_open < 0.99
    # (3) Points near the coast (which SOSE tends to say are around 0C, even if this makes no sense). Extend the surface model_mask by coast_iters cells, and tile to be 3D. This will also remove all ice shelf cavities.
    coast_mask = xy_to_xyz(extend_into_mask(model_mask[0,:], missing_val=0, num_iters=coast_iters), sose_grid)
    # Put them all together into one mask
    discard = (sose_mask + model_mask + coast_mask).astype(bool)

    print 'Building mask for SOSE points to fill'
    # Now figure out which points we need for interpolation
    # Open cells according to model, interpolated to SOSE grid
    # This time, consider a cell to be open if any of the points used to interpolate it are open (i.e. ceiling)
    fill = np.ceil(model_open)
    # Extend into the mask a few times to make sure there are no artifacts near the coast
    fill = extend_into_mask(fill, missing_val=0, use_3d=True, num_iters=3)


    # Loop over variables:
    #   Read the data
    #   Remove the points we don't trust
    #   Fill the points we need to fill
    #   Interpolate
    #   Write to file
    


    
    '''print 'Interpolating mask'
    # Figure out which points on the model grid can't be reliably interpolated from SOSE output (as they are outside the bounds, within the land/ice-shelf mask, or too near the coast)
    interp_mask = interp_reg_3d_mask(grid, sose_grid)

    # Set up a NetCDF file so the user can check the results
    if nc_out is not None:
        ncfile = NCfile(nc_out, grid, 'xyz')

    # Process 3D fields
    for n in range(len(fields_3d)):
        print 'Processing ' + fields_3d[n]
        in_file = sose_dir + fields_3d[n] + infile_tail
        out_file = output_dir + fields_2d[n] + outfile_tail
        print '...reading ' + in_file
        # Just keep the January climatology
        sose_data = read_binary(in_file, sose_grid, 'xyzt')[0,:]
        data_interp = interp_fill_reg_3d(grid, sose_grid, sose_data, interp_mask)
        print '...writing ' + out_file
        write_binary(data_interp, out_file)
        if nc_out is not None:
            print '...adding to ' + nc_out
            ncfile.add_variable(fields_3d[n], data_interp, 'xyz')

    if nc_out is not None:
        ncfile.finished()'''
