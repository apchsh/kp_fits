"""Kernel Phase FITS Format Validator

***TEST SCRIPT / WIP*** 

This module is built to validate that FITS files containing kernel phases are
saved in the standard (to be decided) format. Currently the module relies on
astropy.fits.io to read in the file, and a validator class which check each
extension size, format etc... 

Example
-------

To run the validator simply type the following: 

    $ python validate.py my_file.fits 

The script can also take in multiple fits files as a list: 

    $ python validate.py my_file1.py my_file2.py ... my_fileN.py

Notes
-----

At the moment it's being setup so that the validator takes in a dictionary
containing all the relevant info about the file, this way the fits library is 
decoupled from the code. This may change in future if it's decided 
that it doesn't make sense... 


Attributes
----------

"""

import argparse 
from astropy.io import fits 
from os.path import exists

class validator(): 
   """Validation class

   """


if __name__ == "__main__": 

    #Parse the inputted file names 
    parser = argparse.ArgumentParser(
        description="Kernel phase FITS file validator."
        )

    parser.add_argument("files", type=str, nargs="+",
            help="Files to be processed"
    )
    
    args = parser.parse_args() 

    #Run through the files and validate in turn 
    if len(args.files) == 0:
    
        print("Error: no files provided.") 

    else:

        for file_ in args.files:

            if exists(file_): 
                
                print("validating: %s" % file_) 

            else:
                #!TODO: change this to python3 string formatting 
                print("%s does not exist." % file_) 

    

