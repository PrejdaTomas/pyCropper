from .A_DEPENDENCIES import runConstants as _runConstants
print("Initializing the Cropper package")
if _runConstants.RUNMODE == RunMode.TEST:
	print("In a test run!")
	import A_DEPENDENCIES
	import B_DESCRIPTORS
	import C_CLASSES_UTILITY
	import D_CONSTANTS
	import E_FUNCTIONS_UTILITY
	import G_CLASSES_CV2
	import H_FUNCTIONS_CV2
 
from .A_DEPENDENCIES import aPoint, aColour, aCorners, aShape
from .A_DEPENDENCIES import Path
from .C_CLASSES_UTILITY import ImageType, RunMode
from .D_CONSTANTS import userConstants, controlConstants
from .E_FUNCTIONS_UTILITY import getPicsInDirectory
from .E_FUNCTIONS_UTILITY import getCycledPicsInDirectory
from .H_FUNCTIONS_CV2 import processImage
from .H_FUNCTIONS_CV2 import processImages


