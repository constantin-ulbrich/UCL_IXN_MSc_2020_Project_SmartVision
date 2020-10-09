# Module Description: The module is responsilbe for capturing an image with an RGB visual sensor.
import sys 
import os
import cv2

# To run the script locally from VSCode, uncomment the import statement(s) below:
#import config

""" 
    The Flask application has problems with relative imports across the different project files. 
    Therefore, this solution was developed to use absolute import paths within the project.
    Some help was obtained by the client to discover the issue, as the client had some experience with these kind of issues:
"""
currentDir = os.getcwd() # get the current working directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..",".."))) # move up two folders, due to issue with relative import
#print("CWD:" + os.getcwd()) # prints current working directory to confirm folder move
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.directory_manipulation as dm # import library
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.config as config# import library
os.chdir(currentDir) # return to initial working directory to prevent issue reading files
#print("CWD:" + os.getcwd()) # to check whether the default working environment is restored



def takePicWebCam(imageName, imageType):
    """
        Description: This function takes a .jpg image with the local machine's webcam or the Azure Kinect DK, depending on the configuration.
        Input: (imageName -> string), (imageType -> string)
        Output: No direct output, but it writes the image files into the folder "Images" in the directory COMP0073_SmartVision_Prototype.
    """
    currentDir = os.getcwd() # get the current working directory
    print("Current Working Directory:", currentDir)
    # Create a Video Capture Object from the WebCam
    camera = cv2.VideoCapture(config.webcam)
    # Read in a frame using the WebCam
    check, frame = camera.read()

    # Check whether a frame could be captured
    if not check:
        print("Failed to capture an image.")
    else:
        # Try writing image to the local image file.
        try:
            cv2.imwrite(dm.createTargetDirectory("Images")+imageName, frame)
            print("picture was taken successfully!")
        except Exception as e:
            print("Something went wrong when taking the picture. See the following error:\n", e)
            camera.release()

    # Close the WebCam
    camera.release()



if(__name__ == "__main__"):
    takePicWebCam("tester", ".jpg")