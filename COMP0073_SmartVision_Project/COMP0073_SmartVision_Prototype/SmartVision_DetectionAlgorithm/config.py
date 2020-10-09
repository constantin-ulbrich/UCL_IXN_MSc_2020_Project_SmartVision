# Module Description: This file is the configuration file for all services related to the SmartVision Algorithm

"""
    Configuration to take image via the Webcam or using the integrated and programmed Azure Kinect DK:
    If you set the visual sensor variable to "azure_kinect_dk", then the SmartVision algorithm will use
    the integrated and programmed Azure Kinect DK, by promting the Azure_Kinect_Controller System.
    If the variable is set to "webcam", then the webcam of the local machine is used (also the webcam
    configurations apply).
"""
visual_sensor = "azure_kinect_dk"


"""
    Configuration of the Webcam:
    Selecting the webcam 0 is usually the default integrated, front-facing webcam.
    To use the Azure Kinect DK as your webcam, set the variable equal to 1 or 2, 
    depending on the number of cameras you have in your device.
"""
webcam = 2


"""
    Configuration of the database:
    This is a configuration for a local database.
"""
DB_host="localhost"
DB_user="smartVisionUser"
DB_password="12345SmartVision"
DB_database="smartvisiondatabase"


"""
    Configuration of the Azure Computer Vision Service in object_detection_remote.py:
"""
ACV_endpoint = "[Insert your Azure Computer Vision Service Endpoint]"
ACV_subscription_key = "[Insert your Azure Computer Vision Subscription Key]"


"""
    Configuration of the Azure Custom Vision Service in custom_vision_detection_remote.py (Note, this project used a custom made detection model to detect
    objects, which are usually found on a workstation, to support the precision of the detection capabilities of the SmartVision system. Access to this model 
    might be granted if permission is obtained from the author and Avanade.):
"""
#Custom Vision Azure Authentication Keys
ACCV_endpoint = "[Insert your Azure Custom Vision Service Endpoint]"
ACCV_subscription_key = "[Insert your Azure Custom Vision Service Subscription Key]"
ACCV_prediction_key = "[Insert your Azure Custom Vision Service Prediction Key"
#Custom Vision Azure Project Credentials
ACCV_project_id = "[Insert your Azure Custom Vision Project ID]"
ACCV_published_name = "[Insert your Azure Custom Vision Project Published Name]"


"""
    Configuration of the Azure Face Service in face_detection_remote.py:
"""
#Computer Vision Azure Authentication Keys
AFD_endpoint = "[Insert your Azure Face Service Endpoint]"
AFD_subscription_key = "[Insert your Azure Face Service Subscription Key]"


"""
    Configuration of the Azure Blob Storage in handling_blob_storage.py (Note in case you are setting up a new blob storage account, the blob storage needs to 
    contain four containers with the names: "analysedframes", "frames", "lasttakenframe", and "tests".):
"""
# Azure Blob Storage Authentication Credentials
azure_blob_key = "[Insert your Azure Blob Storage Key]"
azure_blob_connection_string = "[Insert your Azure Blob Storage Connection String]"
