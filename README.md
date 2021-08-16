# Kernel Phase Standard Data Format
Temporary repository to hold information about the kernel phase fits file format and a data validator. The kernel phase FITS file format is designed to be a common data exchange format among researchers interested in kernel phase observations (Martinache 2010). The data format is modelled on the XARA data structured, developed by Frantz Martinache. The format contains several mandatory HDUs, which are needed to reconstrunct the kernel phases, as well as several optional ones which are helpful for calibration and down-stream processing.

The validation code performs the following checks:
1. Checks the number of HDUs (fails if less than 7)
2. Check that all the required HDUs are present 
3. Check that the required HDUs have a consistent size 

TODO: 
- Finish the HDU consistency tests for the current validation format 
- Select and add a number of 'random' fits file to use for testing
- Add an end-to-end unit test on each of the files

#### Example:
```
kp_fits % python dummyfile.py test.fits

kp_fits % python validate.py test.fits 

Validating test.fits...

*** test.fits ***
------------------
PRIMARY [9, 4, 16, 16]
APERTURE [352, 3]
UV-PLANE [153, 3]
KER-MAT [499, 153]
BLM-MAT [153, 352]
KP-DATA [9, 4, 499]
KP-SIGM [9, 4, 499]
CWAVEL [4, 2]
DETPA [9]
VIS-DATA [9, 4, 153]
KA-DATA [9, 4, 499]
KA-SIGM [9, 4, 499]
CAL-MAT [5, 499]
KP-COV [9, 4, 499, 499]
KA-COV [9, 4, 499, 499]
FULL-COV [9, 4, 2, 499, 2, 499]
IMSHIFT [9, 2]
------------------
PASS: all mandatory HDUs were found.
PASS: sufficient HDUs found.
PASS: Number of kernels is consistent
PASS: Number of frames is consistent
PASS: Number of pixels is consistent
PASS: Number of wavelengths is consistent
PASS: Number of uv-points is consistent
PASS: mandatory keywords present in PRIMARY HDU
```
