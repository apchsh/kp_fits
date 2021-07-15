"""Kernel Phase FITS Format Validator

***TEST SCRIPT / WIP*** 

This module is built to validate that FITS files containing kernel phases are
saved in the standard (to be decided) format. Currently the module relies on
the fitsio library to read in the file, and a validator class which check each
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
import fitsio 

from os.path import exists

class validator(): 
    """Validation class

    This class decided whether a file matches the correct format as specified 
    in the document XXXX. The class takes in a "structure" dictionary from the
    read_fits() function, which is a dictionary containing all the relevant
    info for each hdu in the fits file. 

    Attributes
    ----------
    struct : dict 
        Containing the information of the file to be validated 

    Notes
    ----

    Todo
    ----

    """

    _struct = None 

    def _check_hdu_names(self): 
        """Check required HDUs""" 
        
        if not("APERTURE") in self._struct.keys(): 
            print("APERTURE HDU missing") 
    

    def _validate(self): 
        """Run the validation

        Returns
        -------
        result : bool
            True if valid, false otherwise

        """ 

        #List of requirements the file must meet 
        self._check_hdu_names() 

    def __init__(self, struct): 
        """Initialise the class and run the validation

        Parameters
        ----------
        struct : dict
            Contains the information of the file to be validated

        Returns
        -------
        result : bool 
            True if valid, false otherwise 

        Todo
        ----
        - Do some validation on the struct object to check its not empty etc..

        """ 
        
        self._struct = struct 
        return self._validate() 


def read_fits(filename, verbose=False): 
    """Function to read in and process a fits file 

    Function which takes in a fits filename and parses the contents into a
    list for the validator class. 

    Parameters
    ----------
    filename : str
        The name of the fits file to be processed
    verbose : bool
        How much info to print 

    Returns
    -------
    struct : dict
        Dict of dicts containing all the useful info from the fits file

    """ 

    #Dictionary into which we'll be saving the fits file info 
    struct = {}

    #Open and read in the fits file 
    f = fitsio.FITS(filename)

    if verbose: print("Validating %s..." % filename) 

    #Iterate through the extensions 
    for ext in f: 

        #Read in the extension information 
        ext_info = ext.get_info() 
        ext_header = ext.read_header()

        #Lets come up with a name under which to save the info 
        if len(ext_info["hduname"]) > 0: 
            name = ext_info["hduname"] 
        elif len(ext_info["extname"]) > 0:
            name = ext_info["extname"] 
        else:
            name = ext_info["extnum"] 

        #Now lets store the useful information 
        struct[name] = {} 
        struct[name]["dims"] = ext_info["dims"] 
        struct[name]["hdutype"] = ext_info["hdutype"] 
        struct[name]["header"] = ext_header 
        
    #Finally close the file
    f.close()

    return struct 

def summary(struct, filename): 
    """Print a summary of the file information

    Parameters
    ----------
    struct : dict
        The dictionary produced by read_fits() which contains file info
    filename : str
        The filename to which the "struct" dictionary belongs
    """ 

    #preamble 
    str_ = "*** %s ***" % filename 
    print(str_) 
    print("-"*len(str_)) 

    for key in struct.keys():
        
        print(key, struct[key]["dims"]) 

    #final print 
    print("-"*len(str_)) 
 
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

            #Check the file is real 
            if exists(file_): 
                
                #Read in the fits file 
                file_info = read_fits(file_, verbose=True) 

                #Optional file info
                summary(file_info, file_) 

                #Run the validation
                validator(file_info) 

            else:
                #!TODO: change this to python3 string formatting 
                print("%s does not exist." % file_) 

    

