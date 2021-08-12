"""Kernel Phase FITS Format Test File

This module contains a single function which produces a test Kernel Phase FITS
file according to the specifications in the format document. 

Example
-------

To produce the test file simply run the following: 

    $ python dummyfile.py filename.fits 

"""

import fitsio 
import argparse 
import numpy as np

from numpy.random import randint 

def create_dummy(filename): 
    """Create dummy file 

    This is the main function which takes in a name and produces the fake file. 

    Parameters
    ----------
    filename (str) : the name of the dummy file 

    """ 

    #Create the parameters for the file 
    num_kernels = randint(low=10, high=1000) 
    num_frames = randint(low=5, high=50) 
    num_pixels = 2**randint(low=2, high=8)
    num_apertures = randint(low=56, high=752) 
    num_wavelengths = randint(low=1, high=11)
    num_uv = randint(low=100, high=200) 
        
    #--- Required HDUs ---# 
    primary = np.zeros((num_frames, num_wavelengths, num_pixels, num_pixels)) 
    aperture = np.zeros((num_apertures, 3)) 
    uv_points = np.zeros((num_uv, 3)) 
    ker_mat = np.zeros((num_kernels, num_uv)) 
    blm_mat = np.zeros((num_uv, num_apertures)) 
    kp_data = np.zeros((num_frames, num_wavelengths, num_kernels)) 
    kp_sigm = np.zeros((num_frames, num_wavelengths, num_kernels))
    detpa = np.zeros((num_frames)) 
    vis_data = np.zeros((num_frames, num_wavelengths, num_uv)) 

    #CWAVEL is a table 
    cwavel = {} 
    cwavel["CWAVEL"] = np.zeros(num_wavelengths)
    cwavel["DWAVEL"] = np.zeros(num_wavelengths) 
  
    #--- Optional HDUs ---# 
    ka_data = kp_data
    ka_sigm = kp_sigm 
    cal_mat = np.zeros((randint(low=2, high=20), num_kernels)) 
    kp_cov = np.zeros((num_frames, num_wavelengths, num_kernels, num_kernels)) 
    ka_cov = kp_cov 
    full_cov = np.zeros((num_frames, num_wavelengths, 2, num_kernels, 2,
        num_kernels))
    
    #IMSHIFT is a table 
    imshift = {} 
    imshift["XSHIFT"] = np.zeros(num_frames)
    imshift["YSHIFT"] = np.zeros(num_frames) 

    #Create the primary header 
    prim_header = {"PSCALE":3.14, "DIAM":1.62, "EXPTIME":2.72} 

    #Open the file for writing
    with fitsio.FITS(filename, "rw") as f:  
        
        #Required HDUs
        f.write(primary, header=prim_header, extname="PRIMARY")     
        f.write(aperture, extname="APERTURE")     
        f.write(uv_points, extname="UV-PLANE") 
        f.write(ker_mat, extname="KER-MAT")     
        f.write(blm_mat, extname="BLM-MAT")     
        f.write(kp_data, extname="KP-DATA")     
        f.write(kp_sigm, extname="KP-SIGM")     
        f.write(cwavel, extname="CWAVEL")
        f.write(detpa, extname="DETPA")     
        f.write(vis_data, extname="VIS-DATA")     

        #Optional HDUs
        f.write(ka_data, extname="KA-DATA")     
        f.write(ka_sigm, extname="KA-SIGM")     
        f.write(cal_mat, extname="CAL-MAT")     
        f.write(kp_cov, extname="KP-COV")     
        f.write(ka_cov, extname="KA-COV")     
        f.write(full_cov, extname="FULL-COV")     
        f.write(imshift, extname="IMSHIFT")
 
if __name__ == "__main__": 

    #Parse the inputted file names 
    parser = argparse.ArgumentParser(
        description="Kernel phase FITS file validator."
        )

    parser.add_argument("files", type=str, nargs="+",
            help="Filename of the dummy file"
    )
    
    args = parser.parse_args() 

    #Iterate through the list of files and produce them 
    for file_ in args.files:

        create_dummy(file_) 
    
