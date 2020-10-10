# Module Description: This module contains a helper function for better accessing files in different directories. 
import os.path

# Note: As the Flask application changes the working directory, there are two accessing modes: 
# To execute the scripts from VSCode the return string has to look as follows: currentDirectory+"\\COMP0073_SmartVision_Prototype"+"\\"+targetFolderName+"\\"
# To execute the scripts from the Flask Application the return string has to look as follows: currentDirectory+"\\.."+"\\"+targetFolderName+"\\"
def createTargetDirectory(targetFolderName):
    """
        Description: This method manipulates its current directory in such a way, that it returns the target directory in order to address folders contained in the COMP0073_SmartVision_Prototype package. 
        Input: (targetFolderName -> string)
        Output: file path in form of a string to the target folder.
    """
    currentDirectory = os.getcwd()
    return currentDirectory+"\\.."+"\\"+targetFolderName+"\\"



if(__name__ == '__main__'):

    currentDirectory = os.getcwd()
    currentFolderName = os.path.basename(currentDirectory)
    indexCurrentFolderName = currentDirectory.find(currentFolderName)
    targetDirectory = currentDirectory[0:indexCurrentFolderName]

    print (currentDirectory)
    print(currentFolderName)
    print(createTargetDirectory("Images"))