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
    _struct : dict 
        Containing the information of the file to be validated 
    _log : list
        List containing any errors / information about the validation checks


    Notes
    ----

    Todo
    ----

    """

    _struct = None 
    _log = [] 

    _required_hdus = ["APERTURE", "UV-PLANE", "KER-MAT", 
                    "BLM-MAT", "KP-DATA", "KP-SIGM",
                    "CWAVEL", "DETPA", "VIS-DATA"] 

    _standard_names = ["PRIMARY", "APERTURE", "UV-PLANE", "KER-MAT", 
                        "BLM-MAT", "KP-DATA", "KP-SIGM",
                        "CWAVEL", "DETPA", "VIS-DATA",
                        "KA-DATA", "KA-SIGM", "CAL-MAT"]

    def _check_unique(self, list_, name): 
        if len(list(set(list_))) == 1:
            self._log.append("PASS: Number of %s is consistent" % name) 
        elif len(list(set(list_))) >= 2: 
            self._log.append("FAIL: Inconsistent number of %s: " % name)
            self._log.append(list_) 

    def _check_required_hdus(self): 
        """Check required HDUs

        Make sure the mandatory HDUs are present.
        """ 
        
        test = True

        for hdu_ in self._required_hdus:
            if not(hdu_ in self._struct.keys()): 
                test = False
                self._log.append("FAIL: mandatory HDU %s missing" % hdu_) 
 
        if test == True:
            self._log.append("PASS: all mandatory HDUs were found.") 

        return test 

    def _check_num_hdus(self): 
        """Check how many HDUs are present. 

        Currently each file needs to have at least 7 HDUs including the Primary
        one. Rough first check. 
        """

        if len(self._struct) < 7:
            self._log.append("FAIL: Too few HDUs to be a valid file.") 
            test = False 
        else:
            self._log.append("PASS: sufficient HDUs found.") 
            test = True 

        return test 
        
    def _check_all_hdu_names(self): 
        """Check HDU names

        Check all HDUs for non-standard names and raises a warning message.
        This is just for user info, so won't fail the validation. 
        """
        
        for hdu_name in self._struct.keys(): 

            if not(hdu_name in self._standard_names):
                self._log.append("WARNING: %s is not a standard HDU name"
                         % hdu_name) 

        return True 

    def _check_hdu_dimensions(self): 
        """Check HDU dimensions 

        Check the size of the data in each HDU and make sure it is consistent
        across. This function has to deal with missing HDUs, so can provide
        information even if other tests have failed. 

        """

        #!TODO: check the dimensions of each HDU in turn 
        #!TODO: add the result boolean to if statements and return it 

        result = True #assume it'll pass

        #List of all the array size elements
        kernels = []
        frames = [] 
        pixels = [] 
        apertures = []
        wavelengths = [] 
        uv_points = []

        #Iterate through the list of standard HDUs
        for hdu in self._standard_names: 

            #Check if it's present in the file 
            if hdu in self._struct.keys(): 
                
                dims = self._struct[hdu]["dims"] 

                #Extract the dimensions and add it to each list 
                if hdu == "PRIMARY": 
                    if len(dims) == 4: 
                        frames.append(dims[0])
                        wavelengths.append(dims[1])
                        pixels.append(dims[2]) 
                        pixels.append(dims[3]) 
                    else:
                        self._log.append(
                        "FAIL: PRIMARY HDU has too few dimensions"
                        ) 

                if hdu == "APERTURE": 
                    if len(dims) == 2: 
                        apertures.append(dims[0]) 
                        if dims[1] != 3:
                            self._log.append(
                            "FAIL: APERTURE HDU has incorrect dimensions"
                            )
                    else:
                        self._log.append(
                            "FAIL: APERTURE HDU has incorrect dimensions"
                            )

                if hdu == "UV-PLANE": 
                    uv_points.append(dims[0]) 
                
                if hdu == "KER-MAT": 
                    kernels.append(dims[0])
                    uv_points.append(dims[1]) 
                
                if hdu == "BLM-MAT": 
                    uv_points.append(dims[0]) 
                    apertures.append(dims[1])
                
                if hdu == "KP-DATA": 
                    frames.append(dims[0])
                    wavelengths.append(dims[1])
                    kernels.append(dims[2]) 
                
                if hdu == "KP-SIGM": 
                    frames.append(dims[0])
                    wavelengths.append(dims[1])
                    kernels.append(dims[2]) 
                    if len(dims) == 4:
                        kernels.append(dims[3]) 

                if hdu == "CWAVEL": 
                    wavelengths.append(dims[0]) 

                if hdu == "DEPTA":
                    frames.append(dims[0]) 

                if hdu == "VIS-DATA": 
                    frames.append(dims[0])
                    wavelengths.append(dims[1])
                    uv_points.append(dims[2])

                if hdu == "KA-DATA": 
                    frames.append(dims[0])
                    wavelengths.append(dims[1])
                    kernels.append(dims[2]) 
                    
                if hdu == "KA-SIGM": 
                    frames.append(dims[0])
                    wavelengths.append(dims[1])
                    kernels.append(dims[2]) 
                    if len(dims) == 4:
                        kernels.append(dims[3]) 

                if hdu == "CAL-MAT":
                    kernels.appned(dims[2]) 
 
        #!TODO: remove check_unique from function class 

        #Now check that the items in each list are the same
        self._check_unique(kernels, "kernels") 
        self._check_unique(frames, "frames") 
        self._check_unique(pixels, "pixels") 
        self._check_unique(apertures, "apertures") 
        self._check_unique(wavelengths, "wavelengths") 
        self._check_unique(uv_points, "uv-points") 

        return result

    def _validate(self): 
        """Run the validation

        Returns
        -------
        result : bool
            True if valid, false otherwise

        """ 

        #List of requirements the file must meet 
        check1 = self._check_required_hdus()
        check2 = self._check_num_hdus()
        check3 = self._check_hdu_dimensions() 

        #List of non-mandatory checks
        self._check_all_hdu_names() 

        #Display the results
        for item in self._log:
            print(item)  

        if check1 and check2 and check3: 
            return True
        else:
            return False 
 
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
        self._validate() 
        return 


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

    if verbose: print("\nValidating %s..." % filename) 

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
        struct[name]["hdutype"] = ext_info["hdutype"] 
        struct[name]["header"] = ext_header 
  
        #If it's an image it will have the dims keyword
        if "dims" in ext_info.keys():
            struct[name]["dims"] = ext_info["dims"] 
            struct[name]["type"] = "IMAGE"
        else:
            struct[name]["dims"] = [ext_info["nrows"], ext_info["ncols"]] 
            struct[name]["type"] = "TABLE"

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
    str_ = "\n*** %s ***" % filename 
    print(str_) 
    print("-"*len(str_)) 

    for key in struct.keys():
        
        print(key, struct[key]["dims"]) 

    #final print 
    print("-"*len(str_)+"\n") 
 
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

    

