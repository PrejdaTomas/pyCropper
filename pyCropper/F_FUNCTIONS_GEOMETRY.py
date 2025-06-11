from .A_DEPENDENCIES import Number, typing
from .A_DEPENDENCIES import aPoint, aColour, aCorners

from .D_CONSTANTS import userConstants, controlConstants


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
