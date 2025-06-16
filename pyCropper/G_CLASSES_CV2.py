from __future__ import annotations
if __name__ == "__main__":
	from A_DEPENDENCIES import runConstants, RunMode
	runConstants.RUNMODE = RunMode.TEST

if runConstants.RUNMODE == RunMode.TEST:
	from A_DEPENDENCIES import allowedFileTypes, screenX, screenY, TkinterActions, signal, signal_handler, ClickStates
	from A_DEPENDENCIES import aPoint, aCorners
	from A_DEPENDENCIES import os, cv2, typing
	from A_DEPENDENCIES import Image, ImageTk, tk

	from A_DEPENDENCIES import Path, ImageOrientation
	from A_DEPENDENCIES import aShape, cv2Image
	from D_CONSTANTS import userConstants
	import B_DESCRIPTORS
	from C_CLASSES_UTILITY import Picklable
	import E_FUNCTIONS_UTILITY
	import F_FUNCTIONS_GEOMETRY


else:
	from .A_DEPENDENCIES import allowedFileTypes, screenX, screenY, TkinterActions, signal, signal_handler, ClickStates
	from .A_DEPENDENCIES import aPoint, aCorners
	from .A_DEPENDENCIES import os, cv2, typing
	from .A_DEPENDENCIES import Path, ImageOrientation
	from .A_DEPENDENCIES import Image, ImageTk, tk

	from .A_DEPENDENCIES import aShape, cv2Image
	from .D_CONSTANTS import userConstants
	from . import B_DESCRIPTORS
	from .C_CLASSES_UTILITY import Picklable
	from . import E_FUNCTIONS_UTILITY
	from . import F_FUNCTIONS_GEOMETRY



class ImageWrapper(Picklable, B_DESCRIPTORS.ImageWrapperTYPECHECK):
	_pickleSuffix = ".imgW"
	image: cv2Image

	@property
	def shape(self) -> aShape: return self.image.shape

	@property
	def colorChannels(self) -> int: return self.shape[2]

	@property
	def x(self) -> int: return self.shape[1]

	@property
	def y(self) -> int: return self.shape[0]

	@property
	def ARfloat(self) -> float: return self.x/self.y if self.x < self.y else round(self.y/self.x, 6)

	@property
	def ARstr(self) -> str: return f"{self.x}:{self.y}" if self.x < self.y else f"{self.y}:{self.x}"


	@property
	def xScaleScreen(self) -> float: return self.x/screenX

	@property
	def yScaleScreen(self) -> float: return self.y/screenY

	@property
	def scaleScreenFactor(self) -> float: return 1.0 / max(self.xScaleScreen, self.yScaleScreen)

	imageOrigOrientation: ImageOrientation		= B_DESCRIPTORS.ImageOrienter(name="imageOrigOrientation", getFromAttr="image")

	def __init__(self, image: cv2Image, screenScale: typing.Optional[float] = 0.75):
		super().__init__()
		self.image = image
		self.screenScale = screenScale

		self._scaleX_orig = self.x/screenX
		self._scaleY_orig = self.y/screenY

		self._origSizeX = self.x
		self._origSizeY = self.y

	@classmethod
	def readImage(cls, filePath: Path) -> ImageWrapper:
		if not os.path.exists(filePath):
			raise FileNotFoundError(f"{cls.__name__}.readImage: attempting to read an image from a non-existent address {filePath}")
		readImage: cv2Image = cv2.imread(filename=filePath)
		nuInstance = cls(readImage)
		return nuInstance

	def __array__(self, dtype=None) -> cv2Image:
		if self.image: return self.image
		else: raise ValueError(f"{self}: something is trying to access the {self}.image attribute, which is not implemented, through the __array__ method")

	def __getitem__(self, key: typing.Union[int, slice, typing.Tuple[int,...]]) -> cv2Image:
		return self.image[key]

	@property
	def shape(self) -> aShape: return self.image.shape

	def transform(self) -> None:
		prevTransform = self.imageOrigOrientation

		self.image= self.image.transpose(1,0,2)
		if self.imageOrigOrientation == ImageOrientation.LANDSCAPE:
			self.image = cv2.flip(self.image, 1)
		else: self.image= cv2.flip(self.image, 0)
		print(f"{self}: transformed image from {prevTransform} to {self.imageOrigOrientation}")

	@property
	def fittedCoords(self) -> tuple[int, int]:
		newX	= self.scaleScreenFactor * self.x
		newY	= self.scaleScreenFactor * self.y
		return newX, newY

	def getScaledCoords(self, scaleFactor: float) -> typing.Tuple[int, int]:
		return tuple([int(round(scaleFactor * _, 0)) for _ in self.fittedCoords])
 
	def fitToScreen(self) -> None:
		self.image		= cv2.resize(
			src=self.image,
			dsize=self.getScaledCoords(self.screenScale)
		)
	

	def __str__(self) -> str:
		return f"<{self.__class__.__name__}(x={self.x}, y={self.y}, channels={self.colorChannels}) @ {hex(id(self))}>"

class ImageHandler(Picklable):
	_pickleSuffix = ".imgH"


	imagePath: Path	= B_DESCRIPTORS.ValidPathDescriptor(name="imagePath")

	imageOrig:		ImageWrapper
	imagePreview: 	ImageWrapper


	def __init__(self, filePath: Path, screenScale: typing.Optional[float] = 0.75):
		self.screenScale = screenScale
		self.imagePath = filePath
		self.imageOrig = ImageWrapper.readImage(filePath=filePath)

		self.imagePreview =  ImageWrapper(image=	cv2.resize(	src=self.imageOrig.image.copy(),
													dsize=self.imageOrig.getScaledCoords(scaleFactor=screenScale),
													fx=userConstants.DISPLAY_SCALE,
													fy=userConstants.DISPLAY_SCALE)
		)


	def transposePreview(self) -> None: self.imagePreview.transform()

	def transposeImage(self) -> None: self.imageOrig.transform()

	def transpose(self) -> None:
		self.transposePreview()
		self.transposeImage()

	def fitPreview(self) -> None: self.imagePreview.fitToScreen()

	@property
	def aspectRatio(self) -> float:
		if self.imageOrig.imageOrigOrientation == ImageOrientation.LANDSCAPE: returnValue= self.imageOrig.x/self.imageOrig.y
		else: returnValue= self.imageOrig.y/self.imageOrig.x
		return round(returnValue, 5)

class Displayer(Picklable):
	mousePos: typing.Optional[aPoint] = None
	corner_1: typing.Optional[aPoint] = None
	corner_2: typing.Optional[aPoint] = None
	croppingAllowed: bool
	clickState: ClickStates

	@property
	def rectangleCorners(self) -> aCorners:
		if self.corner_1 and self.corner_2: return [self.corner_1, self.corner_2]
		if self.corner_1 and not self.corner_2: return [self.corner_1]
		return []

	def __init__(	self, handler: ImageHandler,
					screenName: typing.Optional[str] = "Cropper.py",
		screenScale: typing.Optional[float]=0.75
		) -> None:
		super().__init__()
		self.handler			= handler
		self.screenName			= screenName
		self.croppingAllowed	= False
		AR = max(userConstants.WIDTH_SCALE, userConstants.HEIGHT_SCALE), min(userConstants.WIDTH_SCALE, userConstants.HEIGHT_SCALE)

		self.targetAR			= AR if self.handler.imageOrig.imageOrigOrientation == ImageOrientation.LANDSCAPE else AR[::-1]

		self.clickState			= ClickStates.NOTHING
		self.screenScale		= screenScale

	def initRender(self) -> None:
		cv2.namedWindow(winname=self.screenName)
		cv2.moveWindow(winname=self.screenName, x=0, y=0)
		cv2.setMouseCallback(self.screenName, self.__class__.clickAndCrop, param=self)


	def renderImg(self) -> None:
		self.initRender()
		cornersPreview = None
		while not (cv2.getWindowProperty(self.screenName, cv2.WND_PROP_VISIBLE) < 1):

			self.handler.imagePreview = ImageWrapper(
				cv2.resize(	src=self.handler.imageOrig.image.copy(),
								dsize=self.handler.imageOrig.getScaledCoords(scaleFactor=screenScale),
								fx=userConstants.DISPLAY_SCALE,
								fy=userConstants.DISPLAY_SCALE)
			)

			try:
				self.handler.fitPreview()

				if self.croppingAllowed and len(self.rectangleCorners) == 1:
					adjusted_end	= F_FUNCTIONS_GEOMETRY.movePointByAspectRatio(self.corner_1, self.mousePos, artup=self.targetAR)
					cornersPreview		= (	F_FUNCTIONS_GEOMETRY.scalePoint(self.corner_1, 1),
											F_FUNCTIONS_GEOMETRY.scalePoint(adjusted_end, 1))

				elif len(self.rectangleCorners) == 2:
					cornersPreview = 		(	F_FUNCTIONS_GEOMETRY.scalePoint(self.corner_1, 1), 
												F_FUNCTIONS_GEOMETRY.scalePoint(self.corner_2, 1))
				else: cornersPreview = None

				if E_FUNCTIONS_UTILITY.checkExistenceAndLength(variable=cornersPreview, length=2):
					F_FUNCTIONS_GEOMETRY.greenInfo(imageOrientation=self.handler.imagePreview.imageOrigOrientation, disp=self.handler.imagePreview.image, corners=cornersPreview)
		
				cv2.imshow(winname=self.screenName, mat=self.handler.imagePreview.image)
				key = cv2.waitKey(1) & 0xFF

				if key in E_FUNCTIONS_UTILITY.ords('t'):
					self.handler.transpose()

					AR = max(userConstants.HEIGHT_SCALE, userConstants.WIDTH_SCALE), min(userConstants.HEIGHT_SCALE, userConstants.WIDTH_SCALE)
					self.targetAR = AR if self.handler.imagePreview.imageOrigOrientation == ImageOrientation.LANDSCAPE else AR[::-1]


				elif key in E_FUNCTIONS_UTILITY.ords('i'):
					print(f"\tINVERTING SELLECTION")
					self.targetAR = tuple(self.targetAR[::-1])

			except KeyboardInterrupt:
				print("Interupting via ctrl-c")
				print("*"*40)
				exit()
		else:
			print("Interupting via window shutdown")
			print("*"*4)
			exit(1)

	def clickAndCrop(event: int, x: int, y: int, flags: int, param: Displayer) -> None:
		self: Displayer	= param
		self.mousePos	= (x,y)

		unscaledPoint = F_FUNCTIONS_GEOMETRY.unscalePoint(self.mousePos, self.handler.aspectRatio/self.screenScale)
		unscaledPoint = self.mousePos
		if event == cv2.EVENT_LBUTTONDOWN:
			print(f"click {self.clickState.value}, {self.targetAR}: {self.mousePos} -> {unscaledPoint}", self.handler.imagePreview.shape)
			if self.clickState == ClickStates.NOTHING:
				self.corner_1			= unscaledPoint
				self.croppingAllowed	= True
				self.clickState			= ClickStates.FIRST

			elif self.clickState == ClickStates.FIRST:
				self.croppingAllowed	= False
				self.corner_2			= F_FUNCTIONS_GEOMETRY.movePointByAspectRatio(	start=self.corner_1,
																						end=unscaledPoint,
																						artup=self.targetAR)
				self.clickState = ClickStates.BOTH

			else: print("No more clicking", self.handler.imagePreview.shape)

		elif event == cv2.EVENT_MBUTTONDOWN:
			print("Resetting the point array")
			self.clickState			= ClickStates.NOTHING
			self.croppingAllowed	= False
			self.rectangleCorners.clear()
			self.corner_1 = None
			self.corner_2 = None

		elif event == cv2.EVENT_MOUSEMOVE and self.croppingAllowed:
			self.mousePos = unscaledPoint


if __name__ == "__main__":
	print("*"*40)
	print(f"Starting the test run for {os.path.basename(__file__)}")
	winName: str = "testPreview"

	testImgFolder	= Path(os.path.join(E_FUNCTIONS_UTILITY.getFileSuperfolder(__file__), "testImages"))
	testImgPath		= E_FUNCTIONS_UTILITY.getPicsInDirectory(testImgFolder)[0]

	screenScale 	= 1.0
	imgHandler		= ImageHandler(filePath=testImgPath,screenScale=screenScale)
	displayer		= Displayer(handler=imgHandler, screenScale=screenScale)
	displayer.renderImg()