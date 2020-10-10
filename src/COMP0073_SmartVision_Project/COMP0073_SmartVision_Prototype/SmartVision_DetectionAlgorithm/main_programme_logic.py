# Module Description: This module ties together all the different aspects necessary to analyse a workstation and an employee's emotions.
# It assemsbles the different components to the SmartVision algorithm.
import os
import sys
import time
import datetime
from mysql.connector import Error
# Source for the package schedule: https://schedule.readthedocs.io/en/stable/index.html
import schedule

""" 
    The Flask application has problems with relative imports across the different project files. 
    Therefore, this solution was developed to use absolute import paths within the project.
    Some help was obtained by the client to discover the issue, as the client had some experience with these kind of issues:
"""
#print("Current working directory:", os.getcwd())
currentDir = os.getcwd() # get the current working directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))) # move up two folders, due to issue with relative import
#print("CWD:" + os.getcwd()) # prints current working directory to confirm folder move
import COMP0073_SmartVision_Prototype.SmartVision_Database.database_connection as dbc # import library
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.object_detection_remote as odr # import library
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.face_detection_remote as fdr # import library
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.handling_blob_storage as hbs # import library
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.camera_controller as cc # import library
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.custom_vision_detection_remote as ccvr # import library
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.image_modification as im # import library
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.directory_manipulation as dm # import library
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.run_kinectDK as akdk # import library
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.config as config # import library
os.chdir(currentDir) # return to initial working directory to prevent issue reading files
#print("CWD:" + os.getcwd()) # to check whether the default working environment is restored

# To run the script locally from VSCode, uncomment the import statement(s) below:
#import directory_manipulation as dm
#import object_detection_remote as odr
#import face_detection_remote as fdr
#import handling_blob_storage as hbs
#import camera_controller as cc
#import custom_vision_detection_remote as ccvr
#import face_test as ft
#import image_modification as im



# Global Variables:
container_name = "frames"
container_lastTakenFrame = "lasttakenframe"
frame_name = "tester.jpg"
algorithm_running = "" # Initiating the global variable to start and stop the algorithm

# Initiating the global variable: global_counter to track how often the program ran, such that it can be safely terminated after a certain number of iterations.
global_counter = 0


#Functions:

def display_WebCam_analyse():
        """
                Description: The function takes a picture with the webcam of the local machine and analyses the image for objects and emotions. 
                The computer vision and face detection algorithm by Microsoft Azure are used, as well as a Custom Vision Algorithm. Afterwards, the results are printed to the console. 
                Input: Nothing
                Output: No output, analysis results are printed to the console.
        """
        global global_counter
        global container_name
        global frame_name

        # Taking an image
        cc.takePicWebCam(frame_name, ".jpg")

        print("_________________________")

        #Uploading an Image into the container frames in the blob storge
        hbs.uploadBlob(container_name, frame_name, frame_name, ".jpg")

        print("_________________________")

        #Detecing objects in an uploaded picture
        print(odr.detectObjects(container_name, frame_name))
        print()
        ccvr.customVisionDetectObjects(container_name, frame_name)
        print()

        print("_________________________")

        #Analysis of faces in uploaded image
        print(fdr.detectFaces(container_name, frame_name))
        #fdr.detectFacesPrintResults("frames", "testPic")

        print("_________________________")

        #Deleting an Image in the blobstorage:
        hbs.deleteBlob(container_name, frame_name)

        global_counter +=1




def workstationOccupied(containerName, frameName):
        """
                Description: The function utilises the "detectObjects" function to obtain all the detected objects in an image. 
                Then it compares the found objects to all objects in the object_score dictionary. Following the function evaluates 
                a occupation_score based on the found objects (the scores for each relevant object is found in the object_score dictionary, 
                retrieved from the SmartVision database table customvisionobjectscore). 
                Input: (containerName -> string), (frameName -> string)
                Output: dictionary -> {'occupied': boolean, 'occupation_score': integer, 'person_detected': boolean, 'timestamp': string of form "YYYY-MM-DD HH:MM:SS"}
        """
        # Retrieving the object scores from all customVision objects into a dictionary from the database
        object_score = dbc.retrieve_customObjectScore_toDict()
        resultDict = {}
        occupied = False
        personDetected = False
        occupation_threshold = 100
        overallDetectedObjects = []
        occupation_score = 0

        #Detecing objects in an uploaded picture using Object Detection Algorithm
        resultObjectDetection = odr.detectObjects(containerName, frameName)

        for detectedObject in resultObjectDetection:
                overallDetectedObjects.append(detectedObject[0])

        #Detecing objects in an uploaded picture using Custom Vision Algorithm
        resultCustomVisionDetection = ccvr.customVisionDetectObjects(containerName, frameName)

        for detectedCustomObject in resultCustomVisionDetection:
                overallDetectedObjects.append(detectedCustomObject[0])

        # Taking a timestamp, once the image has been analysed
        currentTime = datetime.datetime.now()
        currentTimestamp = currentTime.strftime("%Y-%m-%d %H:%M:%S")

        # Calculating the Occupation Score
        for foundObject in overallDetectedObjects:
                if foundObject in object_score.keys():
                        occupation_score += object_score[foundObject]
                        if(foundObject == "person"):
                                personDetected = True

        # Determine whether workstation is occupied or not
        if(occupation_score >= occupation_threshold):
                occupied = True
        else:
                occupied = False

        resultDict['occupied'] = occupied
        resultDict['occupation_score'] = occupation_score
        resultDict['person_detected'] = personDetected
        resultDict['timestamp'] = currentTimestamp

        return resultDict




def detectedDominatEmotion(containerName, frameName):
        """
                Description: Function retrieves the emotions and smile value of the 
                "detectFaces" function. Those are then packaged into a dictionary for each face.  
                Input: (containerName -> string), (frameName -> string)
                Output: list -> [{'dominant_emotion': string, 'smile': boolean}, {...}]
        """
        faceAnalysisResults = fdr.detectFaces(containerName, frameName)

        # Retrieving probability threshold for analysed item smile
        result_SmileprobThreshold = dbc.retrieve_probThreshold("smile")
        smileThreshold = float(result_SmileprobThreshold[0])
        detectedEmotions = {'dominant_emotion': "no face detected", 'smile': False}
        # Printing out the Face analysis results to the console for testing purposes
        #print("Face Analysis Results:")
        #print(faceAnalysisResults)
        for face in faceAnalysisResults:
                dominantEmotionProbability = 0
                dominantEmotion = ""
                if(face['eye_occluded'] == True or face['mouth_occluded'] == True):
                        detectedEmotions['dominant_emotion'] = "face occluded"
                else:
                        if (len(face['emotions']) > 0):
                                for emotions in face['emotions'].keys():
                                        if (face['emotions'][emotions]>dominantEmotionProbability):
                                                dominantEmotionProbability = face['emotions'][emotions]
                                                dominantEmotion = emotions

                                detectedEmotions['dominant_emotion'] = dominantEmotion
                        else:
                                detectedEmotions['dominant_emotion'] = "undetected"

                if(face['smile'] > smileThreshold):
                        detectedEmotions['smile'] = True
                else:
                        detectedEmotions['smile'] = False

                # break out of the loop after first iteration, as only one face can be processed and no facial tracking is allowed
                break


        return detectedEmotions



def analyseWorkstation():
        """
                Description: This function brings together the functions "workstationOccupied" and "detectDominatEmotion" to analyse an image taken by a camera connected to the local machine.
                The results of the analysis are then uploaded to the SmartVision database table frameanalysis.  
                Input: Nothing
                Output: No direct output, except deleting the analysed image in the blob storage, which it uploaded at the start of the function, and inserting the analysis results into the frameanalysis table.
        """
        global global_counter
        global container_name
        global frame_name
        global container_lastTakenFrame

        # These if statements evaluate whether an image should be captured via the webcam module or by invoking the Azure_Kinect_Controller System.
        # This system programmes the Azure Kinect DK to capture a color image (and depth image), which is then uploaded to the Azure Blob Storage of the SmartVision System. 
        if(config.visual_sensor == "azure_kinect_dk"):
                #Running the Azure Kinect DK Code from the Azure_Kinect_Controller System
                akdk.executeKinectDKinC()
                print("Kinect Executed\n")
        elif(config.visual_sensor == "webcam"):
                # Taking an image with visual sensor as webcam
                cc.takePicWebCam(frame_name, ".jpg")

                #Uploading an Image into the container frames in the blob storge
                hbs.uploadBlob(container_name, frame_name, frame_name, ".jpg")

                #Uploading an Image into the container lasttakenframe in the blob storge used for the imageManipulation function
                hbs.uploadBlob(container_lastTakenFrame, frame_name, frame_name, ".jpg")
        else:
              print()  
              print("!!!!! ERROR OCCURRED !!!!!")
              print("No image was taken by the webcam or the Azure Kinect DK! Check the configuration settings of the SmartVision System.")
              print("To check the settings go to COMP0073_SmartVision_Project -> COMP0073_SmartVision_Prototype -> SmartVision_Detection Algorithm -> config.py.\n")

        print("_________________________")

        #Analyse whether a workstation is occupied or not
        resultWorkstationOccupied = workstationOccupied(container_name, frame_name)
        #print(resultWorkstationOccupied)

        print("_________________________")

        #Analyse emotions of detected faces in the occupied workspace
        if(resultWorkstationOccupied['person_detected']):
                resultDetectedDominantEmotion = detectedDominatEmotion(container_name, frame_name)
        else:
                resultDetectedDominantEmotion = {'dominant_emotion': "no person detected", 'smile': False}

        #Printing the results of the emotion detection to the console for checking
        #print(resultDetectedDominantEmotion)

        #Insert results into the table frameanalysis of the database
        if(dbc.insert_frameanalysis(resultWorkstationOccupied['occupied'], resultWorkstationOccupied['occupation_score'], resultWorkstationOccupied['person_detected'], resultDetectedDominantEmotion['dominant_emotion'], resultDetectedDominantEmotion['smile'], resultWorkstationOccupied['timestamp'])):
                print("Success")
        else:
                print("Failure")
        print("_________________________")

        #Deleting an Image in the blobstorage:
        hbs.deleteBlob(container_name, frame_name)

        global_counter +=1


def set_variable_global_running(command):
        """
                Description: Function serves to control the execution flow from the SmartVision_Flask file server.py to interrupt the analyseWorkstation function.
                Input: (command -> string)
                Output: No output, simply sets the global variable algorithm_running to "start", to initiate the algorithm, or to "", to stop the algorithm.
        """
        global algorithm_running
        algorithm_running = str(command)


def runSmartVisionAlgorithm():
        """
                Description: This function is executed by the SmartVision_Flask file server.py to start the analyseWorkstation function. The latter named function is run every 10 seconds, unitl
                the global variable algorithm_running is set to "".  
                Input: Nothing
                Output: None.
        """
        global algorithm_running

        schedule.every(10).seconds.do(analyseWorkstation).tag('analysis')

        while (algorithm_running == "start"):
                schedule.run_pending()
                time.sleep(1)
                print("Counter:", global_counter)
                print("Global Variable in WhileLoop:", algorithm_running)


        print("Global Variable after WhileLoop:", algorithm_running)
        schedule.clear('analysis')
        algorithm_running = ""
        print("Exiting the Programme.")
        #sys.exit()



# Main Execution Thread:

if(__name__ == '__main__'):
        print("=====Main Logic Programme=====\n\n")
        #print(workstationOccupied("tests", "homeWorkstation.jpg"))

        schedule.every(10).seconds.do(analyseWorkstation).tag('analysis')

        while True:
                schedule.run_pending()
                time.sleep(1)
                print("Counter:", global_counter)
                if (global_counter == 1):
                        schedule.clear('analysis')
                        print("Exiting the While Loop.")
                        break

        sys.exit()
