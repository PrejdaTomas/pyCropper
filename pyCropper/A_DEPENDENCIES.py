from __future__ import annotations
import os
import typing
from numbers import Number
from enum import Enum
import cv2
import numpy as np
import time
import ctypes
import argparse

aPoint		= typing.Tuple[Number, Number]
aCorners	= typing.Tuple[aPoint, aPoint]
aColour		= typing.Tuple[int,int,int]

T			= typing.TypeVar("T")

allowedFileTypes: typing.Sequence[str] = [".jpg", ".jpeg", ".png", ".bmp", ".jfif"]

class Path(str, os.PathLike):
	def __new__(cls, value: str) -> typing.Self:
		if len(value) > 260: raise ValueError(f"{cls.__name__}: {value} length exceeds 260 characters")
		return super(Path, cls).__new__(cls, value)

	def __setattr__(self, name: str, value: str) -> None:
		if not isinstance(value, str): raise TypeError("Value must be a string")
		if name == 'value' and len(value) >= 260: raise IOError(f"{self.__class__.__name__}: '{value}' -> length exceeds 260 characters")
		if name == 'value' and len(value) <= 0: raise IOError(f"{self.__class__.__name__}: '{value}' -> zero-length or negative lengthpath")

		super().__setattr__(name, value)

	def __fspath__(self) -> str:
		return str(self)



VALUE = typing.TypeVar('VALUE')
CLASS = typing.TypeVar('CLASS')


CV2_ESCAPE:		int = 27
CV2_LEFT:		int = 81
CV2_UP:			int = 82
CV2_RIGHT:		int = 83
CV2_DOWN:		int = 84
CV2_KEYS:		typing.Tuple[int, ...] = (CV2_ESCAPE, CV2_LEFT, CV2_RIGHT, CV2_UP, CV2_DOWN)