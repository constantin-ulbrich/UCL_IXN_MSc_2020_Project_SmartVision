# Module Description: This module accesses the Cognitive Service Computer Vision and analyses the target frame stored in the blob storage for objects on the workstation.
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from array import array
import os
import io
from PIL import Image
import sys
import time

# To run the script locally from VSCode, uncomment the import statement(s) below:
#import directory_manipulation as dm 
#import handling_blob_storage as hbl
#import config

""" 
    The Flask application has problems with relative imports across the different project files. 
    Therefore, this solution was developed to use absolute import paths within the project.
    Some help was obtained by the client to discover the issue, as the client had some experience with these kind of issues:
"""
# As there are problems with the relative import of this module, the following workaround was developed:
currentDir = os.getcwd() # get the current working directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..",".."))) # move up two folders, due to issue with relative import
#print("CWD:" + os.getcwd()) # prints current working directory to confirm folder move
import COMP0073_SmartVision_Prototype.SmartVision_Database.database_connection as dbc # import library
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.directory_manipulation as dm # import library
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.handling_blob_storage as hbl # import library
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.config as config# import library
os.chdir(currentDir) # return to initial working directory to prevent issue reading files
#print("CWD:" + os.getcwd()) # to check whether the default working environment is restored



#Computer Vision Azure Authentication Keys
CV_endpoint = config.ACV_endpoint
CV_subscription_key = config.ACV_subscription_key



def detectObjects(containerName, blobName):
    """
        Description: This function detects objects, using Microsofts Azure Computer Vision Algorithm, in an image retrieved from an Azure Blob Storage, via its URL.
        Source: The code has been written with the help of the Azure Computer Vision Documentation (https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-vision-computervision/azure.cognitiveservices.vision.computervision.operations.computervisionclientoperationsmixin?view=azure-python#detect-objects-in-stream-image--custom-headers-none--raw-false--callback-none----operation-config-)
        Input: (containerName -> string), (blobName -> string)
        Output: List -> [[object.object_property, object.confidence, object.rectangle.x, object.rectangle.w, object.rectangle.y, object.rectangle.h], ...]
    """
    print("\n\n===== Detect Objects=====\n")

    #Retriving the probability threshold to recognise an object
    result_probThreshold = dbc.retrieve_probThreshold("computerVisionObjects")
    probThreshold = float(result_probThreshold[0])

    # Client Authentication
    computervision_client = ComputerVisionClient(CV_endpoint, CognitiveServicesCredentials(CV_subscription_key))

    # Get URL image with different objects
    remote_image_url_objects = hbl.getBlobURI(containerName, blobName)

    # Call API with URL
    detect_objects_results_remote = computervision_client.detect_objects(remote_image_url_objects)

    # Detect objects in an image and store results in nested resultList of form: [[object.object_property, object.confidence], [object.object_property, object.confidence], ...]
    resultList = []
    
    print("Detecting objects in remote image:")
    if len(detect_objects_results_remote.objects) == 0:
        print("No objects detected.")
    else:
        for object in detect_objects_results_remote.objects:
            if(object.confidence > probThreshold):
                objectList = [object.object_property, object.confidence, object.rectangle.x, object.rectangle.w, object.rectangle.y, object.rectangle.h]
                resultList.append(objectList)

    return resultList



if(__name__ == '__main__'):
    print("===== Object Detection =====\n\n")
    print(detectObjects("tests", "homeWorkstation.jpg"))