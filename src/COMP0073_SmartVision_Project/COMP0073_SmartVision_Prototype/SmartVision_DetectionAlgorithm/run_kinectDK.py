# Module Description: This Module triggers the Azure Kinect Controller System, by invoking its executable file. This causes the Kinect DK to capture a colour and depth image.
import subprocess
import os
import sys


def executeKinectDKinC():
    """
        This function executes the Azure_Kinect_Controller System's executable file.
    """
    # Original Path on the developer's machine:
    #path_to_controller = "C:\\Users\\const\\COMP0073_SmartVision_Project\\Azure_Kinect_Controller\\Debug\\Azure_Kinect_Controller.exe"
    # Flexible path looks up the directory of this file and then moves to the known location of the Azure_Kinect_Controller executable file from this position.
    path_to_controller = os.path.join(os.path.dirname(__file__), "..", "..", "Azure_Kinect_Controller\\Debug\\Azure_Kinect_Controller.exe")
    subprocess.run([r""+path_to_controller])




if(__name__=="__main__"):
    executeKinectDKinC()
    print("CWD:" + os.getcwd()) # to check whether the default working environment is restored
    #print(os.path.join(os.path.dirname(__file__), "..", "..", "Azure_Kinect_Controller\\Debug\\Azure_Kinect_Controller.exe"))
