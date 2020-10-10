import numpy as np
from PIL import Image

""" 
    The Flask application has problems with relative imports across the different project files. 
    Therefore, this solution was developed to use absolute import paths within the project.
    Some help was obtained by the client to discover the issue, as the client had some experience with these kind of issues:
"""
currentDir = os.getcwd() # get the current working directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..",".."))) # move up two folders, due to issue with relative import
#print("CWD:" + os.getcwd()) # prints current working directory to confirm folder move
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.directory_manipulation as dm # import library
os.chdir(currentDir) # return to initial working directory to prevent issue reading files
#print("CWD:" + os.getcwd()) # to check whether the default working environment is restored



if(__name__=="__main__"):
    # This code has been adapted from: https://stackoverflow.com/questions/10763298/how-can-i-read-a-binary-file-and-turn-the-data-into-an-image
    # Define width and height
    w, h = 1280, 720

    # Read file using numpy "fromfile()"
    with open(dm.createTargetDirectory("Images")+'transformedDepthImage.bin', mode='rb') as f:
        print(f)
        d = np.fromfile(f,dtype=np.uint8,count=w*h).reshape(h,w)
        print(d)

    # Make into PIL Image and save
    PILimage = Image.fromarray(d)
    PILimage.save(dm.createTargetDirectory("Images")+'test_depth.png')