# Module Description: This module is responsible for generating all the relevant graphics for the SmartVision Interface.
# Those can be found on the statistics page of the SmartVision interface.
import os
import sys
from datetime import date, datetime
from math import pi
import matplotlib.pyplot as plt
import numpy as np

# To run the script locally from VSCode, uncomment the import statement(s) below:
#import directory_manipulation as dm

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
os.chdir(currentDir) # return to initial working directory to prevent issue reading files
#print("CWD:" + os.getcwd()) # to check whether the default working environment is restored



def plot_pie_occupation(timePeriod):
    """
        Description: The function plots a pie chart of the number of recordings, when the space is occupied or available. It takes the inputs "daily", "pastWeek", and "currentYear" to provide the corresponding
        analysis based on the timePeriod, which was provided.
        Source: Method was constructed with the help of the documentation example found at https://matplotlib.org/3.1.1/gallery/pie_and_polar_charts/pie_features.html#sphx-glr-gallery-pie-and-polar-charts-pie-features-py
        Input: (timePeriod -> string)
        Output: If soemthing is recorded in database: return plt object, otherwise it returns flase if nothing is in the database. Also, it saves an image of the analysis to the "static" folder.
    """
    count_available = 0
    count_occupied = 0
    if(timePeriod == "daily"):
        results_occupation = dbc.retrieve_dailyOccupationCount()
        imageName = "pie_daily_occupation.png"
    elif(timePeriod == "pastWeek"):
        results_occupation = dbc.retrieve_lastWeeks_OccupationCount()
        imageName = "pie_lastWeek_occupation.png"
    elif(timePeriod == "currentYear"):
        results_occupation = dbc.retrieve_currentYear_OccupationCount()
        imageName = "pie_currentYear_occupation.png"
    else:
        return False

    #print(results_occupation)
    if(len(results_occupation)>0):
        for row_dict in results_occupation:
            if(row_dict['occupied'] == 0):
                count_available = row_dict['count_occupied']
            elif(row_dict['occupied'] == 1):
                count_occupied = row_dict['count_occupied']

        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = 'Occupied', 'Available'
        sizes = [count_occupied, count_available]
        explode = (0.1, 0)

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        #plt.savefig(dm.createTargetDirectory("SmartVision_Flask/static")+imageName) # if run from Visual Studio
        plt.savefig("static\\"+imageName)
        #plt.show() # For testing
        plt.close('all')
        return plt
    else:
        return False

        


def plot_pie_months_occupation(month):
    """
        Description: The function plots a pie chart of the number of recordings, when the space is occupied or available. It takes any given month as an integer as input.
        Source: Method was constructed with the help of the documentation example found at https://matplotlib.org/3.1.1/gallery/pie_and_polar_charts/pie_features.html#sphx-glr-gallery-pie-and-polar-charts-pie-features-py
        Input: (month -> integer between 1 and 12)
        Output: If soemthing is recorded in database: return plt object, otherwise it returns flase if nothing is in the database. Also, it saves an image of the analysis to the "static" folder.
    """
    count_available = 0
    count_occupied = 0
    imageName = "pie_month_occupation.png"

    # if the value of month is zero, then the values of the last month should be retrieved.
    if(month == 0):
        current_date = datetime.now()
        current_month = current_date.month
        month = current_month -1

    print("Selected Occupation Month:", month)

    results_occupation = dbc.retrieve_months_OccupationCount(month)
    #print("Occupation results:", results_occupation)

    if(len(results_occupation)>0):
        for row_dict in results_occupation:
            if(row_dict['occupied'] == 0):
                count_available = row_dict['count_occupied']
            elif(row_dict['occupied'] == 1):
                count_occupied = row_dict['count_occupied']

        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = 'Occupied', 'Available'
        sizes = [count_occupied, count_available]
        explode = (0.1, 0)  # only "explode" the 2nd slice

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        #plt.savefig(dm.createTargetDirectory("SmartVision_Flask/static")+imageName) # if run from Visual Studio
        plt.savefig("static\\"+imageName)
        #plt.show() # For testing
        plt.close('all')

        return plt
    else:
        return False




def relativization(input_number, total_sum, base):
    """
        Description: This function relativizes a given number based on the total sum of collected data and a base.
        Input: (input_number -> int), (total_sum -> int), (base -> int)
        Output: result -> float
    """
    if(total_sum != 0):
        result = (input_number/total_sum)*base
    else:
        result = 0
    return result



def plot_radar_chart(data, categories):
    """
        Description: The function has been adopted from a blog post on medium. It takes in data and data labes to then generate a radar diagram.
        Source: This function has been adopted from https://medium.com/python-in-plain-english/radar-chart-basics-with-pythons-matplotlib-ba9e002ddbcd
        Input: (data -> list of int or floats), (data -> list)
        Output: returns mathplotlib object "plt"
    """
    fig = plt.figure(figsize=(8,6))

    ax = plt.subplot(polar="True")

    categories = categories
    N = len(categories)

    values = data
    values += values[:1]

    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    plt.polar(angles, values, "g", marker='.')
    plt.fill(angles, values, "g", alpha=0.3)

    plt.xticks(angles[:-1], categories, y=-0.08)

    ax.set_rlabel_position(14)
    plt.yticks([1, 2, 3, 4, 5, 6, 7, 8, 9], color="grey")
    plt.ylim(0,10)

    #plt.show() # For testing

    return plt



def plot_radar_emotions(timePeriod):
    """
        Description: The function plots a radar chart of the number of recordings of detected emotions. It takes the inputs "daily", "pastWeek", and "currentYear" to provide the corresponding
        analysis based on the timePeriod, which was provided.
        Input: (timePeriod -> string)
        Output: If soemthing is recorded in database: return plt object, otherwise it returns flase if nothing is in the database. Also, it saves an image of the analysis to the "static" folder.
    """
    count_anger = 0
    count_contempt = 0
    count_disgust = 0
    count_fear = 0
    count_happiness = 0
    count_neutral = 0
    count_sadness = 0
    count_surprise = 0
    count_noFace = 0
    count_occludedFace = 0
    count_noPerson = 0


    if(timePeriod == "daily"):
        results_emotions = dbc.retrieve_dailyEmotionCount()
        imageName = "radar_daily_emotions.png"
    elif(timePeriod == "pastWeek"):
        results_emotions = dbc.retrieve_lastWeeks_Emotions()
        imageName = "radar_lastWeek_emotions.png"
    elif(timePeriod == "currentYear"):
        results_emotions = dbc.retrieve_currentYear_Emotions()
        imageName = "radar_currentYear_emotions.png"
    else:
        return False
    
    if(len(results_emotions)>0):

        for result_row in results_emotions:
            if(result_row["dominant_emotion"] == 'anger'):
                count_anger = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'contempt'):
                count_contempt = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'disgust'):
                count_disgust = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'fear'):
                count_fear = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'happiness'):
                count_happiness = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'neutral'):
                count_neutral = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'sadness'):
                count_sadness = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'surprise'):
                count_surprise = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'contempt'):
                count_contempt = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'no face'):
                count_noFace = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'face occluded'):
                count_occludedFace = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'no person detected'):
                count_noPerson = result_row["count_emotions"]

        total_count = count_anger + count_contempt + count_disgust + count_fear + count_happiness + count_neutral + count_sadness + count_surprise + count_noFace + count_occludedFace + count_noPerson
        relative_base = 10
        relative_count_anger = relativization(count_anger, total_count, relative_base)
        relative_count_contempt = relativization(count_contempt, total_count, relative_base)
        relative_count_disgust = relativization(count_disgust, total_count, relative_base)
        relative_count_fear = relativization(count_fear, total_count, relative_base)
        relative_count_happiness = relativization(count_happiness, total_count, relative_base)
        relative_count_neutral = relativization(count_neutral, total_count, relative_base)
        relative_count_sadness = relativization(count_sadness, total_count, relative_base)
        relative_count_surprise = relativization(count_surprise, total_count, relative_base)
        relative_count_noFace = relativization(count_noFace, total_count, relative_base)
        relative_count_occludedFace = relativization(count_occludedFace, total_count, relative_base)
        relative_count_noPerson = relativization(count_noPerson, total_count, relative_base)

        categories = ['Happiness', 'Contempt', 'Surprise', 'Neutral', 'Sadness', 'Fear', 'Anger', 'Disgust', 'Face Occluded', 'No Face', 'No Person']
        values = [relative_count_happiness, relative_count_contempt, relative_count_surprise, relative_count_neutral, relative_count_sadness, relative_count_fear, relative_count_anger, relative_count_disgust, relative_count_occludedFace, relative_count_noFace, relative_count_noPerson]
        
        radar_figure = plot_radar_chart(values, categories)
        
        #radar_figure.savefig(dm.createTargetDirectory("SmartVision_Flask/static")+imageName) # if run from Visual Studio
        radar_figure.savefig("static\\"+imageName) # if run from Flask Web Application
        #radar_figure.show() # For testing
        radar_figure.close('all')

        return radar_figure
    else:
        return False



def plot_radar_months_emotions(month):
    """
        Description: The function plots a radar chart of the number of recordings of detected emotions. It takes any given month as an integer as input.
        Input: (month -> integer between 1 and 12)
        Output: If soemthing is recorded in database: return plt object, otherwise it returns flase if nothing is in the database. Also, it saves an image of the analysis to the "static" folder.
    """
    count_anger = 0
    count_contempt = 0
    count_disgust = 0
    count_fear = 0
    count_happiness = 0
    count_neutral = 0
    count_sadness = 0
    count_surprise = 0
    count_noFace = 0
    count_occludedFace = 0
    count_noPerson = 0

    # if the value of month is zero, then the values of the last month should be retrieved.
    if(month == 0):
        current_date = datetime.now()
        current_month = current_date.month
        month = current_month -1

    #print("Selected Emotion Month:", month) # for testing purposes

    results_emotions = dbc.retrieve_months_Emotions(month)
    #print("Database results:", results_emotions) # for testing purposes
    
    if(len(results_emotions)>0):

        for result_row in results_emotions:
            if(result_row["dominant_emotion"] == 'anger'):
                count_anger = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'contempt'):
                count_contempt = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'disgust'):
                count_disgust = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'fear'):
                count_fear = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'happiness'):
                count_happiness = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'neutral'):
                count_neutral = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'sadness'):
                count_sadness = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'surprise'):
                count_surprise = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'contempt'):
                count_contempt = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'no face'):
                count_noFace = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'face occluded'):
                count_occludedFace = result_row["count_emotions"]
            elif(result_row["dominant_emotion"] == 'no person detected'):
                count_noPerson = result_row["count_emotions"]

        total_count = count_anger + count_contempt + count_disgust + count_fear + count_happiness + count_neutral + count_sadness + count_surprise + count_noFace + count_occludedFace + count_noPerson
        relative_base = 10
        relative_count_anger = relativization(count_anger, total_count, relative_base)
        relative_count_contempt = relativization(count_contempt, total_count, relative_base)
        relative_count_disgust = relativization(count_disgust, total_count, relative_base)
        relative_count_fear = relativization(count_fear, total_count, relative_base)
        relative_count_happiness = relativization(count_happiness, total_count, relative_base)
        relative_count_neutral = relativization(count_neutral, total_count, relative_base)
        relative_count_sadness = relativization(count_sadness, total_count, relative_base)
        relative_count_surprise = relativization(count_surprise, total_count, relative_base)
        relative_count_noFace = relativization(count_noFace, total_count, relative_base)
        relative_count_occludedFace = relativization(count_occludedFace, total_count, relative_base)
        relative_count_noPerson = relativization(count_noPerson, total_count, relative_base)


        categories = ['Happiness', 'Contempt', 'Surprise', 'Neutral', 'Sadness', 'Fear', 'Anger', 'Disgust', 'Face Occluded', 'No Face', 'No Person']
        values = [relative_count_happiness, relative_count_contempt, relative_count_surprise, relative_count_neutral, relative_count_sadness, relative_count_fear, relative_count_anger, relative_count_disgust, relative_count_occludedFace, relative_count_noFace, relative_count_noPerson]
        
        radar_figure = plot_radar_chart(values, categories)

        #radar_figure.savefig(dm.createTargetDirectory("SmartVision_Flask/static")+"radar_month_emotions.png") # if run from Visual Studio
        radar_figure.savefig("static\\"+"radar_month_emotions.png") # if run from Flask Web Application
        #radar_figure.show() # For testing purposes
        radar_figure.close('all')

        return radar_figure

    else:
        return False



if(__name__ == "__main__"):

    #figure = plot_pie_occupation("daily")
    #print(figure)
    #plot_pie_months_occupation(8)
    radarFigure = plot_radar_emotions("currentYear")
    pieFigure = plot_pie_occupation("currentYear")
    radarFigureMonth = plot_radar_months_emotions(0)
    pieFigureMonth = plot_pie_months_occupation(0)
    #figure.show()
    #figure = plot_radar_months_emotions(8)
    #figure.savefig("static\\"+"radar_lastWeek_emotions.png")
    #figure.show()
    #print(dbc.retrieve_dailyOccupationCount())
    #plot_radar_months_emotions(8)
    #liste = []
    #print("lenght:", len(liste))
    
    