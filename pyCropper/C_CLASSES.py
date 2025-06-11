from __future__ import annotations
from .A_DEPENDENCIES import typing,os

from . import A_DEPENDENCIES
from . import B_DESCRIPTORS


class Constants(object):
	_instance: typing.Optional[Constants] = None
	
	def __new__(cls, *args, **kwargs) -> Constants:
		"""Ensures the returned Constants instance is a singleton.

		Returns:
			Constants: a pointer to the new singleton Constants instance
		"""
		if cls._instance is None:
			"""Ensures the returned Constants instance is a singleton.

			Returns:
				typing.Self: a pointer to the new singleton Constants instance
			"""
			cls._instance = super().__new__(cls)
			cls._instance.__dict__.update(kwargs)
		return cls._instance

	def __str__(self) -> str:
		returnStr = f"{self.__class__.__name__} @ {hex(id(self))}\n"
		for argument,value in self.__dict__.items():
			returnStr += f"\t{argument.ljust(24, ' ')}= <{value}: {type(value)}>\n"
		return returnStr

class UserConstants(Constants):
	FROM_FOLDER: A_DEPENDENCIES.Path	= B_DESCRIPTORS.WriteOnce_CreatePath(name="FROM_FOLDER")
	CROPPED_FOLDER: A_DEPENDENCIES.Path	= B_DESCRIPTORS.WriteOnce_CreatePath(name="CROPPED_FOLDER")
	MINIMUM_PIXELS: int					= B_DESCRIPTORS.WriteOnce_UnsignedInteger(name="MINIMUM_PIXELS")

	WIDTH_SCALE: int				= B_DESCRIPTORS.WriteOnce_UnsignedInteger(name="WIDTH_SCALE")
	HEIGHT_SCALE: int				= B_DESCRIPTORS.WriteOnce_UnsignedInteger(name="HEIGHT_SCALE")
	DISPLAY_SCALE: float			= B_DESCRIPTORS.WriteOnce_RangedFloat(name="DISPLAY_SCALE", minimum=0.05, maximum=float("inf"))

	IMAGE_TYPE: str					= B_DESCRIPTORS.WriteOnce_String(name="IMAGE_TYPE")
	JPG_QUALITY: int				= B_DESCRIPTORS.WriteOnce_RangedInt(name="JPG_QUALITY", minimum=10, maximum=100)
	PNG_QUALITY: int				= B_DESCRIPTORS.WriteOnce_RangedInt(name="PNG_QUALITY", minimum=1, maximum=10)

	MINIMUM_DIAGONAL_SIZE_SQUARED: int = B_DESCRIPTORS.WriteOnce_UnsignedInteger(name="MINIMUM_DIAGONAL_SIZE_SQUARED")

	def __init__(		self,
						fromFolder:	typing.Optional[A_DEPENDENCIES.Path]=	os.path.dirname(os.path.dirname(__file__)), 
						toFolder:	typing.Optional[A_DEPENDENCIES.Path]=	os.path.join(os.path.dirname(os.path.dirname(__file__)), "CROPPED"), 
						minimumPixels:	typing.Optional[int]=				360, 
						widthScale:		typing.Optional[int]=				4, 
						heightScale:	typing.Optional[int]=				3, 
						displayScale:	typing.Optional[float]=				0.25, 
						imageType:		typing.Optional[str]=				"JPG", 
						JPG_quality:	typing.Optional[int]=				95, 
						PNG_quality:	typing.Optional[int]=				5
	) -> None:
		super().__init__()
		self.FROM_FOLDER = fromFolder
		self.CROPPED_FOLDER = toFolder
		self.MINIMUM_PIXELS = minimumPixels
		self.WIDTH_SCALE = widthScale
		self.HEIGHT_SCALE = heightScale
		self.DISPLAY_SCALE = displayScale
		self.IMAGE_TYPE = imageType
		self.JPG_QUALITY = JPG_quality
		self.PNG_QUALITY = PNG_quality
		self.MINIMUM_DIAGONAL_SIZE_SQUARED = (int(round(self.DISPLAY_SCALE*self.MINIMUM_PIXELS,0)))**2
		print(self.FROM_FOLDER, self.CROPPED_FOLDER)

	def __str__(self) -> str:
		returnStr = f"{self.__class__.__name__} @ {hex(id(self))}\n"
		for argument,value in self.__dict__.items():
			returnStr += f"\t{argument.ljust(24, ' ')}= <{value}: {type(value)}>\n"
		return returnStr


class ControlConstants(Constants):
	CLICK_COUNT: int = 0
	AR_EXPONENT: int = 1

	MOUSE_XY:typing.Tuple[int,int] = (0,0)
	RELATIVE_TEXT_OFFSET:float = B_DESCRIPTORS.RangedNumber(name="RELATIVE_TEXT_OFFSET", minimum=0.0, maximum=1.00)
	RECT_CORNERS:A_DEPENDENCIES.aCorners = []

	CROPPING_ALLOWED: bool = False
	SKIP: bool = False
	EXIT: bool = False
	TRANSPOSE: bool = False
	FIRSTTRY: bool = True

	LANDSCAPE: bool = True



class IndexedCycle(typing.Generic[A_DEPENDENCIES.T]):
	_sequence: typing.Sequence[A_DEPENDENCIES.T]
	_index: int

	def __init__(self, sequence: typing.Sequence[A_DEPENDENCIES.T]) -> None:
		self._sequence = sequence
		self._index = -1

	def __len__(self) -> int: return len(self._sequence)
 
	def __next__(self) -> A_DEPENDENCIES.T:
		self._index = (self._index + 1) % len(self._sequence)
		return self._sequence[self._index]

	def previous(self) -> A_DEPENDENCIES.T:
		self._index = (self._index - 1) % len(self._sequence)
		return self._sequence[self._index]

	def __getitem__(self, index: int) -> A_DEPENDENCIES.T:
		self._index = index
		return self._sequence[self._index]

	def __repr__(self) -> str: return f"{self._sequence}"




class ImageType(A_DEPENDENCIES.Enum):
	JPG = "jpg"
	PNG = "png"
