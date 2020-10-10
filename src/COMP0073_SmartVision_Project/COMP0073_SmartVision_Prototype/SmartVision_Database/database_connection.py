# Module Description: This module handles all the communication between the SmartVision system and the MySQL database.
import mysql.connector
from mysql.connector import Error
import os
import sys
from datetime import date, datetime

# Running the SmartVision application via the Flask application and via the VSCode
# influenced the working directories. Consequntly, a problem occurred with the relative import of this module.
# The existing workaround, which has been used in the other scripts worked to solve it.
currentDir = os.getcwd() # get the current working directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..",".."))) # move up two folders, due to issue with relative import
#print("CWD:" + os.getcwd()) # prints current working directory to confirm folder move
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.config as config # import library
os.chdir(currentDir) # return to initial working directory to prevent issue reading files
#print("CWD:" + os.getcwd())



def connectToDatabase():
    """
        Description: This method establishes a connection to the MySQL database.
        Input: Nothing
        Output: Dictionary of Form -> {'valid_DB_connection': validDBconnection, 'DB_connection': DBconnection}
    """
    try:
        DBconnection = mysql.connector.connect(host=config.DB_host, user=config.DB_user, 
        password=config.DB_password, database=config.DB_database)

        if DBconnection.is_connected():
            validDBconnection = True
        
        return {'valid_DB_connection': validDBconnection, 'DB_connection': DBconnection}        

    except Error as e:
        print("An error occurred while connecting to the SmartVision MySQL Database:", e)



def retrieve_customObjectScore_toDict():
    """
        Description: # Retrieving the object scores from all customVision objects into a dictionary from the database
        Input: Nothing
        Output: Dictionary of Form -> {'object name': object score, ...}
    """
    try:
            database = connectToDatabase()
            connectionDB = database['DB_connection']
            DBcursor = connectionDB.cursor()

            DBcursor.execute("SELECT * FROM customvisionobjectscore")

            DBresult = DBcursor.fetchall()

            object_score = {}
            for tuples in DBresult:
                    object_score[tuples[1]] = tuples[2]
            
            return object_score

    except Error as e:
            print("An error occurred while inserting something into the databaseSmartVision:", e)

    finally:
            DBcursor.close()



def update_probabilityThresholds(analysed_item, prob_threshold):
    """
        Description: Updates the probability threshold of a selected item in the probabilitythresholds table.
        Input: (analysed_item -> string), (prob_threshold -> float)
        Output: Retunrns Boolean True if successful otherwise false.
    """
    try:
        prob_threshold = str(prob_threshold)
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor()

        mysql = "UPDATE probabilityThresholds SET prob_threshold = %s WHERE analysed_item = %s"
        values = (prob_threshold, analysed_item)

        DBcursor.execute(mysql, values)

        connectionDB.commit()

        print(DBcursor.rowcount, "record(s) affected")

        return True
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



def update_customvisionobjectscore(object_name, object_score):
    """
        Description: Updates the object score of a selected objected from the customvisionobjects table.
        Input: (object_item -> string), (object_score -> float)
        Output: Retunrns Boolean True if successful otherwise false.
    """
    try:
        object_score = str(object_score)
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor()

        mysql = "UPDATE customvisionobjectscore SET object_score = %s WHERE object_name = %s"
        values = (object_score, object_name)

        DBcursor.execute(mysql, values)

        connectionDB.commit()

        print(DBcursor.rowcount, "record(s) affected")

        return True
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



def retrieve_probThreshold(anaylsed_item):
    """
        Description: Retrieve the probability threshold of a selected item from the probabilitythresholds table.
        Input: (analysed_item -> string)
        Output: List -> [prob_threshold].
    """
    try:
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor()

        mysql = "SELECT prob_threshold FROM probabilitythresholds WHERE analysed_item = %s"
        values = (anaylsed_item, )

        DBcursor.execute(mysql, values)

        dbResult = DBcursor.fetchone()

        print(DBcursor.rowcount, "record(s) affected")

        return dbResult
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



def insert_customvisionobjectscore(object_name, object_score):
    """
        Description: Inserts the object score and object_name into the customvisionobjects table.
        Input: (object_name -> string), (object_score -> float)
        Output: Retunrns Boolean True if successful.
    """
    try:
        object_score = str(object_score)
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor()

        mysql = "INSERT INTO customvisionobjectscore (object_name, object_score) VALUES (%s, %s)"
        values = (object_name, object_score)

        DBcursor.execute(mysql, values)

        connectionDB.commit()

        print(DBcursor.rowcount, "record(s) affected")

        return True
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()




def insert_frameanalysis(occupied, occupation_score, person_detected, dominant_emotion, smile, time_recorded):
    """
        Description: Inserts an analysed frame into the table frameanalysis of the database.
        Input: (occupied -> boolean), (occupation_score -> int), (person_detected -> boolean), (dominant_emotion -> string), (smile -> boolean), (time_recorded -> timestamp)
        Output: Retunrns Boolean True if successful.
    """
    try:
        occupation_score = str(occupation_score)
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor()

        mysql = "INSERT INTO frameanalysis (occupied, occupation_score, person_detected, dominant_emotion, smile, time_recorded) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (occupied, occupation_score, person_detected, dominant_emotion, smile, time_recorded)

        DBcursor.execute(mysql, values)

        connectionDB.commit()

        print(DBcursor.rowcount, "record(s) affected")

        return True
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



def retrieve_Admin(email):
    """
        Description: Retrieves developer's data based on the unique identifier email from the developer table in the database.
        Input: (email -> string)
        Output: List -> [developer_id, email, password, first_name]
    """
    try:
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor()

        query = "SELECT developer_id, email, password, first_name FROM developer WHERE email = %s"
        values=(email, )
        DBcursor.execute(query, values)
        DBresult = DBcursor.fetchone()

        return DBresult
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



def retrieve_AllAdminData():
    """
        Description: Retrieves all developer data from the developer table in the database.
        Input: Nothing
        Output: List -> [[developer_id, first_name, last_name, institution, department, email], ...]
    """
    try:
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor()

        query = "SELECT developer_id, first_name, last_name, institution, department, email FROM developer"
        DBcursor.execute(query)
        DBresult = DBcursor.fetchall()

        return DBresult
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



def retrieveSingleAdminData(developer_id):
    """
        Description: Retrieves Admin Data for a single entry based on an developer_id from the developer table in the database.
        Input: (email -> string)
        Output: List -> (developer_id (int), email (string), password (string))
    """
    try:
        developer_id = str(developer_id)
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor()

        query = "SELECT developer_id, email, password, first_name, last_name, institution, department FROM developer WHERE developer_id = %s"
        values = (developer_id, )
        DBcursor.execute(query, values)
        DBresult = DBcursor.fetchone()

        return DBresult
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



def update_adminPassword(password, developer_id):
    """
        Description: Updates the Password of a selected Admin, based on the developer_id, in the developer table in the database.
        Input: (password -> string), (developer_id -> int)
        Output: If successful it returns True, else it returns False.
    """
    try:
        developer_id = str(developer_id)
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor()

        mysql = "UPDATE developer SET password = %s WHERE developer_id = %s"
        values = (password, developer_id)

        DBcursor.execute(mysql, values)

        connectionDB.commit()

        if(DBcursor.rowcount > 0):
            return True
        else:
            return False
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



def checkForAdminEmail(developer_email):
    """
        Description: Retrieves an email of an admin if it exists from the developer table in the database.
        Input: (developer_email -> string)
        Output: It it exists (email, ...), otherwise "None".
    """
    try:
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor()

        query = "SELECT email FROM developer WHERE email = %s"
        values = (developer_email, )
        DBcursor.execute(query, values)
        DBresult = DBcursor.fetchone()

        return DBresult
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



def update_adminDetails(developer_id, firstName, lastName, email, institution, department):
    """
        Description: Updates the account details of a selected Admin, based on the developer_id, in the developer table in the database.
        Input: (developer_id -> int), (firstName -> string), (lastName -> string), (email -> string), (institution -> string), (department -> string)
        Output: If successful it returns True, else it returns False.
    """
    try:
        developer_id = str(developer_id)
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor()

        mysql = "UPDATE developer SET first_name=%s, last_name=%s, email=%s, institution=%s, department=%s WHERE developer_id = %s"
        values = (firstName, lastName, email, institution, department, developer_id)

        DBcursor.execute(mysql, values)

        connectionDB.commit()

        if(DBcursor.rowcount > 0):
            return True
        else:
            return False
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



def insert_adminDetails(firstName, lastName, email, institution, department, password):
    """
        Description: Inserts Admin details into the table developer of the database.
        Input: (firstName -> string), (lastName -> string), (email -> string), (institution -> string), (department -> string), (password -> string)
        Output: Retunrns Boolean True if successful.
    """
    try:
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor()

        mysql = "INSERT INTO developer (first_name, last_name, institution, department, email, password) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (firstName, lastName, institution, department, email, password)

        DBcursor.execute(mysql, values)

        connectionDB.commit()

        print(DBcursor.rowcount, "record(s) affected")

        return True
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



def delete_admin(developer_id):
    """
        Description: Deletes an Admin from the table developer of the database, based on the developer_id.
        Input: (developer_id -> int)
        Output: Retunrns Boolean True if successful.
    """
    try:
        developer_id = str(developer_id)
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor()

        mysql = "DELETE FROM developer WHERE developer_id = %s"
        values = (developer_id,)

        DBcursor.execute(mysql, values)

        connectionDB.commit()

        print(DBcursor.rowcount, "record(s) affected")

        return True
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



#retrieves last added row in the table frameanalysis and returns the values of the row: (frame_id (int), occupied (boolean), occupation_score (int), person_detected (boolean), dominant_emotion (string), smile (boolean) time_recorded (timestamp))
def retrieveLatestFrameAnalysis():
    """
        Description: Retrieves the lastest analysed frame from the table frameanalysis in the database, by soriting it in descending order and only displaying the first row.
        Input: Nothing
        Output: List -> (frame_id (int), occupied (boolean), occupation_score (int), person_detected (boolean), dominant_emotion (string), smile (boolean), time_recorded (timestamp))
    """
    try:
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor()

        query = "SELECT * FROM frameanalysis ORDER BY frame_id DESC LIMIT 1"

        DBcursor.execute(query,)
        DBresult = DBcursor.fetchone()

        return DBresult
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



def retrieveTablecustomvisionobjectscore():
    """
        Description: Retrieves all entries from table customvisionobjectscore.
        Input: Nothing
        Output: List -> [(object_id, object_name, object_score), ...]
    """
    try:
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor()

        query = "SELECT * FROM customvisionobjectscore"

        DBcursor.execute(query,)
        DBresult = DBcursor.fetchall()

        return DBresult
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



def retrieveTableprobabilitythresholds():
    """
        Description: Retrieves all entries from table probabilitythresholds.
        Input: Nothing
        Output: List -> [(threshold_id, analysed_item, prob_threshold), ...]
    """
    try:
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor()

        query = "SELECT * FROM probabilitythresholds"

        DBcursor.execute(query,)
        DBresult = DBcursor.fetchall()

        return DBresult
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



def retrieve_dailyOccupationCount():
    """
        Description: Query retrieves the daily count, how often the workstation was occupied or not.
        Input: Nothing
        Output: List -> [{'occupied': 0, 'count_occupied': 1}, {'occupied': int, 'count_occupied': int}]
    """
    try:
        today = datetime.now().day
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor(dictionary=True)

        query = "SELECT occupied, COUNT(occupied) AS count_occupied FROM frameanalysis WHERE DAY(time_recorded) = %s GROUP BY occupied"
        values=(today,)
        DBcursor.execute(query, values)
        DBresult = DBcursor.fetchall()

        return DBresult
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



def retrieve_lastWeeks_OccupationCount():
    """
        Description: Query retrieves the last week's count, how often the workstation was occupied or not.
        Input: Nothing
        Output: List -> [{'occupied': 0, 'count_occupied': 1}, {'occupied': int, 'count_occupied': int}]
    """
    try:
        current_date = datetime.now()
        year, week_num, day_of_week = current_date.isocalendar()
        week_num -=1
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor(dictionary=True)

        query = "SELECT occupied, COUNT(occupied) AS count_occupied FROM frameanalysis WHERE WEEKOFYEAR(time_recorded) = %s GROUP BY occupied"
        values=(week_num,)
        DBcursor.execute(query, values)
        DBresult = DBcursor.fetchall()

        return DBresult
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



def retrieve_months_OccupationCount(month):
    """
        Description: Query retrieves the count, how often the workstation was occupied or not, for a provided month. The input must be a number between 1 and 12.
        Input: (month -> int)
        Output: List -> [{'occupied': 0, 'count_occupied': 1}, {'occupied': int, 'count_occupied': int}]
    """
    try:
        year = str(datetime.now().year)
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor(dictionary=True)

        query = "SELECT occupied, COUNT(occupied) AS count_occupied FROM frameanalysis WHERE (MONTH(time_recorded) = %s AND YEAR(time_recorded)=%s) GROUP BY occupied"
        values=(month, year)
        DBcursor.execute(query, values)
        DBresult = DBcursor.fetchall()

        return DBresult
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



def retrieve_currentYear_OccupationCount():
    """
        Description: Query retrieves the count, how often the workstation was occupied or not, for the current year.
        Input: Nothing
        Output: List -> [{'occupied': 0, 'count_occupied': 1}, {'occupied': int, 'count_occupied': int}]
    """
    try:
        year = str(datetime.now().year)
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor(dictionary=True)

        query = "SELECT occupied, COUNT(occupied) AS count_occupied FROM frameanalysis WHERE YEAR(time_recorded)=%s GROUP BY occupied"
        values=(year, )
        DBcursor.execute(query, values)
        DBresult = DBcursor.fetchall()

        return DBresult
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



def retrieve_dailyEmotionCount():
    """
        Description: Query retrieves the daily count of the various emotions, which were detected throughout the day.
        Input: Nothing
        Output: (Note, this is an example and may include more or less emotions) List -> [{'dominant_emotion': 'face occluded', 'count_emotions': 1}, {'dominant_emotion': 'neutral', 'count_emotions': 1}, {'dominant_emotion': 'no face', 'count_emotions': 2}]
    """
    try:
        today = str(datetime.now().day)
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor(dictionary=True)

        query = "SELECT dominant_emotion, COUNT(dominant_emotion) AS count_emotions FROM frameanalysis WHERE DAY(time_recorded) = %s GROUP BY dominant_emotion"
        values=(today,)
        DBcursor.execute(query, values)
        DBresult = DBcursor.fetchall()

        return DBresult
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



def retrieve_lastWeeks_Emotions():
    """
        Description: Query retrieves last week's count of the various emotions, which were detected throughout the day.
        Input: Nothing
        Output: (Note, this is an example and may include more or less emotions) List -> [{'dominant_emotion': 'face occluded', 'count_emotions': 1}, {'dominant_emotion': 'neutral', 'count_emotions': 1}, {'dominant_emotion': 'no face', 'count_emotions': 2}]
    """
    try:
        current_date = datetime.now()
        year, week_num, day_of_week = current_date.isocalendar()
        week_num -=1
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor(dictionary=True)

        query = "SELECT dominant_emotion, COUNT(dominant_emotion) AS count_emotions FROM frameanalysis WHERE WEEKOFYEAR(time_recorded) = %s GROUP BY dominant_emotion"
        values=(week_num,)
        DBcursor.execute(query, values)
        DBresult = DBcursor.fetchall()

        return DBresult
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



def retrieve_months_Emotions(month):
    """
        Description: Query retrieves any month's count of the various emotions, which were detected throughout the day.
        Input: (month -> int, must be between 1 and 12) 
        Output: (Note, this is an example and may include more or less emotions) List -> [{'dominant_emotion': 'face occluded', 'count_emotions': 1}, {'dominant_emotion': 'neutral', 'count_emotions': 1}, {'dominant_emotion': 'no face', 'count_emotions': 2}]
    """
    try:
        year = str(datetime.now().year)
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor(dictionary=True)

        query = "SELECT dominant_emotion, COUNT(dominant_emotion) AS count_emotions FROM frameanalysis WHERE (MONTH(time_recorded) = %s AND YEAR(time_recorded)=%s) GROUP BY dominant_emotion"
        values=(month, year)
        DBcursor.execute(query, values)
        DBresult = DBcursor.fetchall()

        return DBresult
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



def retrieve_currentYear_Emotions():
    """
        Description: Query retrieves the current year's count of the various emotions, which were detected throughout the day.
        Input: Nothing
        Output: (Note, this is an example and may include more or less emotions) List -> [{'dominant_emotion': 'face occluded', 'count_emotions': 1}, {'dominant_emotion': 'neutral', 'count_emotions': 1}, {'dominant_emotion': 'no face', 'count_emotions': 2}]
    """
    try:
        year = str(datetime.now().year)
        database = connectToDatabase()
        connectionDB = database['DB_connection']
        DBcursor = connectionDB.cursor(dictionary=True)

        query = "SELECT dominant_emotion, COUNT(dominant_emotion) AS count_emotions FROM frameanalysis WHERE YEAR(time_recorded)=%s GROUP BY dominant_emotion"
        values=(year, )
        DBcursor.execute(query, values)
        DBresult = DBcursor.fetchall()

        return DBresult
        
    except Error as e:
        print("An error occurred while inserting something into the databaseSmartVision:", e)
        
    finally:
        DBcursor.close()



# tester function to check the database connection 
def testDb(name):
    database = connectToDatabase()
    connectionDB = database['DB_connection']
    DBcursor = connectionDB.cursor()
    query = "SELECT first_name FROM developer WHERE email = %s"
    values = (name,)
    DBcursor.execute(query, values)

    DBresult = DBcursor.fetchall()

    for tuples in DBresult:
            name = tuples[0]

    return name





if(__name__ == '__main__'):
    print("===== Database Connection Module =====")
    #currentDir = os.getcwd() # get the current working directory
    #print("Current Working Directory:", currentDir)
    #print(testDb("root.developer@smartvision.com"))
    #print(retrieveSingleAdminData("1"))
    #print(update_adminPassword('SmartVision12345', 1))
    #print(checkForAdminEmail("email.notExisting@smartVision.com"))
    #print(update_adminDetails(1, "RootDeveloper", "RootDeveloper", "rootdeveloper@smartvision.com", "Developer", "Developer"))
    #print(retrieveLatestFrameAnalysis())
    #print(len(retrieveTablecustomvisionobjectscore()))
    #print(type(retrieveTableprobabilitythresholds()))
    #print(update_customvisionobjectscore("pencil", 5))
    #print(update_probabilityThresholds("smile", 0.03))
    #print(retrieve_probThreshold("smile"))
    #print(retrieve_Admin("root.developer@smartvision.com"))
    #print(retrieve_dailyOccupationCount())
    #print(retrieve_dailyEmotionCount())
    #print(retrieve_months_OccupationCount(8))
    #print(retrieve_currentYear_OccupationCount())
    #print(retrieve_lastWeeks_Emotions())
    #print(retrieve_lastWeeks_OccupationCount())
    #print(retrieve_months_Emotions(8))
    #print(retrieve_currentYear_Emotions())

