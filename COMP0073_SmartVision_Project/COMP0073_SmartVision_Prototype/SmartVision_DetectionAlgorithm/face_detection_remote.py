# Module Description: This module accesses the Cognitive Service Face and analyses the target frame for faces and emotions in the blob storage.
# Note, the code was written with the support of the Azure Cognitive Face Service Documentation (https://docs.microsoft.com/en-us/rest/api/cognitiveservices/face/face/detectwithurl)

#import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
#from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType

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




#Computer Vision Azure Authentication Keys
FD_endpoint = config.AFD_endpoint
FD_subscription_key = config.AFD_subscription_key



def detectFacesPrintResults(containerName, blobName):
    """
        Description: This function detects facial characteristics, age, and emotions, using the face detection algorithm by Microsoft Azure, in an image retrieved from an Azure Blob Storage, via its URL. It then prints out the results to the console. 
        Input: (containerName -> string), (blobName -> string)
        Output: No direct output, but it writes the results of the object detection to the console.
    """
    print("===== Face Detection =====")
    # Create an authenticated FaceClient.
    face_client = FaceClient(FD_endpoint, CognitiveServicesCredentials(FD_subscription_key))

    # Get URL image with different objects
    remote_image_url = hbl.getBlobURI(containerName, blobName)

    # Call API with URL
    detected_faces = face_client.face.detect_with_url(url=remote_image_url, return_face_id=True, return_face_attributes=["gender", "age", "facialHair", "glasses", "emotion", "accessories", "occlusion", "makeup", "hair", "smile"])

    # Retrieving and Formatting Data about recognised faces in supplied image
    if not detected_faces:
        print('No face detected from image Blob {}'.format(blobName))
    else:
        # Display the detected face ID in the first single-face image.
        # Face IDs are used for comparison to faces (their IDs) detected in other images.
        for face in detected_faces:
            print('Detected Face from image:', blobName) 

            #Generating Face ID for detected image
            print ("Face ID:", face.face_id)

            #Detecting Gender
            print("Gender:", face.face_attributes.gender.name)

            #Detecting Age
            print("Age:", face.face_attributes.age)

            #Detecting Emotion
            # Retrieving probability threshold for analysed item emotions
            result_EmotionprobThreshold = dbc.retrieve_probThreshold("emotions")
            emotionThreshold = float(result_EmotionprobThreshold[0])


            emotions = {}
            if(face.face_attributes.emotion.anger > emotionThreshold):
                emotions["anger"] = face.face_attributes.emotion.anger
            
            if(face.face_attributes.emotion.contempt > emotionThreshold):
                emotions["contempt"] = face.face_attributes.emotion.contempt
            
            if(face.face_attributes.emotion.disgust > emotionThreshold):
                emotions["disgust"] = face.face_attributes.emotion.disgust

            if(face.face_attributes.emotion.fear > emotionThreshold):
                emotions["fear"] = face.face_attributes.emotion.fear

            if(face.face_attributes.emotion.happiness > emotionThreshold):
                emotions["happiness"] = face.face_attributes.emotion.happiness

            if(face.face_attributes.emotion.neutral > emotionThreshold):
                emotions["neutral"] = face.face_attributes.emotion.neutral

            if(face.face_attributes.emotion.sadness > emotionThreshold):
                emotions["sadness"] = face.face_attributes.emotion.sadness

            if(face.face_attributes.emotion.surprise > emotionThreshold):
                emotions["surprise"] = face.face_attributes.emotion.surprise
            
            print("Emotions:",)
            if(len(emotions.keys()) >0):
                for emotionsKey in emotions:
                    print(emotionsKey + " with Confidence of", str(emotions[emotionsKey]) + "; ",)
                print()
            else:
                print("None;")


            #Detecting a Smile
            # Retrieving probability threshold for analysed item smile
            result_SmileprobThreshold = dbc.retrieve_probThreshold("smile")
            smileThreshold = float(result_EmotionprobThreshold[0])

            if(face.face_attributes.smile > smileThreshold):
                print("Smile: Yes, with confidence of", str(face.face_attributes.smile) + ";")
            else:
                print("Smile: None;")
  

            #Detecting Accessories
            # Retrieving probability threshold for analysed item accessories
            result_accessoriesProbThreshold = dbc.retrieve_probThreshold("accessories")
            accessoriesThreshold = float(result_accessoriesProbThreshold[0])

            print("Accessories:",)
            if (len(face.face_attributes.accessories) > 0):
                for accessoriesItem in face.face_attributes.accessories:
                    if(accessoriesItem.confidence > accessoriesThreshold):
                        print(accessoriesItem.type.name + " with Confidence of", str(accessoriesItem.confidence) + ";") 
            else: 
                print("None;")


            #Detecting Makup
            print("Eye makeup:", face.face_attributes.makeup.eye_makeup)
            print("lip makeup:", face.face_attributes.makeup.lip_makeup)

            
            #Detecting Facial Hair
            # Retrieving probability threshold for analysed item facial hair
            result_fHairProbThreshold = dbc.retrieve_probThreshold("facialHair")
            fHairThreshold = float(result_fHairProbThreshold[0])

            facialHair = {}
            if(face.face_attributes.facial_hair.beard > fHairThreshold):
                facialHair["beard"] = face.face_attributes.facial_hair.beard
            
            if(face.face_attributes.facial_hair.moustache > fHairThreshold):
                facialHair["moustache"] = face.face_attributes.facial_hair.moustache

            if(face.face_attributes.facial_hair.sideburns > fHairThreshold):
                facialHair["sideburns"] = face.face_attributes.facial_hair.sideburns
            
            print("Facial Hair:",)
            if(len(facialHair.keys()) >0):
                for facialHairKey in facialHair:
                    print(facialHairKey + " with Confidence of", str(facialHair[facialHairKey]) + ";")
            else:
                print("None;")


            #Detecting Hair
            # Retrieving probability threshold for analysed item facial hair
            result_hairProbThreshold = dbc.retrieve_probThreshold("hair")
            hairThreshold = float(result_hairProbThreshold[0])

            if(face.face_attributes.hair.invisible == False):
                if(face.face_attributes.hair.bald > hairThreshold):
                    print("Hair: bald")
                else:
                    print("Hair: ",)
                    for hairColor in face.face_attributes.hair.hair_color:
                        if(hairColor.confidence > hairThreshold):
                            print(hairColor.color.name, "with a Confidence of", str(hairColor.confidence) + "; ",)

                    print()
            else:
                print("Hair: not visible;")


            #Detecting Glasses
            print("Glasses:", face.face_attributes.glasses.name)


            #Detecting Occlusion
            occlusion = []
            if(face.face_attributes.occlusion.eye_occluded):
                occlusion.append("Eye Occluded")
            
            if(face.face_attributes.occlusion.forehead_occluded):
                occlusion.append("Forehead Occluded")
            
            if(face.face_attributes.occlusion.mouth_occluded):
                occlusion.append("Mouth Occluded")
            
            if(len(occlusion) > 0):
                print("Occlusion:", occlusion)
            else:
                print("Occlusion: None;")
    
            print()




def detectFaces(containerName, blobName):
    """
        Description: This function detects facial characteristics, age, and emotions, using the face detection algorithm by Microsoft Azure, in an image retrieved from an Azure Blob Storage, via its URL. 
        Input: (containerName -> string), (blobName -> string)
        Output: resultList = [{'faceID': string, 'gender': string, 'age': float, 'emotions': {'some emotion': confidence value as float}, 'smile': float, 'accessories': list, 'eye_makeup': boolean, 'lip_makeup': boolean, 'facial_hair': list, 'hair': string, 'glasses': string, 'eye_occluded': boolean, 'forehead_occluded': boolean, 'mouth_occluded': boolean }]
    """
    # Create an authenticated FaceClient.
    face_client = FaceClient(FD_endpoint, CognitiveServicesCredentials(FD_subscription_key))

    # Get URL image with different objects
    remote_image_url = hbl.getBlobURI(containerName, blobName)

    # Call API with URL
    detected_faces = face_client.face.detect_with_url(url=remote_image_url, return_face_id=True, return_face_attributes=["gender", "age", "facialHair", "glasses", "emotion", "accessories", "occlusion", "makeup", "hair", "smile"])

    # Initiating the result List containing a dictionary for each identified face
    resultList = []

    # Retrieving and Formatting Data about recognised faces in supplied image
    if not detected_faces:
        pass
    else:
        for face in detected_faces:
            #Creating a dictionary with each face attribute as a key
            faceDict = {}

            #Generating Face ID for detected image
            faceDict["faceID"] = face.face_id

            #Detecting Gender
            faceDict["gender"] = face.face_attributes.gender.name

            #Detecting Age
            faceDict["age"] = face.face_attributes.age

            #Detecting Emotion
            # Retrieving probability threshold for analysed item facial hair
            result_emotionsProbThreshold = dbc.retrieve_probThreshold("emotions")
            emotionsThreshold = float(result_emotionsProbThreshold[0])

            #Creating a dictionary containing all emotions with a confidence value greater than 0.5
            emotions = {}
            if(face.face_attributes.emotion.anger > emotionsThreshold):
                emotions["anger"] = face.face_attributes.emotion.anger
            
            if(face.face_attributes.emotion.contempt > emotionsThreshold):
                emotions["contempt"] = face.face_attributes.emotion.contempt
            
            if(face.face_attributes.emotion.disgust > emotionsThreshold):
                emotions["disgust"] = face.face_attributes.emotion.disgust

            if(face.face_attributes.emotion.fear > emotionsThreshold):
                emotions["fear"] = face.face_attributes.emotion.fear

            if(face.face_attributes.emotion.happiness > emotionsThreshold):
                emotions["happiness"] = face.face_attributes.emotion.happiness

            if(face.face_attributes.emotion.neutral > emotionsThreshold):
                emotions["neutral"] = face.face_attributes.emotion.neutral

            if(face.face_attributes.emotion.sadness > emotionsThreshold):
                emotions["sadness"] = face.face_attributes.emotion.sadness

            if(face.face_attributes.emotion.surprise > emotionsThreshold):
                emotions["surprise"] = face.face_attributes.emotion.surprise

            # Adding the emotions dictionary to the faceDict dictionary
            faceDict["emotions"] = emotions
            

            #Detecting a Smile
            faceDict["smile"] = face.face_attributes.smile


            #Detecting Accessories
             # Retrieving probability threshold for analysed item accessories
            result_accessoriesProbThreshold = dbc.retrieve_probThreshold("accessories")
            accessoriesThreshold = float(result_accessoriesProbThreshold[0])

            accessories = []
            if (len(face.face_attributes.accessories) > 0):
                for accessoriesItem in face.face_attributes.accessories:
                    if(accessoriesItem.confidence > accessoriesThreshold):
                        accessories.append(accessoriesItem.type.name)
            else: 
                pass

            faceDict["accessories"] = accessories


            #Detecting Makup
            faceDict["eye_makeup"] = face.face_attributes.makeup.eye_makeup
            faceDict["lip_makeup"] = face.face_attributes.makeup.lip_makeup

            
            #Detecting Facial Hair
            # Retrieving probability threshold for analysed item facial hair
            result_fHairProbThreshold = dbc.retrieve_probThreshold("facialHair")
            fHairThreshold = float(result_fHairProbThreshold[0])

            facialHair = []
            if(face.face_attributes.facial_hair.beard > fHairThreshold):
                facialHair.append("beard")
            
            if(face.face_attributes.facial_hair.moustache > fHairThreshold):
                facialHair.append("moustache")

            if(face.face_attributes.facial_hair.sideburns > fHairThreshold):
                facialHair.append("sideburns")
            
            faceDict["facial_hair"] = facialHair


            #Detecting Hair
            # Retrieving probability threshold for analysed item facial hair
            result_hairProbThreshold = dbc.retrieve_probThreshold("hair")
            hairThreshold = float(result_hairProbThreshold[0])

            if(face.face_attributes.hair.invisible == False):
                if(face.face_attributes.hair.bald > hairThreshold):
                    faceDict['hair'] = "bald"
                else:
                    color = ""
                    confidence = hairThreshold
                    for hairColor in face.face_attributes.hair.hair_color:
                        if(hairColor.confidence > confidence):
                            confidence = hairColor.confidence
                            color = hairColor.color.name
                    faceDict['hair'] = color
            else:
                faceDict['hair'] = "invisible"


            #Detecting Glasses
            faceDict['glasses'] = face.face_attributes.glasses.name


            #Detecting Occlusion
            faceDict['eye_occluded'] = face.face_attributes.occlusion.eye_occluded
            
            faceDict['forehead_occluded'] = face.face_attributes.occlusion.forehead_occluded
            
            faceDict['mouth_occluded'] = face.face_attributes.occlusion.mouth_occluded
            

            # Append faceDict dictionary with all attributes for an identified face to the result list
            resultList.append(faceDict)


    # Return the result list
    return resultList




if(__name__ == "__main__"):
    print("===== Face Detection =====")
    print(detectFaces("tests", "happyKids.jpg"))
    #detectFacesPrintResults("tests", "happyKids.jpg")

