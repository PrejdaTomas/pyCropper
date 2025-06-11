import os
import pyCropper

if __name__ == "__main__":
	outputImgtype = pyCropper.ImageType[pyCropper.userConstants.IMAGE_TYPE]

	pyCropper.processImages(workDir= pyCropper.userConstants.FROM_FOLDER, outputImageType= outputImgtype)
