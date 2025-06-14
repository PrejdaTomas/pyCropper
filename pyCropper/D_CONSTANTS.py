from . import C_CLASSES
from .A_DEPENDENCIES import argparse,os

_parser = argparse.ArgumentParser(
	prog="pyCropper",
	usage="Image Manipulation",
	description="Crop images quickly by clicking in sequence and using shortcuts"
)

_parser.add_argument("-i", "--fromFolder", default=os.path.dirname(os.path.dirname(__file__)), help="Input folder. String. Defaults to the directory containing main.py.")
_parser.add_argument("-o", "--toFolder", default="CROPPED", help="Name of the folder created in the workdir, where the images will be stored. String. Defaults to 'CROPPED'.")
_parser.add_argument("-m", "--minSize", default="0", help="Minimum pixels on the resulting image diagonal. Defaults to 0. Integer. Range = <0, inf)")
_parser.add_argument("-x", "--width", help="Width part of the aspect ratio. Integer")
_parser.add_argument("-y", "--height",help="Height part of the aspect ratio. Integer")
_parser.add_argument("-s", "--displayScale", default="0.25", help="Zoom of the displayed image. Float. Defaults to 0.25. Range = <0.05, inf)")
_parser.add_argument("-t", "--imageType", default="JPG", help="Type of the image. String. Defaults to JPG. Range= \{JPG, PNG\}")
_parser.add_argument("-j", "--qualityJPG", default="95", help="Quality of the resulting JPG. Integer. Defaults to 95. Range = <10, 100>")
_parser.add_argument("-p", "--qualityPNG", default="5", help="Compression of the resulting PNG. Integer. Defaults to 5. Range = <1, 10>")

_args = _parser.parse_args()
if _args.width is None or len(_args.width.strip()) == 0: raise UserWarning(f"You have not inputted the width scaling factor. Both must be inputted: python main.py -x 4 -y 3")
if _args.height is None or len(_args.width.strip()) == 0: raise UserWarning(f"You have not inputted the height scaling factor. Both must be inputted: python main.py -y 3 -x 4")
print(_args)
userConstants       = C_CLASSES.UserConstants(	fromFolder=(_args.fromFolder).strip(),
												toFolder=os.path.join((_args.fromFolder).strip(), (_args.toFolder).strip()),
												minimumPixels=int(_args.minSize),
												widthScale=int(_args.width),
												imageType=(_args.imageType.strip()).upper(),
												heightScale=int(_args.height),
												displayScale=float(_args.displayScale),
												JPG_quality=int(_args.qualityJPG),
												PNG_quality=int(_args.qualityPNG),

)
controlConstants    = C_CLASSES.ControlConstants()
controlConstants.RELATIVE_TEXT_OFFSET = 0.05