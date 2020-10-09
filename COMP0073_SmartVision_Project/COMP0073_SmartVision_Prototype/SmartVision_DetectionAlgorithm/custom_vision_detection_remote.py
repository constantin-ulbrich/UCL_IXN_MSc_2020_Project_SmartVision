# Module Description: This module accesses the custom detection model of the SmartVision System and analyses the target frame stored in the blob storage.
# Note, the code was written with the support of the Azure Cognitive Custom Vision Documentation (https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-vision-customvision/azure.cognitiveservices.vision.customvision.prediction?view=azure-python)

from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClientConfiguration
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from msrest.authentication import CognitiveServicesCredentials
from msrest.authentication import ApiKeyCredentials
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
currentDir = os.getcwd() # get the current working directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..",".."))) # move up two folders, due to issue with relative import
#print("CWD:" + os.getcwd()) # prints current working directory to confirm folder move
import COMP0073_SmartVision_Prototype.SmartVision_Database.database_connection as dbc # import library
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.directory_manipulation as dm # import library
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.handling_blob_storage as hbl # import library
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.config as config # import library
os.chdir(currentDir) # return to initial working directory to prevent issue reading files
#print("CWD:" + os.getcwd()) # to check whether the default working environment is restored



#Custom Vision Azure Authentication Keys
CCV_endpoint = config.ACCV_endpoint
CCV_subscription_key = config.ACCV_subscription_key
CCV_prediction_key = config.ACCV_prediction_key
CCV_credentials = ApiKeyCredentials(in_headers={"Prediction-Key": CCV_prediction_key})
#Custom Vision Azure Project Credentials
project_id = config.ACCV_project_id
published_name = config.ACCV_published_name


def customVisionDetectObjectsDisplay(containerName, blobName):
    """
        Description: This function detects selected workstation objects, using a custom vision algorithm, in an image retrieved from an Azure Blob Storage, via its URL. It then prints out the results to the console.
        Source: The Azure Custom Vision SDK Sample was used as guidance and for finding an elegant way to print the results to the console (https://github.com/Azure-Samples/cognitive-services-python-sdk-samples/blob/master/samples/vision/custom_vision_prediction_samples.py) 
        Input: (containerName -> string), (blobName -> string)
        Output: No direct output, but it writes the results of the object detection to the console.
    """
    print("\n\n===== Custom Vision Object Detection=====\n")
    #Retriving the probability threshold to recognise an object
    result_probThreshold = dbc.retrieve_probThreshold("customVisionObjects")
    probThreshold = float(result_probThreshold[0])

    # Client Authentication
    predictor = CustomVisionPredictionClient(CCV_endpoint, CCV_credentials)

    # Get URL image with different objects
    remote_image_url_objects = hbl.getBlobURI(containerName, blobName)

    # Call API with URL
    custom_vision_prediction = predictor.detect_image_with_no_store(project_id, published_name, remote_image_url_objects)
    
    print("Objects Detected with Custom Vision and a Probability Threshold >= 0.2:")
    if len(custom_vision_prediction.predictions) == 0:
        print("No objects detected.")
    else:
         for prediction in custom_vision_prediction.predictions:
             print("Objects Detected with Custom Vision and a Probability Threshold >= 0.2:")
             if (prediction.probability >= probThreshold):
                print("->\t" + prediction.tag_name +
                ": {0:.2f}%".format(prediction.probability * 100))



def customVisionDetectObjectsLocalDisplay(imageFileName):
    """
        Description: This function detects selected workstation objects, using a custom vision algorithm, in an image retrieved from an Azure Blob Storage, via its URL. It then prints out the results to the console. 
        Source: The Azure Custom Vision SDK Sample was used as guidance and for finding an elegant way to print the results to the console (https://github.com/Azure-Samples/cognitive-services-python-sdk-samples/blob/master/samples/vision/custom_vision_prediction_samples.py)
        Input: (containerName -> string), (blobName -> string)
        Output: No direct output, but it writes the results of the object detection to the console.
    """
    print("\n\n===== Custom Vision Object Detection=====\n")
    #Retriving the probability threshold to recognise an object
    result_probThreshold = dbc.retrieve_probThreshold("customVisionObjects")
    probThreshold = float(result_probThreshold[0])

    # Client Authentication
    predictor = CustomVisionPredictionClient(CCV_endpoint, CCV_credentials)

    # Get URL image with different objects
    #remote_image_url_objects = hbl.getBlobURI(containerName, blobName)
    with open(dm.createTargetDirectory("Images") + imageFileName, "rb") as image_contents:
        # Call API with URL
        custom_vision_prediction = predictor.detect_image_with_no_store(project_id, published_name, image_contents.read())
    
    print("Objects Detected with Custom Vision and a Probability Threshold >= 0.2:")
    if len(custom_vision_prediction.predictions) == 0:
        print("No objects detected.")
    else:
         for prediction in custom_vision_prediction.predictions:
             if (prediction.probability >= probThreshold):
                print("->\t" + prediction.tag_name +
                ": {0:.2f}%".format(prediction.probability * 100))



def customVisionDetectObjects(containerName, blobName):
    """
        Description: This function detects selected workstation objects, using a custom vision algorithm, in an image retrieved from an Azure Blob Storage, via its URL. 
        Input: (containerName -> string), (blobName -> string)
        Output: List -> [[prediction.tag_name, prediction.probability, prediction.bounding_box.left, prediction.bounding_box.top, prediction.bounding_box.width, prediction.bounding_box.height], ...]
    """
    print("\n\n===== Custom Vision Object Detection=====\n")
    #Retriving the probability threshold to recognise an object
    result_probThreshold = dbc.retrieve_probThreshold("customVisionObjects")
    probThreshold = float(result_probThreshold[0])

    # Client Authentication
    predictor = CustomVisionPredictionClient(CCV_endpoint, CCV_credentials)

    # Get URL image with different objects
    remote_image_url_objects = hbl.getBlobURI(containerName, blobName)

    # Call API with URL
    custom_vision_prediction = predictor.detect_image_url_with_no_store(project_id, published_name, remote_image_url_objects)

    # Detect objects in an image and store results in nested resultList of form: [[prediction.tag_name, prediction.probability], [prediction.tag_name, prediction.probability], ...]
    resultList = []
    
    #print("Detecting objects in remote image:")
    if len(custom_vision_prediction.predictions) == 0:
        pass
    else:
         for prediction in custom_vision_prediction.predictions:
             if (prediction.probability >= probThreshold):
                resultList.append([prediction.tag_name, prediction.probability, prediction.bounding_box.left, prediction.bounding_box.top, prediction.bounding_box.width, prediction.bounding_box.height])
    return resultList




if(__name__ == '__main__'):
    print("===== Object Detection =====\n\n")
    #customVisionDetectObjectsLocalDisplay("officeWork.jpg")
    print(customVisionDetectObjects("tests", "homeWorkstation.jpg"))

