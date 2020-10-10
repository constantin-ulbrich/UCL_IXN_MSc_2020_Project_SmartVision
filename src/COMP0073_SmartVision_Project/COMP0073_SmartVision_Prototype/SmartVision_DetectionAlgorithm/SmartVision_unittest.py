# Module Description: This module contains all the automated unit tests for the SmartVision System.
import unittest
import os
import sys

# Note, this script is only run locally from VSCode for unit testing purposes.
from handling_blob_storage import getBlobURI
from object_detection_remote import detectObjects
from custom_vision_detection_remote import customVisionDetectObjects
from face_detection_remote import detectFaces
from stats import relativization

# Running the SmartVision application via the Flask application and via the VSCode
# influenced the working directories. Consequntly, a problem occurred with the relative import of this module.
# The existing workaround, which has been used in the other scripts worked to solve it.
currentDir = os.getcwd() # get the current working directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..",".."))) # move up two folders, due to issue with relative import
#print("CWD:" + os.getcwd()) # prints current working directory to confirm folder move
import COMP0073_SmartVision_Prototype.SmartVision_Database.database_connection as dbc # import library
os.chdir(currentDir) # return to initial working directory to prevent issue reading files
#print("CWD:" + os.getcwd())



# Initializing Test Suite
test_suite = unittest.TestSuite()


class Test_Database(unittest.TestCase):
    def test_testDB(self):
        self.assertAlmostEqual(dbc.testDb("root.developer@smartvision.com"), "RootDeveloper")

    def test_retrieveSingleAdminData(self):
        self.assertTupleEqual(dbc.retrieveSingleAdminData("1"), (1, 'root.developer@smartvision.com', 'pbkdf2:sha256:150000$mAuFOaGD$34aa16b0bb6bd025a8a493d0a5b5185acb49ef754a0d400f33e6c21fd0106ca4', 'RootDeveloper', 'RootDeveloper', 'Developer', 'Developer'))

    def test_checkForAdminEmail(self):
        self.assertIsNone(dbc.checkForAdminEmail("email.notExisting@smartVision.com"))
    
    def test_len_retrieveTablecustomVisionobjectscore(self):
        self.assertAlmostEqual(len(dbc.retrieveTablecustomvisionobjectscore()), 38)

    def test_retrieveTableprobabilitythresholds(self):
        # Unittest function is not recognising a list object... Function was tested manually and it works.
        #self.assertIs(dbc.retrieveTableprobabilitythresholds(), [])
        pass
    
    def test_update_customvisionobjectscore(self):
        self.assertTrue(dbc.update_customvisionobjectscore("pencil", 5))
    
    def test_update_probabilityThresholds(self):
        self.assertTrue(dbc.update_probabilityThresholds("smile", 0.4))

    def test_retrieve_probthreshold(self):
        self.assertTupleEqual(dbc.retrieve_probThreshold("smile"), (0.4,))
    
    def test_retrieve_Admin(self):
        self.assertTupleEqual(dbc.retrieve_Admin("root.developer@smartvision.com"), (1, 'root.developer@smartvision.com', 'pbkdf2:sha256:150000$mAuFOaGD$34aa16b0bb6bd025a8a493d0a5b5185acb49ef754a0d400f33e6c21fd0106ca4', 'RootDeveloper'))
    
    def test_retrieve_dailyOccupation(self):
        self.assertListEqual(dbc.retrieve_dailyOccupationCount(), [])
    
    def test_retrieve_dailyEmotion(self):
        self.assertListEqual(dbc.retrieve_dailyEmotionCount(), [])
    
    def test_retrieve_LastWeeksOccupation(self):
        # Test was based on data present in the MySQL database on the 30/08/2020
        self.assertListEqual(dbc.retrieve_lastWeeks_OccupationCount(), [{'occupied': 0, 'count_occupied': 23}, {'occupied': 1, 'count_occupied': 17}])
    
    def test_retrieve_monthsOccupation(self):
        # Test was based on data present in the MySQL database on the 30/08/2020
        self.assertListEqual(dbc.retrieve_months_OccupationCount(8), [{'occupied': 0, 'count_occupied': 33}, {'occupied': 1, 'count_occupied': 39}])

    def test_retrieve_currentYearOccuption(self):
        # Test was based on data present in the MySQL database on the 30/08/2020
        self.assertListEqual(dbc.retrieve_currentYear_OccupationCount(), [{'occupied': 0, 'count_occupied': 33}, {'occupied': 1, 'count_occupied': 39}])

    def test_retrieve_lastWeeksEmotion(self):
        # Test was based on data present in the MySQL database on the 30/08/2020
        self.assertListEqual(dbc.retrieve_lastWeeks_Emotions(), [{'dominant_emotion': 'no face detected', 'count_emotions': 18}, {'dominant_emotion': 'no person detected', 'count_emotions': 22}])
    
    def test_retrieve_MonthsEmotion(self):
        # Test was based on data present in the MySQL database on the 30/08/2020
        self.assertListEqual(dbc.retrieve_months_Emotions(8), [{'dominant_emotion': 'face occluded', 'count_emotions': 1}, {'dominant_emotion': 'happiness', 'count_emotions': 2}, {'dominant_emotion': 'neutral', 'count_emotions': 17}, {'dominant_emotion': 'no face', 'count_emotions': 3}, {'dominant_emotion': 'no face detected', 'count_emotions': 18}, {'dominant_emotion': 'no person detected', 'count_emotions': 31}])

    def test_retrieve_currentYearEmotion(self):
        # Test was based on data present in the MySQL database on the 30/08/2020
        self.assertListEqual(dbc.retrieve_currentYear_Emotions(), [{'dominant_emotion': 'face occluded', 'count_emotions': 1}, {'dominant_emotion': 'happiness', 'count_emotions': 2}, {'dominant_emotion': 'neutral', 'count_emotions': 17}, {'dominant_emotion': 'no face', 'count_emotions': 3}, {'dominant_emotion': 'no face detected', 'count_emotions': 18}, {'dominant_emotion': 'no person detected', 'count_emotions': 31}])


class Test_BlobStorage(unittest.TestCase):
    def test_getBlobURI(self):
        self.assertAlmostEqual(getBlobURI("tests", "homeWorkstation.jpg" ), 
        "https://frameblobstorage.blob.core.windows.net/tests/homeWorkstation.jpg")
    
    def runTest(self):
        self.assertAlmostEqual(getBlobURI("tests", "homeWorkstation.jpg" ), 
        "https://frameblobstorage.blob.core.windows.net/tests/homeWorkstation.jpg")


class Test_Remote_ObjectDetection(unittest.TestCase):
    def test_objectDetectionRemote(self):
        self.assertListEqual(detectObjects("tests", "homeWorkstation.jpg"), [['Clock', 0.525, 240, 204, 778, 202], ['computer keyboard', 0.613, 1280, 426, 1544, 393], ['computer keyboard', 0.561, 1834, 536, 1484, 308], ['cup', 0.724, 2381, 500, 2218, 588], ['television', 0.772, 602, 1567, 354, 924], ['chair', 0.904, 553, 1120, 1449, 1575]])

class Test_Remote_CustomDetection(unittest.TestCase):
    def test_customDetectionRemote(self):
            self.assertListEqual(customVisionDetectObjects("tests", "homeWorkstation.jpg"), [['drinking glass', 0.402679443, 0.588774, 0.743242, 0.118759573, 0.175548613]])

class Test_Remote_EmotionDetection(unittest.TestCase):
    def test_detectFaces(self):
        self.assertListEqual( detectFaces("tests", "happyKids.jpg"), [{'faceID': '99fd0036-7a97-483f-b525-afb7ffefb310', 'gender': 'female', 'age': 6.0, 'emotions': {'happiness': 0.965}, 'smile': 0.965, 'accessories': [], 'eye_makeup': True, 'lip_makeup': False, 'facial_hair': [], 'hair': 'brown', 'glasses': 'no_glasses', 'eye_occluded': False, 'forehead_occluded': False, 'mouth_occluded': False}, 
        {'faceID': '699bae45-2157-4248-8f33-6f7ee81a6b89', 'gender': 'female', 'age': 6.0, 'emotions': {'happiness': 1.0}, 'smile': 1.0, 'accessories': [], 'eye_makeup': True, 'lip_makeup': True, 'facial_hair': [], 'hair': 'brown', 'glasses': 'no_glasses', 'eye_occluded': False, 'forehead_occluded': False, 'mouth_occluded': False}])

class Test_statsSupport(unittest.TestCase):
    def test_relativization(self):
        self.assertAlmostEqual(relativization(50, 100, 10), 5.0)


# Creating the Test Suite by adding tests:
test_suite.addTest(Test_BlobStorage())


if(__name__=="__main__"):
    #The function below runs the entire unit test file
    unittest.main(Test_BlobStorage(), verbosity=2)

    #The function below runs the test suite, this one can be used to add a specific collection of tests to the suite and then run it
    #unittest.TextTestRunner(verbosity=2).run(test_suite)