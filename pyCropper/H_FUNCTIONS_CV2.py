from .A_DEPENDENCIES import typing, cv2, time, np, ctypes, os
from .A_DEPENDENCIES import aPoint, aCorners, aColour, Path, cv2Image, CV2_ESCAPE, CV2_KEYS
from . import C_CLASSES_UTILITY
from .D_CONSTANTS import userConstants, controlConstants
from . import E_FUNCTIONS_UTILITY
from . import F_FUNCTIONS_GEOMETRY

def clickAndCrop(event: int, x: int, y: int, flags: int, param: typing.Any) -> None:

	controlConstants.MOUSE_XY = (x,y)
	unscaled = F_FUNCTIONS_GEOMETRY.unscalePoint(controlConstants.MOUSE_XY, userConstants.DISPLAY_SCALE)

	if event == cv2.EVENT_LBUTTONDOWN:
		if controlConstants.CLICK_COUNT == 0:
			controlConstants.RECT_CORNERS = [unscaled]
			controlConstants.CROPPING_ALLOWED = True

		else:
			controlConstants.CROPPING_ALLOWED = False
			controlConstants.RECT_CORNERS.append(F_FUNCTIONS_GEOMETRY.movePointByAspectRatio(start=controlConstants.RECT_CORNERS[0], end=unscaled, artup=param))

			if F_FUNCTIONS_GEOMETRY.getRectangleSizeSquared(controlConstants.RECT_CORNERS) < userConstants.MINIMUM_DIAGONAL_SIZE_SQUARED:
				print("The size of the rectangle is too small.")
				controlConstants.CLICK_COUNT = -1

		controlConstants.CLICK_COUNT += 1

	elif event == cv2.EVENT_MBUTTONDOWN:
		print("Resetting the point array")
		controlConstants.CLICK_COUNT		= 0
		controlConstants.CROPPING_ALLOWED	= False
		controlConstants.RECT_CORNERS		= []

	elif event == cv2.EVENT_MOUSEMOVE and controlConstants.CROPPING_ALLOWED:
		controlConstants.MOUSE_XY = unscaled



green:	typing.Callable[[], aColour]= lambda: (0,255,0) if controlConstants.AR_EXPONENT == 1 else (0,127,0)
red:	typing.Callable[[], aColour]= lambda: (0,0,255) if controlConstants.AR_EXPONENT == 1 else (0,0,127)

greenRectangle:		typing.Callable[[cv2Image, aPoint, aPoint], cv2Image]	= lambda DISP, PT1, PT2: cv2.rectangle(DISP, PT1, PT2, green(), 2)
redRectangle:		typing.Callable[[cv2Image, aPoint, aPoint], cv2Image]	= lambda DISP, PT1, PT2: cv2.rectangle(DISP, PT1, PT2, red(), 2)
redText:			typing.Callable[[cv2Image, aPoint, str], cv2Image]		= lambda DISP, PT, text: cv2.putText(DISP, text, PT, cv2.FONT_HERSHEY_COMPLEX, 0.5, red())
greenText:			typing.Callable[[cv2Image, aPoint, str], cv2Image]		= lambda DISP, PT, text: cv2.putText(DISP, text, PT, cv2.FONT_HERSHEY_COMPLEX, 0.5, green())



arrow: typing.Callable[[cv2Image, aPoint, aPoint, aColour], cv2Image]= lambda DISP, PT1, PT2, COLOR=(0,0,0),THICKNESS=1: cv2.arrowedLine(	DISP, PT1,PT2,COLOR,THICKNESS)


def reset() -> None:
	print("Resetted the variables")
	controlConstants.CLICK_COUNT= 0
	controlConstants.AR_EXPONENT= 1

	controlConstants.MOUSE_XY= (0,0)
	controlConstants.RECT_CORNERS=[]

	controlConstants.CROPPING_ALLOWED = False
	controlConstants.SKIP = False
	controlConstants.EXIT = False
	controlConstants.TRANSPOSE = False
	controlConstants.FIRSTTRY = True

def continueProgram() -> None:
	cv2.destroyAllWindows()
	reset()

def terminateProgram() -> None:
	print("Shutting down gracefully")
	continueProgram()
	exit(1)



def greenInfo(disp: cv2Image, corners: aCorners) -> None:
	pt0, pt1 = corners

	pt0s		= F_FUNCTIONS_GEOMETRY.unscalePoint(pt0, userConstants.DISPLAY_SCALE)
	pt1s		= F_FUNCTIONS_GEOMETRY.unscalePoint(pt1, userConstants.DISPLAY_SCALE)

	center		= (		(pt0[0] + pt1[0]) // 2,
						(pt0[1] + pt1[1]) // 2
	)

	greenRectangle(disp, pt0, pt1)
	greenText(disp, (pt0[0], int(pt0[1] * (1 - controlConstants.RELATIVE_TEXT_OFFSET))), f"D{pt0}")
	greenText(disp, (pt0[0], int(pt0[1] * (1 - 4*controlConstants.RELATIVE_TEXT_OFFSET))), f"P{pt0s}")
 
	greenText(disp, center, f"OK")
 
	greenText(disp, (pt1[0], int(pt1[1] * (1 + controlConstants.RELATIVE_TEXT_OFFSET))), f"D{pt1}")
	greenText(disp, (pt1[0], int(pt1[1] * (1 + 2*controlConstants.RELATIVE_TEXT_OFFSET))), f"P{pt1s}")
 
def redWarning(disp: cv2Image, corners: aCorners) -> None:
	pt0, pt1 = corners

	pt0s		= F_FUNCTIONS_GEOMETRY.unscalePoint(pt0, userConstants.DISPLAY_SCALE)
	pt1s		= F_FUNCTIONS_GEOMETRY.unscalePoint(pt1, userConstants.DISPLAY_SCALE)

	center		= (		(pt0[0] + pt1[0]) // 2,
						(pt0[1] + pt1[1]) // 2
	)

	redRectangle(disp, pt0, pt1)
	redText(disp, (pt0[0], int(pt0[1] * (1 - controlConstants.RELATIVE_TEXT_OFFSET))), f"D{pt0}")
	redText(disp, (pt0[0], int(pt0[1] * (1 - 4*controlConstants.RELATIVE_TEXT_OFFSET))), f"P{pt0s}")
 
	redText(disp, center, f"TOO SMALL")
 
	redText(disp, (pt1[0], int(pt1[1] * (1 + controlConstants.RELATIVE_TEXT_OFFSET))), f"D{pt1}")
	redText(disp, (pt1[0], int(pt1[1] * (1 + 2*controlConstants.RELATIVE_TEXT_OFFSET))), f"P{pt1s}")
 

windowClosed:			typing.Callable[[object], bool]		= lambda window: cv2.getWindowProperty(window, cv2.WND_PROP_VISIBLE) < 1
printImageStatus: typing.Callable[[	str,
									cv2Image,
									bool,
									typing.Tuple[int,int]], None
								] = lambda lineStart,display,transpose,arTuple: print(	f"\t{lineStart}".ljust(24, ' '),
																								f"shape={display.shape}",
																								f"x={display.shape[1]}",
																								f"y={display.shape[0]}",
																								f"transpose={transpose}",
																								f"aspect ratio (image)={F_FUNCTIONS_GEOMETRY.ASPECT_RATIO(*(max(display.shape), min([_ for _ in display.shape if _ != min(display.shape)]))):.3F}",
																								f"aspect ratio (selector)={F_FUNCTIONS_GEOMETRY.ASPECT_RATIO(*arTuple):.3F}",
																								sep=", ")
def getCroppedCV2Img(	source: cv2Image,
						corners: aCorners = controlConstants.RECT_CORNERS) -> typing.Optional[cv2Image]:
	if len(corners) == 2:
		x0, y0 = corners[0]
		x1, y1 = corners[1]
		return source[y0:y1, x0:x1]  # Correct order: [rows, cols] = [y, x]
	return None

def applyMask(img: cv2Image, start: aPoint, end: aPoint, alpha=0.6) -> cv2Image:
	x1, y1 = max(0, min(start[0], end[0])), max(0, min(start[1], end[1]))
	x2, y2 = min(img.shape[1], max(start[0], end[0])), min(img.shape[0], max(start[1], end[1]))

	# Create dark overlay
	overlay	= img.copy()
	mask	= np.zeros_like(img, dtype=np.uint8)
	mask[:]	= (0, 0, 0)

	# Cut out the selected rectangle
	mask[y1:y2, x1:x2] = img[y1:y2, x1:x2]

	# Blend the overlay with the mask
	blended = cv2.addWeighted(src1=overlay, alpha=alpha, src2=mask, beta=1.0 - alpha, gamma=0.0)
	return blended

def processImage(imagePath: str, fileType=C_CLASSES_UTILITY.ImageType.JPG) -> cv2Image:
	#region declarations
	imageName: str
	copyName: str
	copyAddress: str
	imageTitle: str

	image: cv2Image
	clone: cv2Image
	landscape: cv2Image
	portrait: cv2Image
	display: cv2Image
	corners: aCorners

	arTup: typing.Tuple[int,int]
	screenX: int
	screenY: int
	cloneX: int
	cloneY: int

	normalAxes: typing.Tuple[int,int,int]
	invertedAxes: typing.Tuple[int,int,int]

	#endregion declarations 


	imageName	= E_FUNCTIONS_UTILITY.getFileNameWoSuffix(imagePath)
	copyName	= f"{imageName}_c.{fileType.value}"
	copyAddress	= Path(os.path.join(userConstants.FROM_FOLDER, userConstants.CROPPED_FOLDER, copyName))
	print(f"Processing", f"From: {imagePath}", f"Into: {copyAddress}", sep="\n\t", end="\n")

	imageTitle	= "Image"
	image		= cv2.imread(filename=imagePath)
	clone		= image.copy()

	screenY, screenX	= ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
	cloneY, cloneX		= clone.shape[:2]
	arTup				= (userConstants.HEIGHT_SCALE, userConstants.WIDTH_SCALE) if (cloneX > cloneY) else (userConstants.WIDTH_SCALE, userConstants.HEIGHT_SCALE)

	cv2.namedWindow(winname=imageTitle)
	cv2.setMouseCallback(imageTitle, clickAndCrop, arTup)
	
	controlConstants.TRANSPOSE = arTup[0] > arTup[1]
	printImageStatus(f"STARTING image {imageName}", clone, controlConstants.TRANSPOSE, arTup)

	normalAxes		= (0,1,2)
	invertedAxes	= (normalAxes[1],normalAxes[0],normalAxes[2])
	controlConstants.AR_EXPONENT = 1

	corners					= tuple((None,))
	controlConstants.FIRSTTRY, controlConstants.SKIP, controlConstants.EXIT	= True, False, False

	while (controlConstants.CLICK_COUNT < 2):

		if any((cloneX > screenX, cloneY > screenY)):
			landscape			= cv2.resize(src=clone.copy(), dsize=(0, 0), fx=userConstants.DISPLAY_SCALE, fy=userConstants.DISPLAY_SCALE)
			tmpDisplayScale		= userConstants.DISPLAY_SCALE

		else:
			landscape			= clone.copy()
			tmpDisplayScale		= 1.0

		transposed		= landscape.transpose(*invertedAxes)
		rotated			= cv2.flip(transposed, 1)
		portrait		= rotated

		display = landscape if not controlConstants.TRANSPOSE else portrait

		if controlConstants.FIRSTTRY:
			printImageStatus(f"DISPLAYING image {imageName}", display, controlConstants.TRANSPOSE, arTup)
			controlConstants.FIRSTTRY = not controlConstants.FIRSTTRY

		displayY, displayX	= display.shape[:2]
		arTup				= (userConstants.WIDTH_SCALE, userConstants.HEIGHT_SCALE) if (displayX > displayY) else (userConstants.HEIGHT_SCALE, userConstants.WIDTH_SCALE)


		controlConstants.LANDSCAPE = (arTup[0]>arTup[1])

		if controlConstants.CROPPING_ALLOWED and len(controlConstants.RECT_CORNERS) == 1:
			adjusted_end	= F_FUNCTIONS_GEOMETRY.movePointByAspectRatio(controlConstants.RECT_CORNERS[0], controlConstants.MOUSE_XY, artup=arTup)
			corners			= (	F_FUNCTIONS_GEOMETRY.scalePoint(controlConstants.RECT_CORNERS[0], tmpDisplayScale),
								F_FUNCTIONS_GEOMETRY.scalePoint(adjusted_end, tmpDisplayScale))

		elif len(controlConstants.RECT_CORNERS) == 2:
			corners = 		(F_FUNCTIONS_GEOMETRY.scalePoint(controlConstants.RECT_CORNERS[0], tmpDisplayScale), 
							F_FUNCTIONS_GEOMETRY.scalePoint(controlConstants.RECT_CORNERS[1], tmpDisplayScale))


		if len(controlConstants.RECT_CORNERS) > 0:
			if F_FUNCTIONS_GEOMETRY.selectionLargeEnough(corners=corners): greenInfo(display, corners)
			else:	redWarning(disp=display, corners=corners)

			display = applyMask(img=display,start=corners[0], end=corners[1], alpha=0.5)

			leftTopCorner = (corners[1][0], corners[0][1])
			greenText(		display,
							leftTopCorner,
							f"{userConstants.WIDTH_SCALE}:{userConstants.HEIGHT_SCALE}" if controlConstants.LANDSCAPE else f"{userConstants.HEIGHT_SCALE}:{userConstants.WIDTH_SCALE}")


		cv2.imshow(winname=imageTitle, mat=display)


		key = cv2.waitKey(1) & 0xFF

		if key in E_FUNCTIONS_UTILITY.ords('t'):
			controlConstants.TRANSPOSE = not controlConstants.TRANSPOSE
			printImageStatus(f"TRANSPOSING image {imageName}", display, controlConstants.TRANSPOSE, arTup)

		elif key in E_FUNCTIONS_UTILITY.ords('i'):
			print(f"\tINVERTING SELLECTION")
			controlConstants.AR_EXPONENT *= -1

		elif key in E_FUNCTIONS_UTILITY.ords('r'):
			print(f"\tROTATING SELLECTION")
			raise KeyboardInterrupt("ROTATION NOT IMPLEMENTED YET")

		elif key in E_FUNCTIONS_UTILITY.ords('v'):
			print(f"\tFLIPPING IMAGE VERTICALLY")
			raise KeyboardInterrupt("VERTICAL MIRRORING NOT IMPLEMENTED YET")

		elif key in E_FUNCTIONS_UTILITY.ords('v'):
			print(f"\tFLIPPING IMAGE HORIZONTALLY")
			raise KeyboardInterrupt("HORIZONTAL MIRRORING NOT IMPLEMENTED YET")


		elif key == CV2_ESCAPE:
			print("EXITING!")
			controlConstants.EXIT = True
			break

		elif windowClosed(imageTitle) or (key in CV2_KEYS):
			print(f"\tSKIPPING FOR {imagePath}")
			controlConstants.SKIP = True
			break
	

	croppedClone = None
	if not controlConstants.SKIP:
		croppedClone = getCroppedCV2Img(source=clone, corners=controlConstants.RECT_CORNERS)

		if croppedClone is not None:
			if		fileType == C_CLASSES_UTILITY.ImageType.JPG:	cv2.imwrite(filename=copyAddress, img=croppedClone, params=[int(cv2.IMWRITE_JPEG_QUALITY), userConstants.JPG_QUALITY])
			elif	fileType == C_CLASSES_UTILITY.ImageType.PNG:	cv2.imwrite(filename=copyAddress, img=croppedClone, params=[int(cv2.IMWRITE_PNG_COMPRESSION), userConstants.PNG_QUALITY])
			else:	raise TypeError(f"unsupported fileType: {fileType.value}= {type(fileType.value)}")

		else: 
			if not controlConstants.EXIT: raise KeyboardInterrupt("The program exited abnormally - no action was taken by the user but skipping was not selected anyways!")
			else: terminateProgram()

	print(f"Storing image: {copyAddress}\n")

	if controlConstants.EXIT: terminateProgram()
	else:  continueProgram()

	return croppedClone

def processImages(	workDir: typing.Optional[Path] = userConstants.FROM_FOLDER,
					outputImageType: typing.Optional[C_CLASSES_UTILITY.ImageType] = C_CLASSES_UTILITY.ImageType.JPG
	) -> typing.Sequence[cv2Image]:

	images = E_FUNCTIONS_UTILITY.getCycledPicsInDirectory(workDir)
	for image in images: processImage(imagePath=image, fileType=outputImageType)