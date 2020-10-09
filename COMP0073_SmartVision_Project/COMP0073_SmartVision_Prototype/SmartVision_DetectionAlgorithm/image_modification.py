# Module Description: This module receives the latest taken frame from the analysis and modifies the image
# by marking the detected objects with bounding boxes and tags. This is used for the statistics page of the interface.
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import sys

# To run the script locally from VSCode, uncomment the import statement(s) below:
#import directory_manipulation as dm 
#import handling_blob_storage as hbl
#import custom_vision_detection_remote as cvdr
#import object_detection_remote as odr

""" 
    The Flask application has problems with relative imports across the different project files. 
    Therefore, this solution was developed to use absolute import paths within the project.
    Some help was obtained by the client to discover the issue, as the client had some experience with these kind of issues:
"""
currentDir = os.getcwd() # get the current working directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..",".."))) # move up two folders, due to issue with relative import
#print("CWD:" + os.getcwd()) # prints current working directory to confirm folder move
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.custom_vision_detection_remote as cvdr # import library
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.object_detection_remote as odr # import library
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.directory_manipulation as dm # import library
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.handling_blob_storage as hbl # import library
os.chdir(currentDir) # return to initial working directory to prevent issue reading files
#print("CWD:" + os.getcwd()) # to check whether the default working environment is restored




def drawBoxes(object_name, x, y, w, h, drawing):
    """
        Description: The function draws a red rectangle around a detected object in an image and writes above the red bounding box the identified object type.
        Source: This function was adopted to a great extend from the following source https://github.com/Azure-Samples/cognitive-services-quickstart-code/blob/master/python/ComputerVision/DetectObjectsTags.py
        Input: (object_name -> string), (x -> float), (y -> float), (w -> float), (h -> float), (drawing -> PIL.ImageDraw object)
        Output: Simply adjusts the state of an existing PIL.ImageDraw object
    """
    left = x
    top = y
    right = left + w
    bottom = top + h
    fontsize = 75 #A fontsize of 30 is best if the webcam is used
    box_width = 7 # A width of 3 is best if the webcam is used

    coordinates_rectangle = ((left, top), (right, bottom))
    coordinates_text = (left,top - fontsize -9)

    # get a font
    fnt = ImageFont.truetype("arial.ttf", fontsize)

    drawing.rectangle(coordinates_rectangle, outline=(255,88,0), width=box_width) 
    drawing.text(coordinates_text, object_name, font=fnt, fill=(255,88,0,255))



def modifyAnalysedImage(container, frame):
    """
        Description: The function downloads an Image from an Azure Blob Storage. Then, it obtains the identified objects in the image and draws red bounding boxes around them. 
        Afterwards it saves the image in the "Images" folder and uploads them to the analysedframes container in the blob storage.
        Source: Some ideas have been adapted from the source https://github.com/Azure-Samples/cognitive-services-quickstart-code/blob/master/python/ComputerVision/DetectObjectsTags.py 
        Input: (detection_results -> list), (customVision_results -> list), (container -> string), (frame -> string)
        Output: No direct output, but saves the modified image in the folder "images" and uploads it to the container "analysedframes".
    """
    detection_results = odr.detectObjects(container, frame)
    customVision_results= cvdr.customVisionDetectObjects(container, frame)
    print(customVision_results)
    image_stream = hbl.downloadBlob(container, frame)
    image_r = Image.open(BytesIO(image_stream))
    image_draw = ImageDraw.Draw(image_r)
    image_height = image_r.height
    image_width = image_r.width

    # Drawing the rectandlges
    for detected in detection_results:
        drawBoxes(detected[0], detected[2], detected[4], detected[3], detected[5], image_draw)
    
    for customDetected in customVision_results:
        x = round(customDetected[2]*image_width, 0)
        y = round(customDetected[3]*image_height, 0)
        w = round(customDetected[4]*image_width, 0)
        h = round(customDetected[5]*image_height, 0)
        drawBoxes(customDetected[0], x, y, w, h, image_draw)

    image_r.save(dm.createTargetDirectory("Images") + "analysed_workstation.jpg")
    hbl.uploadBlob("analysedframes", "analysed_workstation.jpg", "analysed_workstation.jpg", ".jpg")
    #image_r.show() # for testing purposes
    image_r.close()


def test_imageType(image_stream):
    """
        Description: This function tests, whether the imageType retrieved from the stream is of type '<class 'bytes'>'
    """
    print("The type of the downloaded blob image:", type(image_stream))
    if(str(type(image_stream)) == "<class 'bytes'>"):
        print("The class type equates to <class 'bytes'>: True")
    else:
        print("The class type is of type:", type(image_stream), "--> False")



if(__name__ == '__main__'):
    print("===== Object Detection =====\n\n")

    modifyAnalysedImage("lasttakenframe", "tester.jpg")
    #image_stream = hbl.downloadBlob("lasttakenframe", "tester.jpg")
    #test_imageType(image_stream)
