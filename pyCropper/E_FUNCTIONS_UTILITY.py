try: from A_DEPENDENCIES import runConstants, RunMode
except: from .A_DEPENDENCIES import runConstants, RunMode

if runConstants.RUNMODE== RunMode.TEST:
	from A_DEPENDENCIES import typing, os, Path, allowedFileTypes, cv2, ImageOrientation
	from A_DEPENDENCIES import aColour, aPoint, aCorners, cv2Image
	from C_CLASSES_UTILITY import IndexedCycle
	from D_CONSTANTS import userConstants

else:
	from .A_DEPENDENCIES import typing, os, Path, allowedFileTypes, cv2, ImageOrientation
	from .A_DEPENDENCIES import aColour, aPoint,aCorners,  cv2Image
	from .C_CLASSES_UTILITY import IndexedCycle
	from .D_CONSTANTS import userConstants


getFileNameWoSuffix:	typing.Callable[[Path], str]			= lambda file: os.path.splitext(os.path.basename(file))[0]
getFileSuffix:			typing.Callable[[Path], str]			= lambda file: os.path.splitext(file)[1]
getFileSuperfolder:		typing.Callable[[Path], Path]			= lambda file: os.path.dirname(os.path.dirname(file))

getPicsInDirectory:				typing.Callable[[Path], typing.Sequence[Path]]		= lambda workDir=userConstants.FROM_FOLDER: [Path(os.path.join(workDir, file)) for file in os.listdir(workDir) if getFileSuffix(file).lower() in allowedFileTypes]
getCycledPicsInDirectory:		typing.Callable[[Path], IndexedCycle[Path]]			= lambda workDir=userConstants.FROM_FOLDER:  IndexedCycle(getPicsInDirectory(workDir))
ords:							typing.Callable[[str], typing.Tuple[int,int]]		= lambda ipt: (ord(ipt.lower()), ord(ipt.upper()))

def checkExistenceAndLength(variable: any, length: int) -> bool:
	if variable:
		if len(variable) == length:
			return True
		return False
	return False



green:	typing.Callable[[ImageOrientation], aColour]= lambda mode: (0,255,0) if mode == ImageOrientation.LANDSCAPE else (0,127,0)
red:	typing.Callable[[ImageOrientation], aColour]= lambda mode: (0,0,255) if mode == ImageOrientation.LANDSCAPE else (0,0,127)

greenRectangle:		typing.Callable[[ImageOrientation, cv2Image, aPoint, aPoint], cv2Image]	= lambda ORIENT, DISP, PT1, PT2: cv2.rectangle(DISP, PT1, PT2, green(ORIENT), 2)
redRectangle:		typing.Callable[[ImageOrientation, cv2Image, aPoint, aPoint], cv2Image]	= lambda ORIENT, DISP, PT1, PT2: cv2.rectangle(DISP, PT1, PT2, red(ORIENT), 2)
redText:			typing.Callable[[ImageOrientation, cv2Image, aPoint, str], cv2Image]	= lambda ORIENT, DISP, PT, text: cv2.putText(DISP, text, PT, cv2.FONT_HERSHEY_COMPLEX, 0.5, red(ORIENT))
greenText:			typing.Callable[[ImageOrientation, cv2Image, aPoint, str], cv2Image]	= lambda ORIENT, DISP, PT, text: cv2.putText(DISP, text, PT, cv2.FONT_HERSHEY_COMPLEX, 0.5, green(ORIENT))
