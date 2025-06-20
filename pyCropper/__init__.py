from .A_DEPENDENCIES import runConstants as _runConstants, RunMode
print("Initializing the Cropper package")
if _runConstants.RUNMODE == RunMode.TEST:
	print("In a test run!")
	import A_DEPENDENCIES
	import B_DESCRIPTORS
	import C_CLASSES_UTILITY
	import D_CONSTANTS
	from D_CONSTANTS import userConstants
	import E_FUNC_UTIL
	import G_CLASSES_CV2
	from G_CLASSES_CV2 import FolderProcessor
 
else:
	from . import A_DEPENDENCIES
	from . import B_DESCRIPTORS
	from . import C_CLASSES_UTILITY
	from . import D_CONSTANTS
	from .D_CONSTANTS import userConstants
	from . import E_FUNC_UTIL
	from . import G_CLASSES_CV2
	from .G_CLASSES_CV2 import FolderProcessor

