"""Kernel Phase FITS Format Validator

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

def dimension_check(dims, req, hdu_name):
    """HDU Dimension Check

    Helper function which checks the number of HDU dimensions and then returns
    a log message and a boolean value if they match the required number. 

    Parameters
    ----------
    dims (list) : List of the dimensions of the HDU 
    req (int) : required number of dimensions 
    hdu_name (str) : HDU name as a string 

    Returns
    -------
    result (bool) : True/false based on pass/fail
    log (str) : A message to append to the log 

    """
    
    log = "" 

    if len(dims) == req: 
        return True, log 
    else:
        return False, "FAIL: %s HDU has incorrect dimensions" % hdu_name 
   
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
    _required_hdus : list
        List containing the names of the mandatory HDUs
    _standard_names : list 
        List containing standardised names for optional HDU categories 
    """

    _struct = None 
    _log = [] 

    _required_hdus = ["APERTURE", "UV-PLANE", "KER-MAT", 
                    "BLM-MAT", "KP-DATA", "KP-SIGM",
                    "CWAVEL", "DETPA", "CVIS-DATA"] 

    _standard_names = ["PRIMARY", "APERTURE", "UV-PLANE", "KER-MAT", 
                        "BLM-MAT", "KP-DATA", "KP-SIGM",
                        "CWAVEL", "DETPA", "CVIS-DATA",
                        "KA-DATA", "KA-SIGM", "CAL-MAT", "KP-COV", 
                        "KA-COV", "FULL-COV", "IMSHIFT"]

    _required_keys = ["PSCALE", "DIAM", "EXPTIME", "GAIN", "CONTENT"] 

    def _check_unique(self, list_, name):
        """Check HDU sizes are consistent

        Checks that all the numbers in a list are the same. The list contains
        values of dimensions from a number of HDUs which should all be
        internally consistent

        Parameters
        ----------
        list_ (list) : list of dimensions 
        name (str) : HDU name 

        """

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

    def _check_primary_header(self): 
        """Check primary header keywords 

        Function to check for mandatory keywords in the primary header 

        """ 

        result = True 
        header = self._struct["PRIMARY"]["header"] 

        #Iterate through the required keys and check for them 
        for key in self._required_keys: 
            if not(key in header.keys()): result = False 
    
        if result:
            self._log.append("PASS: mandatory keywords present in PRIMARY HDU")
        else:
            self._log.append("FAIL: mandatory keywords are missing") 
        
        return result

    def _check_hdu_dimensions(self): 
        """Check HDU dimensions 

        Check the size of the data in each HDU and make sure it is consistent
        across. This function has to deal with missing HDUs, so can provide
        information even if other tests have failed. 

        """

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
                    result, log = dimension_check(dims, 4, hdu)
                    if result: 
                        frames.append(dims[0])
                        wavelengths.append(dims[1])
                        pixels.append(dims[2]) 
                        pixels.append(dims[3]) 
                    else:
                        self._log.append(log) 
                
                #Aperture (N_apertures x 3) 
                if hdu == "APERTURE": 
                    result, log = dimension_check(dims, 2, hdu)
                    if result and dims[1] == 3: 
                        apertures.append(dims[0])
                    else: 
                        self._log.append(
                            "FAIL: APERTURE HDU has incorrect dimensions"
                            )

                #UV-points (N_UV x 3) 
                if hdu == "UV-PLANE": 
                    result, log = dimension_check(dims, 2, hdu)
                    if result and dims[1] == 3: 
                        uv_points.append(dims[0])
                    else: 
                        self._log.append(
                            "FAIL: UV-PLANE HDU has incorrect dimensions"
                            )
                    
                #KER-MAT (N_KER x N_UV) 
                if hdu == "KER-MAT":
                    result, log = dimension_check(dims, 2, hdu)
                    if result: 
                        kernels.append(dims[0])
                        uv_points.append(dims[1]) 
                    else:
                        self._log.append(log) 

                #BLM-MAT (N_UV x N_AP) 
                if hdu == "BLM-MAT": 
                    result, log = dimension_check(dims, 2, hdu)
                    if result:  
                       uv_points.append(dims[0]) 
                       apertures.append(dims[1])
                    else:
                        self._log.append(log) 
                
                #KP-DATA (N_FRAMES x N_WAVE x N_KER) 
                if hdu == "KP-DATA": 
                    result, log = dimension_check(dims, 3, hdu)
                    if result:                    
                        frames.append(dims[0])
                        wavelengths.append(dims[1])
                        kernels.append(dims[2]) 
                    else:
                        self._log.append(log) 

                #KP-SIGM (N_FRAMES x N_WAVE x N_KER) 
                if hdu == "KP-SIGM": 
                    result, log = dimension_check(dims, 3, hdu)
                    if result: 
                        frames.append(dims[0])
                        wavelengths.append(dims[1])
                        kernels.append(dims[2]) 
                    else:
                        self._log.append(log) 

                if hdu == "CWAVEL": 
                    result, log = dimension_check(dims, 2, hdu)
                    if result and dims[1] == 2: 
                        wavelengths.append(dims[0]) 
                    else:
                        self._log.append(log) 

                if hdu == "DEPTA":
                    result, log = dimension_check(dims, 2, hdu)
                    if result:
                        frames.append(dims[0]) 
                    else:
                        self._log.append(log) 

                if hdu == "CVIS-DATA": 
                    result, log = dimension_check(dims, 4, hdu)
                    if result and dims[0] == 2: 
                        frames.append(dims[1])
                        wavelengths.append(dims[2])
                        uv_points.append(dims[3])
                    else:
                        self._log.append(log) 

                if hdu == "KA-DATA": 
                    result, log = dimension_check(dims, 3, hdu)
                    if result: 
                        frames.append(dims[0])
                        wavelengths.append(dims[1])
                        kernels.append(dims[2]) 
                    else:
                        self._log.append(log) 
                   
                if hdu == "KA-SIGM": 
                    result, log = dimension_check(dims, 3, hdu)
                    if result: 
                        frames.append(dims[0])
                        wavelengths.append(dims[1])
                        kernels.append(dims[2]) 
                    else:
                        self._log.append(log) 

                if hdu == "CAL-MAT":
                    result, log = dimension_check(dims, 2, hdu)
                    if result: 
                        kernels.append(dims[1]) 
                    else:
                        self._log.append(log) 

                if hdu == "IMSHIFT": 
                    result, log = dimension_check(dims, 2, hdu)
                    if result: 
                        frames.append(dims[0]) 
                    else:
                        self._log.append(log) 

        #!TODO: remove check_unique from function class 

        #Now check that the items in each list are the same
        self._check_unique(kernels, "kernels") 
        self._check_unique(frames, "frames") 
        self._check_unique(pixels, "pixels") 
        self._check_unique(wavelengths, "wavelengths") 
        self._check_unique(uv_points, "uv-points") 

        #Check the number of apertures separately 
        unique_ap = list(set(apertures))
        if len(unique_ap) == 2:
            if abs(unique_ap[0] - unique_ap[1]) == 1:        
                self._log.append("PASS: Number of apertures is consistent")
            else:
                self._log.append("FAIL: Number of apertures is inconsistent") 
                self._log.appned(apertures) 
        
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
        check4 = self._check_primary_header() 

        #List of non-mandatory checks
        self._check_all_hdu_names() 

        #Display the results
        for item in self._log:
            print(item)  

        if check1 and check2 and check3 and check4: 
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
            #check if it's the primary HDU
            if ext_info["extnum"] == 0:
                name = "PRIMARY"
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

    

