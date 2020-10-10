# Module Description: This module handles every interaction of the SmartVision System with the Azure Blob Storage.
# Note, the code was written with the support of the Azure Blob Storage Documentation (https://docs.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob?view=azure-python)
import os
import sys
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# To run the script locally from VSCode, uncomment the import statement(s) below:
#import directory_manipulation as dm
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
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.config as config # import library
os.chdir(currentDir) # return to initial working directory to prevent issue reading files
#print("CWD:" + os.getcwd()) # to check whether the default working environment is restored

# Azure Blob Storage Authentication Credentials
blob_key = config.azure_blob_key
blob_connection_string = config.azure_blob_connection_string


def uploadBlob(targetContainer, imageName, blobName, imageType):
    """
        Description: The function reads in an image saved in the File "Images" and uploads the binary stream into an Azure Blob. 
        Input: (targetContainer -> string), (imageName -> string), (blobName -> string), (imageType -> string)
        Output: Prints "Blob Successfully Uploaded" to the console upon success.
    """
    try:
        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=targetContainer, blob=blobName)
        #create localImagePath:
        localImagePath = dm.createTargetDirectory("Images")+imageName
        # Upload the created file
        with open(localImagePath, "rb") as image:
            blob_client.upload_blob(image, overwrite=True)

        print("\nBlob Successfully Uploaded\n")

    except Exception as ex:
        print('Exception:')
        print(ex)


def uploadBlob_fromByteStream(targetContainer, blobName, image_byteStream):
    """
        Description: The function attempts to upload a byte stream of an image directly into an Azure Blob. 
        Input: (targetContainer -> string), (blobName -> string), (image_byteStream -> binary)
        Output: Prints "Blob Successfully Uploaded" to the console upon success.
    """

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
    
    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=targetContainer, blob=blobName)

    blob_client.upload_blob(image_byteStream, overwrite=True)

    print("\nBlob Successfully Uploaded\n")




def downloadBlob(targetContainer, blobName):
    """
        Description: The function downloads an image blob from an Azure Blob storage and returns the downloaded image stream as a byte stream. 
        Input: (targetContainer -> string), (blobName -> string)
        Output: (download_image_stream -> byte stream)
    """
    try:
        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
        
        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=targetContainer, blob=blobName)

        download_blob = blob_client.download_blob()
        #download_blob = blob_client.download_blob().readall() # For testing purposes
        #print("Blob size:", download_blob.size) # For testing purposes
        #print("Blob Name:", download_blob.name) # For testing purposes
        #print()
         
        download_image_stream = download_blob.content_as_bytes()

        if(download_image_stream == None):
            print("The image stream is null")

        print("Blob Successfully Downloaded\n")

        return download_image_stream
    
    except Exception as ex:
        print('Exception:')
        print(ex)



def deleteBlob(targetContainer, blobName):
    """
        Description: The function deletes a blob from an Azure Blob. 
        Input: (targetContainer -> string), (blobName -> string)
        Output: Prints "Blob Successfully Deleted" to the console upon success.
    """
    try:
        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
        
        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=targetContainer, blob=blobName)

        # delete the targetted blob
        blob_client.delete_blob()

        print("\nBlob Successfully Deleted\n")

    except Exception as ex:
        print('Exception:')
        print(ex)



def getBlobURI(targetContainer, blobName):
    """
        Description: The function gets the image URL from a blob in a Azure Blob storage. 
        Input: (targetContainer -> string), (blobName -> string)
        Output: (blobURL -> string).
    """
    try:
        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
        
        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=targetContainer, blob=blobName)

        # delete the targetted blob
        blobURL = blob_client.url

        #print("\nBlob URL:", blobURL, "\n")

        return blobURL

    except Exception as ex:
        print('Exception:')
        print(ex)





if(__name__ == '__main__'):
    print("===== Blob Storage Handling =====\n\n")
    print(getBlobURI("tester", "homeWorkstation.jpg"))
    