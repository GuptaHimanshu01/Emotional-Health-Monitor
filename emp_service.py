import string

import nltk
import static as static
from flask import jsonify
# nltk.data.path.append("C:/Users/swarnava_sinha/AppData/Roaming/nltk_data")
from nrclex import NRCLex



class EmployeeEmotions:
    goa_sadIndex, pune_sadIndex, indore_sadIndex, hyderabad_sadIndex, banglore_sadIndex, nagpur_sadIndex = 0, 0, 0, 0, 0, 0
    goa_employeeCount, pune_employeeCount, indore_employeeCount, hyderabad_employeeCount, banglore_employeeCount, nagpur_employeeCount = 0, 0, 0, 0, 0, 0
    happy, neutral, sadness, stressed, angry, total_count = 0, 0, 0, 0, 0, 0

    # self.goa_sadIndex, self.pune_sadIndex, self.indore_sadIndex, self.hyderabad_sadIndex = 0, 0, 0, 0
    # self.banglore_sadIndex, self.nagpur_sadIndex = 0, 0
    def getEmotionOfAllEmployeesUtil(employees):

        for employee in employees:
            # access the Employee id of each Employees
            EMP_ID = employee.EMP_ID
            # print(f"emp_id: {EMP_ID}")
            # getting path for each employee data
            file_path = "./Emp_Files/emp_" + str(EMP_ID) + ".txt"
            # reading text file
            # print(file_path)
            try:
                Location = employee.LOCATION.strip().casefold()
                # print(Location)
                text_data = open(file_path, encoding="utf-8").read()
                # creating emotion object using nrclex fun
                emotion = NRCLex(text_data)
                # emotion_percentage =  int(emotion. top_emotions) *100
                top_emotion = emotion.top_emotions
                # print(top_emotion)
                # convert tuple into list
                emotion_tuple = top_emotion[0]
                # print(f" {EMP_ID} hello {emotion_tuple[0]} ")

                # counting employees according to location
                # Counting sadness according to location
                if (Location == 'indore' and (emotion_tuple[0] == 'sadness' or emotion_tuple[0] == 'negative' )):
                    EmployeeEmotions.indore_sadIndex += 1
                elif (Location == 'pune' and (emotion_tuple[0] == 'sadness' or emotion_tuple[0] == 'negative' )):
                    EmployeeEmotions.pune_sadIndex += 1
                elif (Location == 'goa' and (emotion_tuple[0] == 'sadness' or emotion_tuple[0] == 'negative' )):
                    EmployeeEmotions.goa_sadIndex += 1
                elif (Location == 'nagpur' and (emotion_tuple[0] == 'sadness' or emotion_tuple[0] == 'negative') ):
                    EmployeeEmotions.nagpur_sadIndex += 1
                elif (Location == 'hyderabad' and (emotion_tuple[0] == 'sadness' or emotion_tuple[0] == 'negative' )):
                    EmployeeEmotions.hyderabad_sadIndex += 1
                elif (Location == 'banglore' and (emotion_tuple[0] == 'sadness' or emotion_tuple[0] == 'negative') ):
                    EmployeeEmotions.banglore_sadIndex += 1

                if Location == 'indore':
                    EmployeeEmotions.indore_employeeCount += 1
                if (Location == 'pune'):
                    EmployeeEmotions.pune_employeeCount += 1
                elif (Location == 'goa'):
                    EmployeeEmotions.goa_employeeCount += 1
                elif (Location == 'nagpur'):
                    EmployeeEmotions.nagpur_employeeCount += 1
                elif (Location == 'hyderabad'):
                    EmployeeEmotions.hyderabad_employeeCount += 1
                elif (Location == 'banglore'):
                    EmployeeEmotions.banglore_employeeCount += 1

                # Counting Emotions of all employees
                if (emotion_tuple[0] == 'joy' or emotion_tuple[0] == 'surprise' or emotion_tuple[0] == 'positive'):
                    EmployeeEmotions.happy += 1
                elif ( emotion_tuple[0] == 'trust'):
                    EmployeeEmotions.neutral += 1
                elif (emotion_tuple[0] == 'sadness' or emotion_tuple[0] == 'negative'  ):
                    EmployeeEmotions.sadness += 1
                elif (emotion_tuple[0] == 'disgust' or emotion_tuple[0] == 'fear' or emotion_tuple[0] =='anticipation' ):
                    EmployeeEmotions.stressed += 1
                elif (emotion_tuple[0] == 'anger'):
                    EmployeeEmotions.angry += 1
                EmployeeEmotions.total_count += 1
                # print("all emotions...in the file...."+EmployeeEmotions.angry+" .. "+EmployeeEmotions.happy+" "+EmployeeEmotions.sadness+" "+EmployeeEmotions.stressed+" "+EmployeeEmotions.neutral)
            except Exception as ex:
                continue





# # emotion = NRCLex(text)

# return emotion.top_emotions[0][0]+": "+str(round(emotion.top_emotions[0][1],2))
#
    @staticmethod
    def getEmotionIndexOfAllEmployeesForPiechart(employees):
        # this method calls only at once and perform db related operation
        EmployeeEmotions.getEmotionOfAllEmployeesUtil(employees)
        print(EmployeeEmotions.total_count)
        happy = (EmployeeEmotions.happy / EmployeeEmotions.total_count) * 100
        neutral = (EmployeeEmotions.neutral / EmployeeEmotions.total_count) * 100
        sadness = (EmployeeEmotions.sadness / EmployeeEmotions.total_count) * 100
        stressed = (EmployeeEmotions.stressed / EmployeeEmotions.total_count) * 100
        angry = (EmployeeEmotions.angry / EmployeeEmotions.total_count) * 100

        return jsonify(
            [{
                'happy': happy,
                'neutral': neutral,
                'sadness': sadness,
                'stressed': stressed,
                'angry': angry,
            }])

    @staticmethod
    def getEmotionIndexOfAllEmployeesForBargraph(employees):
        # EmployeeEmotions.getEmotionOfAllEmployeesUtil(employees)
        pune_sad,goa_sad,nagpur_sad, hyderabad_sad, indore_sad, bangalore_sad = 0,0,0,0,0,0
        if(EmployeeEmotions.pune_sadIndex>0):
            pune_sad = (EmployeeEmotions.pune_sadIndex / EmployeeEmotions.pune_employeeCount)* 100
        if(EmployeeEmotions.nagpur_sadIndex>0):
            nagpur_sad = EmployeeEmotions.nagpur_sadIndex * 100 / EmployeeEmotions.nagpur_employeeCount
        if(EmployeeEmotions.goa_sadIndex>0):
            goa_sad = EmployeeEmotions.goa_sadIndex * 100 / EmployeeEmotions.goa_employeeCount
        if(EmployeeEmotions.indore_sadIndex>0):
            indore_sad = EmployeeEmotions.indore_sadIndex * 100 / EmployeeEmotions.indore_employeeCount
        if(EmployeeEmotions.hyderabad_sadIndex>0):
            hyderabad_sad = EmployeeEmotions.hyderabad_sadIndex * 100 / EmployeeEmotions.hyderabad_employeeCount
        if(EmployeeEmotions.banglore_sadIndex>0):
            bangalore_sad = EmployeeEmotions.banglore_sadIndex * 100 / EmployeeEmotions.banglore_employeeCount

        return jsonify(
            [{
                'pune': pune_sad,
                'nagpur': nagpur_sad,
                'goa': goa_sad,
                'indore': indore_sad,
                'hyderabad': hyderabad_sad,
                'banglore': bangalore_sad,

            }])

    def searchEmployeeEmotionById(self,employee):
        EMP_ID = employee.EMP_ID
        emotion=''
        # getting path for each employee data
        file_path = "./Emp_Files/emp_" + str(EMP_ID) + ".txt"
        text_data = open(file_path, encoding="utf-8").read()
        # creating emotion object using nrclex fun
        emotion = NRCLex(text_data)
        # emotion_percentage =  int(emotion.top_emotions) *100
        top_emotion = emotion.top_emotions
        # convert tuple into list
        emotion_tuple = top_emotion[0]
        if (emotion_tuple[0] == 'joy' or emotion_tuple[0] == 'surprise' or emotion_tuple[0] == 'positive'):
            emotion = 'happy'
        elif (emotion_tuple[0] == 'trust'):
            emotion = 'neutral'
        elif (emotion_tuple[0] == 'sadness' or emotion_tuple[0] == 'negative'):
            emotion = 'sadness'
        elif (emotion_tuple[0] == 'disgust' or emotion_tuple[0] == 'fear' or emotion_tuple[0] == 'anticipation'):
            emotion = 'stressed'
        elif (emotion_tuple[0] == 'anger' ):
            emotion = 'angry'
        return jsonify(
            {
                'emotion':emotion
            }
        )

    def searchEmployeeEmotionByIds(self, employee):
        EMP_ID = employee.EMP_ID
        emotion = ''
        # getting path for each employee data
        file_path = "./Emp_Files/emp_" + str(EMP_ID) + ".txt"
        text_data = open(file_path, encoding="utf-8").read()
        # creating emotion object using nrclex fun
        emotion = NRCLex(text_data)
        # emotion_percentage =  int(emotion.top_emotions) *100
        top_emotion = emotion.top_emotions
        # convert tuple into list
        emotion_tuple = top_emotion[0]
        if (emotion_tuple[0] == 'joy' or emotion_tuple[0] == 'surprise' or emotion_tuple[0] == 'positive'):
            emotion = 'happy'
        elif (emotion_tuple[0] == 'trust'):
            emotion = 'neutral'
        elif (emotion_tuple[0] == 'sadness' or emotion_tuple[0] == 'negative'):
            emotion = 'sadness'
        elif (emotion_tuple[0] == 'disgust' or emotion_tuple[0] == 'fear' or emotion_tuple[0] == 'anticipation'):
            emotion = 'stressed'
        elif (emotion_tuple[0] == 'anger'):
            emotion = 'angry'
        return emotion




    def searchEmployeeEmotionAccuracyById(self,employee):
        happy,neutral,sadness,stressed,angry=0,0,0,0,0
        EMP_ID = employee.EMP_ID
        # getting path for each employee data
        file_path = "./Emp_Files/emp_" + str(EMP_ID) + ".txt"
        text_data = open(file_path, encoding="utf-8").read()
        # creating emotion object using nrclex fun
        emotion = NRCLex(text_data)
        # emotion_percentage =  int(emotion.top_emotions) *100
        top_emotion = emotion.top_emotions
        # convert tuple into list
        emotion_tuple = top_emotion[0]
        emotion_scores = emotion.raw_emotion_scores
        print(type(emotion_scores))
        print(emotion_scores)
        if emotion_scores.__contains__('anticipation'):
            stressed += emotion_scores['anticipation']
        if emotion_scores.__contains__('joy'):
            happy += emotion_scores['joy']
        if emotion_scores.__contains__('positive'):
            happy += emotion_scores['positive']
        if emotion_scores.__contains__('surprise'):
            happy += emotion_scores['surprise']
        if emotion_scores.__contains__('trust'):
            neutral += emotion_scores['trust']
        if emotion_scores.__contains__('anger'):
            angry += emotion_scores['anger']
        if emotion_scores.__contains__('negative'):
            sadness += emotion_scores['negative']
        if emotion_scores.__contains__('fear'):
            stressed += emotion_scores['fear']
        if emotion_scores.__contains__('sadness'):
            sadness += emotion_scores['sadness']
        if emotion_scores.__contains__('disgust'):
            stressed += emotion_scores['disgust']

        return jsonify(
            {
                'happy': happy/10,
                'neutral': neutral/10,
                'sadness': sadness/10,
                'stressed': stressed/10,
                'angry': angry/10,
                'emp_id': EMP_ID,
                'emp_name': employee.EMP_NAME,
                'emp_bu': employee.BU,
            }
        )

    def getAllEmployeeByEmotions(self, employees, emp_emotion):
        employee_list = []
        for employee in employees:
            # access the Employee id of each Employees
            EMP_ID = employee.EMP_ID

            # getting path for each employee data
            file_path = "./Emp_Files/emp_" + str(EMP_ID) + ".txt"

            text_data = open(file_path, encoding="utf-8").read()
            # creating emotion object using nrclex fun
            emotion = NRCLex(text_data)
            # emotion_percentage =  int(emotion.top_emotions) *100
            top_emotion = emotion.top_emotions
            # convert tuple into list
            emotion_tuple = top_emotion[0]
            # print(str(emotion_tuple[0])+" hii "+emotion
            if(emp_emotion=='happy' and (emotion_tuple[0] == 'joy' or emotion_tuple[0] == 'surprise' or emotion_tuple[0] == 'positive')):
                employee_list.append(employee)
            elif (emp_emotion=='neutral' and (emotion_tuple[0] == 'trust')):
                employee_list.append(employee)
            elif (emp_emotion=='sadness' and (emotion_tuple[0] == 'sadness'  or emotion_tuple[0] == 'negative')):
                employee_list.append(employee)
            elif (emp_emotion=='stressed' and (emotion_tuple[0] == 'disgust' or emotion_tuple[0] == 'fear' or emotion_tuple[0] == 'anticipation')):
                employee_list.append(employee)
            elif (emp_emotion=='angry' and (emotion_tuple[0] == 'anger')):
                employee_list.append(employee)
        return employee_list

