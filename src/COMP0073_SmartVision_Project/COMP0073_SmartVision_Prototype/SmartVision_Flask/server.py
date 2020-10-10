# Module Description: This module contains all the server functionality of the Flask Web-Application for the SmartVision System.
# The the flask documentation and the following "get started" sources were used to gain a general understanding for building a flask application:
# (Get Started Source: https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3), (Get Started Source: https://www.linkedin.com/learning/flask-grundkurs/willkommen-zum-flask-grundkurs?u=69919578)

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sys
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from operator import itemgetter
import matplotlib as plt
from threading import Thread

import COMP0073_SmartVision_Prototype.SmartVision_Database.database_connection as dbc
from COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.main_programme_logic import analyseWorkstation, runSmartVisionAlgorithm, set_variable_global_running
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.handling_blob_storage as hbs
import COMP0073_SmartVision_Prototype.SmartVision_DetectionAlgorithm.stats as stats
from COMP0073_SmartVision_Prototype. SmartVision_DetectionAlgorithm.image_modification import modifyAnalysedImage

#Creating an instance of the Flask object, which represents the Web-app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

#Global Variable:
algorithm_running = "off"
thread_smartVisionAlgo = ""




"""This sesction of the code contains all functions related to the home page and to start and stop the SmartVision Algorithm:"""
@app.route("/home")
def displayHome():
    """
        Description: This function displays the index.html page.
        Input: Nothing
        Output: returns index.html
    """
    global algorithm_running

    if(session.get("logged_in") != True):
        return redirect(url_for('displayLogin'))

    #name = dbc.testDb("root.admin@smartvision.com")
    name = session["user_name"]
    return render_template('index.html', name=name, algorithmRunning = algorithm_running)



@app.route("/home", methods=['POST'])
def runAlgorithm():
    """
        Description: This function starts the runSmartVisioinAlgorithm function from the SmartVision_Detection_Algorithm folder,
         if the play button is pressed. It also stops it, if the stop button is pressed. The runSmartVisionAlgorithm function 
         is executed in a thread called thread_smartVisionAlgo 'parallel' to the main thread. This allows to use the other functions
         of the website, while running the SmartVision Algorithm. Once the pause button is pressed, the two threads are joined and the
         runSmartVisionAlgorithm function is stopped.
        Input: via http request -> ['startButton]
        Output: returns index.html
    """
    global algorithm_running
    global thread_smartVisionAlgo
    #Check if user is logged in
    if(session.get("logged_in") != True):
        return redirect(url_for('displayLogin'))
    
    name = session["user_name"]
    
    #Check if startButton is pressed to start running the algorithm
    if(request.form['startButton'] == "start"):
        #set global variable to "on"
        algorithm_running = "on"

        # set global variable in main_programme_logic.py, which controls the SmartVision Algorithm,
        # to "start" to start the algorithm
        set_variable_global_running("start")
        thread_smartVisionAlgo = Thread(target=runSmartVisionAlgorithm)
        # run the smart Vision algorithm 
        thread_smartVisionAlgo.start()
        
        return render_template('index.html', name=name, algorithmRunning = algorithm_running, buttonValue = algorithm_running)

    elif(request.form['startButton'] == "stop"):
        algorithm_running = "off"
        #set global variable in main_programme_logic.py, which controls the SmartVision Algorithm, 
        #to "" to stop the algorithm
        set_variable_global_running("")
        # join the main thread with the thread running the SmartVision Algorithm
        thread_smartVisionAlgo.join()

        return render_template('index.html', name=name, algorithmRunning = algorithm_running, buttonValue = algorithm_running)






"""This sesction of the code contains all functions related to displaying the relevant statistics collected by the SmartVision algorithm, collected in the SmartVision database:"""
@app.route("/statistics")
def displayStatistics():
    """
        Description: This function displays the statistics.html page.
        Input: Nothing
        Output: returns statistics.html
    """
    if(session.get("logged_in") != True):
        return redirect(url_for('displayLogin'))
    
    occupation_stat_image = "../analysed_error_image.png"
    emotion_stat_image = "../analysed_error_image.png"
    default_timePeriod = "lastWeek"

    figure_occupation = stats.plot_pie_occupation("pastWeek")
    if(figure_occupation != False):
        occupation_stat_image = "../static/pie_lastWeek_occupation.png"
    
    figure_emotion = stats.plot_radar_emotions("pastWeek")
    if(figure_emotion != False):
        emotion_stat_image = "../static/radar_lastWeek_emotions.png"
    
    return render_template('statistics.html', timePeriod = default_timePeriod, occupation_stat_image=occupation_stat_image, emotion_stat_image=emotion_stat_image)



@app.route("/statistics", methods=['POST'])
def generateStatistic():
    """
        Description: This function calls various functions of the stats.py file to generate all the relevant graphics of the desired statistics and returns those as images.
        Input: via http request -> ['button_timePeriod']
        Output: returns statistics.html
    """
    #print("Here1") # for debugging purposes
    #Check if user is logged in
    if(session.get("logged_in") != True):
        return redirect(url_for('displayLogin'))
    
    occupation_stat_image = "../analysed_error_image.png"
    emotion_stat_image = "../analysed_error_image.png"
    button_timePeriod = request.form['button_timePeriod']
    #print("Here2") # for debugging purposes
    if(button_timePeriod == "latestAnalysis"):
        #print("Here: Latest Analysis") # for debugging purposes

        # retrieves last added row in the table frameanalysis and returns: 
        # (frame_id (int), occupied (boolean), occupation_score (int), person_detected (boolean), dominant_emotion (string), smile (boolean) time_recorded (timestamp))
        analysisResult = dbc.retrieveLatestFrameAnalysis()
        timeOfAnalysis = analysisResult[6]
        timeOfAnalysis.strftime('%d-%m-%y %H-%M-%S')
        dominantEmotion = analysisResult[4]
        if(analysisResult[1] == True):
            occupied = "occupied"
        else:
            occupied = "not occupied"
        
        modifyAnalysedImage('lasttakenframe', 'tester.jpg')
        analysedImageURL = hbs.getBlobURI("analysedframes", "analysed_workstation.jpg")
        
        return render_template('statistics.html', timePeriod = button_timePeriod, analysisTime=timeOfAnalysis, dominantEmotion=dominantEmotion, occupationStatus=occupied, imageURL = analysedImageURL)
    elif(button_timePeriod == "today"):
        #print("Here: Today") # for debugging purposes
        figure_occupation = stats.plot_pie_occupation("daily")
        if(figure_occupation != False):
            occupation_stat_image = "../static/pie_daily_occupation.png"
        
        figure_emotion = stats.plot_radar_emotions("daily")
        if(figure_emotion != False):
            emotion_stat_image = "../static/radar_daily_emotions.png"
    elif(button_timePeriod == "lastWeek"):
        #print("Here: Last Week") # for debugging purposes
        figure_occupation = stats.plot_pie_occupation("pastWeek")
        if(figure_occupation != False):
            occupation_stat_image = "../static/pie_lastWeek_occupation.png"
        
        figure_emotion = stats.plot_radar_emotions("pastWeek")
        if(figure_emotion != False):
            emotion_stat_image = "../static/radar_lastWeek_emotions.png"
    elif(button_timePeriod[0:5] == "month"):
        #print("Here: Month") # for debugging purposes
        selected_month = int(button_timePeriod[-1])
        figure_occupation = stats.plot_pie_months_occupation(selected_month)
        if(figure_occupation != False):
            occupation_stat_image = "../static/pie_month_occupation.png"
        
        figure_emotion = stats.plot_radar_months_emotions(selected_month)
        if(figure_occupation != False):
            emotion_stat_image = "../static/radar_month_emotions.png"
    elif(button_timePeriod == "currentYear"):
        #print("Here: Current Year") # for debugging purposes
        figure_occupation = stats.plot_pie_occupation("currentYear")
        if(figure_occupation != False):
            occupation_stat_image = "../static/pie_currentYear_occupation.png"
        
        figure_emotion = stats.plot_radar_emotions("currentYear")
        if(figure_emotion != False):
            emotion_stat_image = "../static/radar_currentYear_emotions.png"
    
    #print("Here: rendering new template after else statements") # for debugging purposes
    return render_template('statistics.html', timePeriod = button_timePeriod, occupation_stat_image=occupation_stat_image, emotion_stat_image=emotion_stat_image)






"""This sesction of the code contains all functions related changing the configuration of the SmartVision Algorithm:"""
@app.route("/smartVisionConfig")
def displaySmartVisionConfig():
    """
        Description: This function displays the smartVisionConfig.html page.
        Input: Nothing
        Output: returns smartVisionConfig.html
    """
    if(session.get("logged_in") != True):
        return redirect(url_for('displayLogin'))
    
    result_CustomVisionObjects = dbc.retrieveTablecustomvisionobjectscore()
    numberOfObjects = len(dbc.retrieveTableprobabilitythresholds())
    # Sorting the result list according to the object name
    result_CustomVisionObjects.sort(key=itemgetter(1))
    

    result_probabilityThresholds = dbc.retrieveTableprobabilitythresholds()
    numberProbabilityThresholds = len(result_probabilityThresholds)
    # Sorting the result list according to the object name
    result_probabilityThresholds.sort(key=itemgetter(1))

    return render_template('smartVisionConfig.html', numberOfObjects=numberOfObjects, customVisionObjectList=result_CustomVisionObjects, numberProbThresholds=numberProbabilityThresholds, probabilityThresholdsList=result_probabilityThresholds)



@app.route("/smartVisionConfig", methods=['POST'])
def updateCustomObjects():
    """
        Description: This function updates the object_scores and prob_thresholds in the SmartVision database, based on the provided from input.
        Input: via http request -> ['updateObject'], ['selectedObject'], ['objectScore'], ['updateProbThresholds'], ['selectedItem'], ['probThreshold']
        Output: returns smartVisionConfig.html
    """
    if(session.get("logged_in") != True):
        return redirect(url_for('displayLogin'))

    if(request.form['update'] == 'updateObject'):
        selectedObject = request.form['selectedObject']
        new_objectScore = request.form['objectScore']

        #Insert the new values into the database and update the corresponding table
        if(dbc.update_customvisionobjectscore(selectedObject, new_objectScore)):
            updateSuccessful = True
        else:
            updateSuccessful = False

        result_CustomVisionObjects = dbc.retrieveTablecustomvisionobjectscore()
        numberOfObjects = len(dbc.retrieveTableprobabilitythresholds())
        # Sorting the result list according to the object name
        result_CustomVisionObjects.sort(key=itemgetter(1))
        
        result_probabilityThresholds = dbc.retrieveTableprobabilitythresholds()
        numberProbabilityThresholds = len(result_probabilityThresholds)
        # Sorting the result list according to the object name
        result_probabilityThresholds.sort(key=itemgetter(1))

        return render_template('smartVisionConfig.html', numberOfObjects=numberOfObjects, customVisionObjectList=result_CustomVisionObjects, numberProbThresholds=numberProbabilityThresholds, probabilityThresholdsList=result_probabilityThresholds, objectUpdate=updateSuccessful)
    
    elif(request.form['update'] == "updateProbThresholds"):
        selectedItem = request.form['selectedItem']
        new_probThreshold = request.form['probThreshold']

        #Insert the new values into the database and update the corresponding table
        if(dbc.update_probabilityThresholds(selectedItem, new_probThreshold)):
            updateSuccessful = True
        else:
            updateSuccessful = False

        result_CustomVisionObjects = dbc.retrieveTablecustomvisionobjectscore()
        numberOfObjects = len(dbc.retrieveTableprobabilitythresholds())
        # Sorting the result list according to the object name
        result_CustomVisionObjects.sort(key=itemgetter(1))
        
        result_probabilityThresholds = dbc.retrieveTableprobabilitythresholds()
        numberProbabilityThresholds = len(result_probabilityThresholds)
        # Sorting the result list according to the object name
        result_probabilityThresholds.sort(key=itemgetter(1))

        return render_template('smartVisionConfig.html', numberOfObjects=numberOfObjects, customVisionObjectList=result_CustomVisionObjects, numberProbThresholds=numberProbabilityThresholds, probabilityThresholdsList=result_probabilityThresholds, probThresholdUpdate=updateSuccessful)






"""This sesction of the code contains all functions related to managing existing admins, meaning you can add new ones or delte existing ones:"""
@app.route("/manageDevelopers")
def displayManageDevelopers():
    """
        Description: This function displays the manageDevelopers.html page.
        Input: Nothing
        Output: returns manageDevelopers.html
    """
    if(session.get("logged_in") != True):
        return redirect(url_for('displayLogin'))
    
    result_adminData = dbc.retrieve_AllAdminData()
    number_admins = len(result_adminData)
    
    return render_template('manageDevelopers.html', numberAdmins=number_admins, adminList=result_adminData)



@app.route("/manageDevelopers", methods=['POST'])
def deleteDeveloper():
    """
        Description: This function deletes and Admin, based on the admin_id submitted via the form.
        Input: via http request -> ['identifier']
        Output: returns manageDevelopers.html
    """
    if(session.get("logged_in") != True):
        return redirect(url_for('displayLogin'))
    
    admin_id = request.form['identifier']

    if(dbc.delete_admin(admin_id)):
        successfulDeletion = "success"
    else:
        successfulDeletion = "fail"


    result_adminData = dbc.retrieve_AllAdminData()
    number_admins = len(result_adminData)
    
    return render_template('manageDevelopers.html', numberAdmins=number_admins, adminList=result_adminData, successfulDeletion = successfulDeletion)



@app.route("/addDevelopers")
def displayAddDeveloper():
    """
        Description: This function displays the addDeveloper.html page.
        Input: Nothing
        Output: returns addDeveloper.html
    """
    if(session.get("logged_in") != True):
        return redirect(url_for('displayLogin'))
    
    return render_template('addDeveloper.html')



@app.route("/addDevelopers", methods=['POST'])
def addDevelopers():
    """
        Description: This function inserts an Admin into the SmartVision database, based on the details provided in the form
        Input: via http request -> ['fname'], ['lname'], ['email'], ['institution'], ['department'], ['password'], ['retypePassword']
        Output: returns manageDevelopers.html if successully added, otherwise returns addDeveloper.html
    """
    if(session.get("logged_in") != True):
        return redirect(url_for('displayLogin'))
    
    error_firstName = ""
    error_lastName = ""
    error_email = ""
    error_institution = ""
    error_department = ""
    error_password = ""
    insertionSuccessful = ""


    firstName = request.form['fname']
    lastName = request.form['lname']
    email = request.form['email']
    institution = request.form['institution']
    department = request.form['department']
    password = request.form['password']
    retypedPassword = request.form['retypePassword']


    #Performing checks that all submitted data is valid:
    if(firstName ==""):
        error_firstName = "error_required"

    if(lastName ==""):
        error_lastName = "error_required"

    if(email ==""):
        error_email = "error_required"
    elif(dbc.checkForAdminEmail(email) != None):
        error_email = "error_exist"
        
    if(institution ==""):
        error_institution = "error_required"
    
    if(department ==""):
        error_department = "error_required"
    
    if(password == ""):
        error_password = "error_required"
    elif(len(password) < 5):
        error_password = "error_tooShort"
    elif(password != retypedPassword):
        error_password = "error_noMatch"
    
    if((error_password == "") and (error_firstName == "") and (error_lastName == "") and (error_email == "") and (error_institution == "") and (error_department == "")):
        hashed_password = generate_password_hash(password)
        # Function inserts data of admin in database
        if(dbc.insert_adminDetails(firstName, lastName, email, institution, department, hashed_password)):
            insertionSuccessful = 'success'
            return redirect(url_for('displayManageDevelopers', insertionSuccessful=insertionSuccessful))
        else:
            # Database error, inserting new admin was not possible
            insertionSuccessful = 'DBerror'
        return render_template('addDeveloper.html', firstName=firstName, lastName=lastName, email=email, institution=institution, department=department, insertionSuccessful=insertionSuccessful)
    else:
        insertionSuccessful = "inputError"
        return render_template('addDeveloper.html', firstName=firstName, error_firstName=error_firstName, lastName=lastName, error_lastName=error_lastName, email=email, error_email=error_email, institution=institution, error_institution=error_institution, department=department, error_department=error_department, error_password=error_password, insertionSuccessful=insertionSuccessful)






"""This sesction of the code contains all functions related to changing the account details of an admin:"""
@app.route("/changePassword")
def displayChangePassword():
    """
        Description: This function displays the changePassword.html page.
        Input: Nothing
        Output: returns changePassword.html
    """
    if(session.get("logged_in") != True):
        return redirect(url_for('displayLogin'))

    return render_template('changePassword.html')



@app.route("/changePassword", methods=['POST'])
def changePassword():
    """
        Description: This function updates the password of an Admin in the SmartVision database, given the from input.
        Input: via http request -> ['password'], ['newPassword']
        Output: returns changePassword.html
    """
    if(session.get("logged_in") != True):
        return redirect(url_for('displayLogin'))
    
    admin_id = session['user_id']
    oldPassword = request.form['password']
    newPassword = request.form['newPassword']

    # fetch specific adminData has the format (admin_id, email, password, first_name, last_name, institution, department)
    adminData = dbc.retrieveSingleAdminData(admin_id)

    validPassword = check_password_hash(adminData[2], oldPassword)

    if(validPassword):
        newHashedPassword = generate_password_hash(newPassword)
        dbValidExecution = dbc.update_adminPassword(newHashedPassword, admin_id)

        if(dbValidExecution == False):
            return render_template('changePassword.html', changePassword='DBerror')
        else:
            return render_template('changePassword.html', changePassword='correct')

    elif(not(validPassword)):
        return render_template('changePassword.html', changePassword='wrongPassword')
    else:
        return render_template('changePassword.html')



@app.route("/changeProfile")
def displayChangeProfile():
    """
        Description: This function displays the changeProfile.html page.
        Input: Nothing
        Output: returns changeProfile.html
    """
    if(session.get("logged_in") != True):
        return redirect(url_for('displayLogin'))
    
    admin_id = session['user_id']
    # fetch specific adminData has the format (admin_id, email, password, first_name, last_name, institution, department)
    adminData = dbc.retrieveSingleAdminData(admin_id)

    return render_template('changeProfile.html', firstName=adminData[3], lastName=adminData[4], email=adminData[1], institution=adminData[5], department=adminData[6])



@app.route("/changeProfile", methods=['POST'])
def changeProfile():
    """
        Description: This function updates the account details of an Admin in the SmartVision database, given the from input.
        Input: via http request -> ['fname'], ['lname'], ['email'], ['institution'], ['department']
        Output: returns changeProfile.html
    """
    if(session.get("logged_in") != True):
        return redirect(url_for('displayLogin'))
    
    error_firstName = ""
    error_lastName = ""
    error_email = ""
    error_institution = ""
    error_department = ""
    updateSuccessful = ""

    admin_id = session['user_id']
    # fetch specific adminData has the format (admin_id, email, password, first_name, last_name, institution, department)
    adminData = dbc.retrieveSingleAdminData(admin_id)

    new_firstName = request.form['fname']
    new_lastName = request.form['lname']
    new_email = request.form['email']
    new_institution = request.form['institution']
    new_department = request.form['department']

    #Performing checks that all submitted data is valid:
    if(new_firstName ==""):
        error_firstName = "error_required"
    
    if(new_lastName ==""):
        error_lastName = "error_required"
    
    if(new_email ==""):
        error_email = "error_required"
    elif((dbc.checkForAdminEmail(new_email) != None) and (new_email != adminData[1])):
        error_email = "error_exist"
        
    if(new_institution ==""):
        error_institution = "error_required"
    
    if(new_department ==""):
        error_department = "error_required"
    
    if((error_firstName == "") and (error_lastName == "") and (error_email == "") and (error_institution == "") and (error_department == "")):
        # Function updates data of admin in database
        if(dbc.update_adminDetails(admin_id, new_firstName, new_lastName, new_email, new_institution, new_department)):
            # fetch specific adminData has the format (admin_id, email, password, first_name, last_name, institution, department)
            adminData = dbc.retrieveSingleAdminData(admin_id)
            updateSuccessful = 'success'
        else:
            # fetch specific adminData has the format (admin_id, email, password, first_name, last_name, institution, department)
            adminData = dbc.retrieveSingleAdminData(admin_id)
            updateSuccessful = 'DBerror'
        return render_template('changeProfile.html', firstName=adminData[3], lastName=adminData[4], email=adminData[1], institution=adminData[5], department=adminData[6], updateSuccessful=updateSuccessful)
    else:
        updateSuccessful = "inputError"
        return render_template('changeProfile.html', firstName=new_firstName, error_firstName=error_firstName, lastName=new_lastName, error_lastName=error_lastName, email=new_email, error_email=error_email, institution=new_institution, error_institution=error_institution, department=new_department, error_department=error_department, updateSuccessful=updateSuccessful)
    





"""This sesction of the code contains all functions related to the authentication, login and logout of a user:"""

@app.route("/login")
def displayLogin():
    """
        Description: This function displays the login.html page.
        Input: Nothing
        Output: returns login.html
    """
    return render_template('login.html')


@app.route("/login", methods=['POST'])
def login():
    """
        Description: This function logs in the user, meaning that the password and username are checked with the entries in the database. Also, the session variables are initiated.
        Input: via http request -> ['username'], ['password']
        Output: returns index.html if successful, otherwise to login.html
    """
    
    loginData_username = request.form['username']
    loginData_password = request.form['password']
    
    #adminData has the format (admin_id, email, password, first_name)
    adminData = dbc.retrieve_Admin(loginData_username)

    if(adminData != None):
        if(adminData[1] == loginData_username):
            validPassword = check_password_hash(adminData[2], loginData_password)
            if(validPassword):
                # clear any old session and create a new session
                session.clear()
                session["logged_in"] = True
                session["user_id"] = adminData[0]
                session["user_name"] = adminData[3]
                return redirect(url_for('displayHome'))
            else:
                return render_template('login.html', password = 'incorrect')
    else:
        return render_template('login.html', username= 'incorrect')
            
    # If no user accounts exist yet, the following will be returned
    return render_template('login.html', nousers = 'correct')



@app.route("/logout")
def logout():
    """
        Description: This function logs the user/admin out of the web application and destroys the session variables. Also, it would make sure that the global variable "algorithm_running" is
        set to "", such that the SmartVision algorithtm "analyseWorksation()" in SmartVision_Detection_Algorithm (main_programme_logic.py) is stopped.
        Input: Nothing
        Output: returns login.html
    """
    """
    Set global variable in main_programme_logic.py, which controls the SmartVision Algorithm to "" to stop the algorithm.
    This ensures in any case, that the SmartVision Algorithm does not keep on running on a thread in the background.
    """
    set_variable_global_running("")

    #check if the global variable thread_smartVisionAlgo has been set to a Thread object, or if it is still an empty string
    if(thread_smartVisionAlgo == ""):
        """
        Nothing has to be done in this case.
        This case simply serves to ensure that the server.py file does not run into an error if the global variable thread_smartvision
        has not been initiated as a Thread object
        """
        pass
        """
        If the global variable thread_smartVisionAlgo is still an active Thread, it must be ensured that the main thread and the smartVisionAlgo
        thread are being joined. This prevents that the smartVisionAlgo thread continues to run in the background if the user logs out.
        """
    elif(thread_smartVisionAlgo.is_alive() == True):
        thread_smartVisionAlgo.join()
    
    session.clear()
    flash('You were logged out.')
    return redirect(url_for('displayLogin'))





if __name__ == "__main__":
    app.run()