try: from A_DEPENDENCIES import runConstants, RunMode
except: from .A_DEPENDENCIES import runConstants, RunMode

if runConstants.RUNMODE== RunMode.TEST:
	from A_DEPENDENCIES import Number, typing
	from A_DEPENDENCIES import aPoint, aColour, aCorners,cv2Image, ImageOrientation
	from D_CONSTANTS import userConstants, controlConstants
	import E_FUNCTIONS_UTILITY

else:
	from .A_DEPENDENCIES import Number, typing
	from .A_DEPENDENCIES import aPoint, aColour, aCorners,cv2Image, ImageOrientation
	from .D_CONSTANTS import userConstants, controlConstants
	from . import E_FUNCTIONS_UTILITY

ASPECT_RATIO:					typing.Callable[[Number, Number], float]	= lambda dx=userConstants.WIDTH_SCALE, dy=userConstants.HEIGHT_SCALE: (dx / dy)**controlConstants.AR_EXPONENT



getWidth:								typing.Callable[[Number, Number], float]	= lambda height, AR: float(abs(AR * height))
getHeight:								typing.Callable[[Number, Number], float]	= lambda width, AR: float(abs(width / AR))
getSign:								typing.Callable[[Number], int]				= lambda value: 1 if value >= 0 else -1
realWidthLargerThanCalculatedWidth:		typing.Callable[[Number, Number], bool]		= lambda real, calculated: abs(real) > abs(calculated)

def getWidthHeightFromAR(width: Number, height: Number, aspectRatio: Number) -> typing.Tuple[float, float]:
	if realWidthLargerThanCalculatedWidth(real=width, calculated=getWidth(height, aspectRatio)):
		width = getSign(width) * getWidth(height, aspectRatio)
	else:
		height = getSign(height) * getHeight(width, aspectRatio)
	return width, height

def movePointByAspectRatio(start: aPoint, end: aPoint, artup: typing.Tuple[int,int] = False) -> aCorners:
	x0, y0	= start
	x1, y1	= end

	dx		= x1 - x0
	dy		= y1 - y0
	
	width, height = getWidthHeightFromAR(width=dx, height=dy, aspectRatio=ASPECT_RATIO(*artup))
	return (x0 + int(width), y0 + int(height))

def scalePoint(point: aPoint, scale: Number) -> aPoint:
	x, y = point
	return int(x * scale), int(y * scale)

def unscalePoint(point: aPoint, scale: Number) -> aPoint:
	x, y = point
	return int(x / scale), int(y / scale)

def getRectangleSizeSquared(corners: aCorners) -> int:
	(x0, y0), (x1, y1) = corners
	return (x1 - x0)**2 + (y1 - y0)**2

def selectionLargeEnough(corners: aCorners, diagonalPow2: int = userConstants.MINIMUM_DIAGONAL_SIZE_SQUARED) -> bool:
	return getRectangleSizeSquared(corners=corners) > diagonalPow2









def greenInfo(imageOrientation: ImageOrientation, disp: cv2Image, corners: aCorners) -> None:
	pt0, pt1 = corners

	pt0s		= unscalePoint(pt0, userConstants.DISPLAY_SCALE)
	pt1s		= unscalePoint(pt1, userConstants.DISPLAY_SCALE)

	center		= (		(pt0[0] + pt1[0]) // 2,
						(pt0[1] + pt1[1]) // 2
	)

	E_FUNCTIONS_UTILITY.greenRectangle(imageOrientation, disp, pt0, pt1)
	E_FUNCTIONS_UTILITY.greenText(imageOrientation, disp, (pt0[0], int(pt0[1] * (1 - controlConstants.RELATIVE_TEXT_OFFSET))), f"D{pt0}")
	E_FUNCTIONS_UTILITY.greenText(imageOrientation, disp, (pt0[0], int(pt0[1] * (1 - 4*controlConstants.RELATIVE_TEXT_OFFSET))), f"P{pt0s}")
 
	E_FUNCTIONS_UTILITY.greenText(imageOrientation, disp, center, f"OK")
 
	E_FUNCTIONS_UTILITY.greenText(imageOrientation, disp, (pt1[0], int(pt1[1] * (1 + controlConstants.RELATIVE_TEXT_OFFSET))), f"D{pt1}")
	E_FUNCTIONS_UTILITY.greenText(imageOrientation, disp, (pt1[0], int(pt1[1] * (1 + 2*controlConstants.RELATIVE_TEXT_OFFSET))), f"P{pt1s}")
 
def redWarning(imageOrientation: ImageOrientation, disp: cv2Image, corners: aCorners) -> None:
	pt0, pt1 = corners

	pt0s		= unscalePoint(pt0, userConstants.DISPLAY_SCALE)
	pt1s		= unscalePoint(pt1, userConstants.DISPLAY_SCALE)

	center		= (		(pt0[0] + pt1[0]) // 2,
						(pt0[1] + pt1[1]) // 2
	)

	E_FUNCTIONS_UTILITY.redRectangle(imageOrientation, disp, pt0, pt1)
	E_FUNCTIONS_UTILITY.redText(imageOrientation, disp, (pt0[0], int(pt0[1] * (1 - controlConstants.RELATIVE_TEXT_OFFSET))), f"D{pt0}")
	E_FUNCTIONS_UTILITY.redText(imageOrientation, disp, (pt0[0], int(pt0[1] * (1 - 4*controlConstants.RELATIVE_TEXT_OFFSET))), f"P{pt0s}")
 
	E_FUNCTIONS_UTILITY.redText(imageOrientation, disp, center, f"TOO SMALL")
 
	E_FUNCTIONS_UTILITY.redText(imageOrientation, disp, (pt1[0], int(pt1[1] * (1 + controlConstants.RELATIVE_TEXT_OFFSET))), f"D{pt1}")
	E_FUNCTIONS_UTILITY.redText(imageOrientation, disp, (pt1[0], int(pt1[1] * (1 + 2*controlConstants.RELATIVE_TEXT_OFFSET))), f"P{pt1s}")