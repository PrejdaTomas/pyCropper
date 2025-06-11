from .A_DEPENDENCIES import Number, typing, os
from . import A_DEPENDENCIES



# instance: The instance of the class where the descriptor is used.
# owner: The class where the descriptor is used.
# value: The value being assigned to the attribute.

class StringDescr:
	"""A descriptor protocol used for string assignments

	Raises:
		TypeError: raises an error if the assigned value is not an string
		ValueError: raises an error if the assigned value is string

	Returns:
		_type_: int: a string
	"""
	# instance: The instance of the class where the descriptor is used.
	# owner: The class where the descriptor is used.
	# value: The value being assigned to the attribute.

	def __init__(self, name: str = None) -> None:
		# name: The name of the attribute being managed by the descriptor.
		self.name = name

	def __get__(self, instance: A_DEPENDENCIES.CLASS, owner: typing.Type[A_DEPENDENCIES.CLASS]) -> str:
		return instance.__dict__[self.name]

	def __set__(self, instance: A_DEPENDENCIES.CLASS, value: int) -> None:
		if not isinstance(value, str):
			raise TypeError(f"{instance}: trying to set the {self.name} to a non-string value: {type(value)}={value}.")

		instance.__dict__[self.name] = value

	def __delete__(self, instance: A_DEPENDENCIES.CLASS) -> None:
		del instance.__dict__[self.name]



class CreatePathDescriptor:
	"""A descriptor protocol used for path properties within a e.g. Constants instance, creates non-existent paths.

	Raises:
		FileNotFoundError: raises an error if the used path does not exist

	Returns:
		_type_: A_CLASSES.Path
	"""
	# instance: The instance of the class where the descriptor is used.
	# owner: The class where the descriptor is used.
	# value: The value being assigned to the attribute.

	def __init__(self, name: str = None) -> None:
		# name: The name of the attribute being managed by the descriptor.
		self.name = name

	def __get__(self, instance: A_DEPENDENCIES.CLASS, owner: typing.Type[A_DEPENDENCIES.CLASS]) -> A_DEPENDENCIES.Path:
		if not os.path.exists(instance.__dict__[self.name]):
			os.makedirs(instance.__dict__[self.name], exist_ok=True)
		return instance.__dict__[self.name]

	def __set__(self, instance: A_DEPENDENCIES.CLASS, value: A_DEPENDENCIES.Path) -> None:
		if not os.path.exists(value):
			os.makedirs(value, exist_ok=True)
		instance.__dict__[self.name] = value

	def __delete__(self, instance: A_DEPENDENCIES.CLASS) -> None:
		del instance.__dict__[self.name]


class ValidPathDescriptor:
	"""A descriptor protocol used for path properties within a e.g. Constants instance, blocks using non-existent paths.

	Raises:
		FileNotFoundError: raises an error if the used path does not exist

	Returns:
		_type_: A_CLASSES.Path
	"""
	# instance: The instance of the class where the descriptor is used.
	# owner: The class where the descriptor is used.
	# value: The value being assigned to the attribute.

	def __init__(self, name: str = None) -> None:
		# name: The name of the attribute being managed by the descriptor.
		self.name = name

	def __get__(self, instance: A_DEPENDENCIES.CLASS, owner: typing.Type[A_DEPENDENCIES.CLASS]) -> A_DEPENDENCIES.Path:
		return instance.__dict__[self.name]

	def __set__(self, instance: A_DEPENDENCIES.CLASS, value: A_DEPENDENCIES.Path) -> None:
		if not os.path.exists(value):
			raise FileNotFoundError(f"{instance}: trying to set the {self.name} to a non-existent path: {value}.")
		instance.__dict__[self.name] = value

	def __delete__(self, instance: A_DEPENDENCIES.CLASS) -> None:
		del instance.__dict__[self.name]





class UnsignedInteger:
	"""A descriptor protocol used for unsigned integer assignments

	Raises:
		TypeError: raises an error if the assigned value is not an integer
		ValueError: raises an error if the assigned value is negative

	Returns:
		_type_: int: an unsigned integer
	"""
	# instance: The instance of the class where the descriptor is used.
	# owner: The class where the descriptor is used.
	# value: The value being assigned to the attribute.

	def __init__(self, name: str = None) -> None:
		# name: The name of the attribute being managed by the descriptor.
		self.name = name

	def __get__(self, instance: A_DEPENDENCIES.CLASS, owner: typing.Type[A_DEPENDENCIES.CLASS]) -> int:
		return instance.__dict__[self.name]

	def __set__(self, instance: A_DEPENDENCIES.CLASS, value: int) -> None:
		if not isinstance(value, int):
			raise TypeError(f"{instance}: trying to set the {self.name} to a floating point value: {value}.")

		if value < 0:
			raise ValueError(f"{instance}: trying to set the {self.name} to a negative value: {value}.")
		instance.__dict__[self.name] = value

	def __delete__(self, instance: A_DEPENDENCIES.CLASS) -> None:
		del instance.__dict__[self.name]



class RangedNumber:
	"""A descriptor protocol used for floating point values in a range

	Raises:
		TypeError: raises an error if the assigned value is not a number
		ValueError: raises an error if the assigned value is outside of the bounds

	Returns:
		_type_: int: an unsigned integer
	"""
	# instance: The instance of the class where the descriptor is used.
	# owner: The class where the descriptor is used.
	# value: The value being assigned to the attribute.

	def __init__(self, name: str = None, minimum: Number = -float("inf"), maximum: Number = float("inf")) -> None:
		# name: The name of the attribute being managed by the descriptor.
		self.name		= name
		self.minimum	= minimum
		self.maximum	= maximum

	def __get__(self, instance: A_DEPENDENCIES.CLASS, owner: typing.Type[A_DEPENDENCIES.CLASS]) -> Number:
		return instance.__dict__[self.name]

	def __set__(self, instance: A_DEPENDENCIES.CLASS, value: Number) -> None:
		if not isinstance(value, Number):
			raise TypeError(f"{instance}: trying to set the {self.name} to a non-numeric value: <{value}: {type(value)}>.")

		if value < self.minimum or value > self.maximum:
			raise ValueError(f"{instance}: trying to set the {self.name} to a value ({value}) outside the bound <{self.minimum}, {self.maximum}>.")
		instance.__dict__[self.name] = value

	def __delete__(self, instance: A_DEPENDENCIES.CLASS) -> None:
		del instance.__dict__[self.name]



class CheckIntMixin:
	"""A descriptor protocol used for limiting the values to integer

	Raises:
		TypeError: raises an error if the assigned value is not a integer

	Returns:
		_type_: int: an integer
	"""

	def __set__(self, instance: A_DEPENDENCIES.CLASS, value:A_DEPENDENCIES.VALUE) -> None:
		if not isinstance(value, int):
			raise TypeError(f"{self.name} must be a int, you have inpuuted {type(value)}={value}.")
		super().__set__(instance, value)

class CheckFloatMixin:
	"""A descriptor protocol used for limiting the values to floats

	Raises:
		TypeError: raises an error if the assigned value is not a float

	Returns:
		_type_: float: a float
	"""

	def __set__(self, instance: A_DEPENDENCIES.CLASS, value:A_DEPENDENCIES.VALUE) -> None:
		if not isinstance(value, float):
			raise TypeError(f"{self.name} must be a float, you have inpuuted {type(value)}={value}.")
		super().__set__(instance, value)




class WriteOnceMixin:
	"""A descriptor protocol used for set-up once values

	Raises:
		AttributeError: raises an error if trying to change the value post-initial assignment

	Returns:
		_type_: int: an unsigned integer
	"""
	def __set__(self, instance:A_DEPENDENCIES.CLASS, value:A_DEPENDENCIES.VALUE) -> None:
		if self.name in instance.__dict__:
			raise AttributeError(f"The attribute '{self.name}' is read-only after initial assignment.")
		super().__set__(instance, value)





class WriteOnce_UnsignedInteger(WriteOnceMixin, CheckIntMixin, UnsignedInteger): pass

class WriteOnce_RangedInt(WriteOnceMixin, CheckIntMixin, RangedNumber): pass

class WriteOnce_RangedFloat(WriteOnceMixin, CheckFloatMixin, RangedNumber): pass

class WriteOnce_CreatePath(WriteOnceMixin, CreatePathDescriptor): pass

class WriteOnce_String(WriteOnceMixin, StringDescr): pass