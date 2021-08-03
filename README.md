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

kp_fits % python validate.py V410Tau_kpfile.fits
Validating V410Tau_kpfile.fits...
*** V410Tau_kpfile.fits ***
----------------------------
0 [6, 1, 192, 192]
APERTURE [105, 3]
UV-PLANE [204, 3]
KER-MAT [100, 204]
BLM-MAT [204, 104]
KP-DATA [6, 1, 100]
KP-SIGM [6, 1, 100, 100]
CWAVEL [1]
DETPA [6]
VIS-DATA [6, 1, 204]
----------------------------
PASS: all mandatory HDUs were found.
PASS: sufficient HDUs found.
PASS: Number of kernels is consistent
PASS: Number of frames is consistent
FAIL: Inconsistent number of apertures: 
[105, 104]
PASS: Number of wavelengths is consistent
PASS: Number of uv-points is consistent
WARNING: 0 is not a standard HDU name
