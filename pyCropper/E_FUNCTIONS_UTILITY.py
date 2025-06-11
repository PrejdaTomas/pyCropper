from .A_DEPENDENCIES import typing, os, Path, allowedFileTypes
from .C_CLASSES import IndexedCycle
from .D_CONSTANTS import userConstants

getFileNameWoSuffix:	typing.Callable[[str], str]			= lambda file: os.path.splitext(os.path.basename(file))[0]
getFileSuffix:			typing.Callable[[str], str]			= lambda file: os.path.splitext(file)[1]

getPicsInDirectory:				typing.Callable[[Path], typing.Sequence[Path]]		= lambda workDir=userConstants.FROM_FOLDER: [Path(os.path.join(workDir, file)) for file in os.listdir(workDir) if getFileSuffix(file).lower() in allowedFileTypes]
getCycledPicsInDirectory:		typing.Callable[[Path], IndexedCycle[Path]]			= lambda workDir=userConstants.FROM_FOLDER:  IndexedCycle(getPicsInDirectory(workDir))
ords:							typing.Callable[[str], typing.Tuple[int,int]]		= lambda ipt: (ord(ipt.lower()), ord(ipt.upper()))