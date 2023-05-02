from flask import Flask, request, jsonify, make_response
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import sessionmaker
from emp_service import EmployeeEmotions
from flask_cors import CORS
# H imports
import json,requests
import os
from flaskext.mysql import MySQL
import pymysql
from flask import flash
from flask import Flask, url_for, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash


# DEFINE THE DATABASE CREDENTIALS
user = 'root'
password = 'root'
host = 'localhost'
port = 3306
database = 'health_monitor'




# PYTHON FUNCTION TO CONNECT TO THE MYSQL DATABASE AND
# RETURN THE SQLACHEMY ENGINE OBJECT
def get_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        ), echo=True
    )


# Init app
app = Flask(__name__)
app.config['SECRET_KEY']= os.urandom(24)
CORS(app)

# Defining the Engine & Session
engine = get_connection()
Session = sessionmaker(bind=engine)
# changed below line from session to session1
session1 = Session()


# create declarative base
Base = declarative_base()

meta = MetaData()


# Employee class/model
class Employee(Base):
    __tablename__ = 'employee'

    EMP_ID = Column(Integer, primary_key=True)
    EMP_NAME = Column(String(255))
    EMP_EMAIL = Column(String(100))
    BU = Column(String(255))
    DU = Column(String(255))
    MANAGER_NAME = Column(String(255))
    PROJECT_NAME = Column(String(255))
    LOCATION = Column(String(255))
    HAPPINESS_INDEX = Column(DECIMAL(precision=3, scale=2))

    def __init__(self, EMP_ID, EMP_NAME, EMP_EMAIL, BU, DU, MANAGER_NAME, PROJECT_NAME, LOCATION, HAPPINESS_INDEX):
        self.EMP_ID = EMP_ID
        self.EMP_NAME = EMP_NAME
        self.EMP_EMAIL = EMP_EMAIL
        self.BU = BU
        self.DU = DU
        self.MANAGER_NAME = MANAGER_NAME
        self.PROJECT_NAME = PROJECT_NAME
        self.LOCATION = LOCATION
        self.HAPPINESS_INDEX = HAPPINESS_INDEX


meta.create_all(engine)
# again changed session to session1
employees = session1.query(Employee).all()
# Add new employee
@app.route('/employees', methods=['POST'])
def add_employee():
    _json = request.get_json()
    employee = Employee(
        EMP_ID=_json['EMP_ID'],
        EMP_NAME=_json['EMP_NAME'],
        EMP_EMAIL=_json['EMP_EMAIL'],
        BU=_json['BU'],
        DU=_json['DU'],
        MANAGER_NAME=_json['MANAGER_NAME'],
        PROJECT_NAME=_json['PROJECT_NAME'],
        LOCATION=_json['LOCATION'],
        HAPPINESS_INDEX=_json['HAPPINESS_INDEX']
    )
    try:
        session1.add(employee)
        session1.commit()
        EmployeeEmotions.getEmotionLevelsNScore(employee)
        return {'message': 'User created successfully'}, 201
    except Exception as ex:
        session1.rollback()
        return {'message': 'problem inserting data+'}, 201


# list all  employees
@app.route('/employees', methods=['GET'])
def get_employees():

    # employees = session1.query(Employee).all()
    # employees = Employee.query().all()
    if not employees:
        return {'message': 'No employees found!'}, 404
    return jsonify(
        [{
            'EMP_ID': employee.EMP_ID,
            'EMP_NAME': employee.EMP_NAME,
            'EMP_EMAIL': employee.EMP_EMAIL,
            'BU': employee.BU,
            'DU': employee.DU,
            'MANAGER_NAME': employee.MANAGER_NAME,
            'PROJECT_NAME': employee.PROJECT_NAME,
            'LOCATION': employee.LOCATION,
            'HAPPINESS_INDEX': employee.HAPPINESS_INDEX
        } for employee in employees])


# Get Single Employee
@app.route('/employees/<int:emp_id>', methods=['GET'])
def get_employee(emp_id):
    employee = session1.query(Employee).filter_by(EMP_ID=emp_id).first()
    if not employee:
        return {'message': 'invalid employee id!'}, 404
    return jsonify(
        {
            'EMP_ID': employee.EMP_ID,
            'EMP_NAME': employee.EMP_NAME,
            'EMP_EMAIL': employee.EMP_EMAIL,
            'BU': employee.BU,
            'DU': employee.DU,
            'MANAGER_NAME': employee.MANAGER_NAME,
            'PROJECT_NAME': employee.PROJECT_NAME,
            'LOCATION': employee.LOCATION,
            'HAPPINESS_INDEX': employee.HAPPINESS_INDEX
        })


# Update employee
@app.route('/employees/<int:emp_id>', methods=['PUT'])
def update_employee(emp_id):
    _json = request.get_json()
    # changed session to session1
    updated_employee = session1.query(Employee).filter_by(EMP_ID=emp_id).first()
    updated_employee.EMP_ID = emp_id,
    updated_employee.EMP_NAME = _json['EMP_NAME'],
    updated_employee.EMP_EMAIL = _json['EMP_EMAIL'],
    updated_employee.BU = _json['BU'],
    updated_employee.DU = _json['DU'],
    updated_employee.MANAGER_NAME = _json['MANAGER_NAME'],
    updated_employee.PROJECT_NAME = _json['PROJECT_NAME'],
    updated_employee.LOCATION = _json['LOCATION'],
    updated_employee.HAPPINESS_INDEX = _json['HAPPINESS_INDEX']
    if not updated_employee:
        return {'message': 'User not found'}, 404
    session1.commit()
    # refresh the object to get the updated values from the data bases
    session1.refresh(updated_employee)
    return {'message': 'User updated successfully'}, 200


#update happiness Index
@app.route('/employees/update-happiness-index', methods=['GET'])
def updateHappinessIndex():
    # response = get_employees()
    response = requests.get("http://127.0.0.1:5000/employees")
    json_data = response.json()

    list_of_lists = []

    for item in json_data:
        row = [item['BU'], item['DU'], item['EMP_EMAIL'], item['EMP_ID'], item['EMP_NAME'], item['HAPPINESS_INDEX'],
               item['LOCATION'], item['MANAGER_NAME'], item['PROJECT_NAME']]
        # print(row)
        list_of_lists.append(row)

    print(list_of_lists)
    return list_of_lists


# update happiness index for an employee
@app.route('/employees/update-happiness-index/<int:emp_id>', methods=['PUT'])
def update_employee_happiness_index(emp_id):
    employee = session1.query(Employee).filter(Employee.EMP_ID == emp_id).first()
    if not employee:
        return {'message': 'Employee not found!'}, 404
    employee.HAPPINESS_INDEX += 1  # increase happiness index by 1
    session1.commit()
    return {'message': 'Happiness index updated successfully!'}




# update happiness index for all employees...
@app.route('/employees/update_happiness_index', methods=['PUT'])
def update_happiness_index():
    emotions_map = {
        "happy": 8.00,
        "neutral": 6.00,
        "sadness": 4.00,
        "stressed": 2.00,
        "angry": 0.50
    }

    employees = session1.query(Employee).all()

    if not employees:
        return {'message': 'No employees found!'}, 404
    for emp in employees:
        emotion = EmployeeEmotions().searchEmployeeEmotionByIds(emp)
        happiness_index = emotions_map.get(emotion, None)
        if happiness_index:
            emp.HAPPINESS_INDEX = happiness_index
    try:
        session1.commit()
        return {'message': 'Happiness index updated successfully!'}, 200
    except Exception as ex:
        session1.rollback()
        return {'message': 'Problem updating happiness index!'}, 500








# Delete an Employee
@app.route('/employees/<int:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    # changed session to session1
    employee = session1.query(Employee).filter_by(EMP_ID=emp_id).first()
    if not employee:
        return {'message': 'User not found'}, 404
    session1.delete(employee)
    session1.commit()
    return {'message': 'User deleted successfully'}, 200

# search employee emotion based on id
@app.route('/employees/searchemotion/<int:emp_id>', methods=['GET'])
def searchEmployeeMotion(emp_id):
    # changed session to session1
    employee = session1.query(Employee).filter_by(EMP_ID=emp_id).first()
    print(employee)
    if not employee:
        return {'message': 'invalid employee id!'}, 404
    return  EmployeeEmotions().searchEmployeeEmotionById(employee)

@app.route('/employees/searchemotion/accuracy/<int:emp_id>', methods=['GET'])
def searchEmployeeMotionWithAccuracy(emp_id):
    # changed session to session1
    employee = session1.query(Employee).filter_by(EMP_ID=emp_id).first()
    if not employee:
        return {'message': 'invalid employee id!'}, 404
    return EmployeeEmotions().searchEmployeeEmotionAccuracyById(employee)

# get employees baased on emotions
@app.route('/employees/emotion', methods=['GET'])
def searchEmployeesByEMotion():
    # emotion = request.args.getlist("emotion")
    # print(emotion)
    # emotion = emotion[0]
    # employee_list = EmployeeEmotions().getAllEmployeeByEmotions(employees,emotion)
    # print(employee_list)
    # return jsonify(
    #     [{
    #         'EMP_ID': employee.EMP_ID,
    #         'EMP_NAME': employee.EMP_NAME,
    #         'EMP_EMAIL': employee.EMP_EMAIL,
    #         'BU': employee.BU,
    #         'DU': employee.DU,
    #         'MANAGER_NAME': employee.MANAGER_NAME,
    #         'PROJECT_NAME': employee.PROJECT_NAME,
    #         'LOCATION': employee.LOCATION,
    #         'HAPPINESS_INDEX': employee.HAPPINESS_INDEX
    #     } for employee in employee_list])
    return get_employees()

@app.route('/employees/piechartdetails', methods=['GET'])
def get_pieChartDetails():
    # getting all employees from db
    # employees = session.query(Employee).all()
    # pass all employees record to getEmotionIndexOfAllEmployees
    # my_instance = EmployeeEmotions()
    return EmployeeEmotions.getEmotionIndexOfAllEmployeesForPiechart(employees)


@app.route('/employees/barchartdetails', methods=['GET'])
def get_barChartDetails():
    # pass all employees record to getEmotionIndexOfAllEmployees
    # employees = session.query(Employee).all()
    return EmployeeEmotions.getEmotionIndexOfAllEmployeesForBargraph(employees)

try:
    # GET THE CONNECTION OBJECT (ENGINE) FOR THE DATABASE

    print(
        f"Connection to the {host} for user {user} created successfully.")
except Exception as ex:
    print("Connection could not be made due to the following error: \n", ex)











#
# h code
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'health_monitor'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


def close_database():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.close()
    conn.close()


@app.route('/employeeList')
def listAllEmployees():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()



@app.route('/addEmployee', methods=['POST'])
def add_new_employee():
    try:
        _json = request.json
        emp_id = _json['emp_id']
        emp_name = _json['emp_name']
        emp_email = _json['emp_email']
        bu = _json['bu']
        du = _json['du']
        manager_name = _json['manager_name']
        project = _json['project']
        location = _json['location']
        happiness_index = _json['happiness_index']

        # validate the received values
        if emp_id and emp_name and emp_email and bu and du and manager_name and project and location and happiness_index and request.method == 'POST':
            # save edits
            sql = "INSERT INTO employees(emp_id, emp_name, emp_email, bu ,du , manager_name , project , location , happiness_index) VALUES(%s, %s, %s ,  %s,  %s,  %s,  %s,  %s, %s)"
            data = (emp_id, emp_name, emp_email, bu, du, manager_name, project, location, happiness_index)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Employee added successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()




def get_current_user():
    user = None
    if 'user' in session:
        user = session['user']
        conn = mysql.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", [user])
        except Exception as e:
            print("Error executing query:", e)
            # handle the error here

        # Get the first row of results if available
        user = cursor.fetchone()
    return user



@app.route('/')
def home():
    user = get_current_user()
    return render_template('home.html', user=user)



@app.route('/home')
def index():
    return render_template('index1.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    user = get_current_user()
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password']
        # hashed_password = generate_password_hash(password)

        conn = mysql.connect()
        cursor = conn.cursor()
        # user_cursor = cursor.execute("SELECT * from users where username= %s", [username])

        # sql = "INSERT INTO users(username,password) VALUES(%s, %s)"
        # data = (username,password)
        # conn = mysql.connect()
        # cursor = conn.cursor()
        # user_cursor = cursor.execute(sql, data)
        # user = user_cursor.fetchone()

        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", [username])
        except Exception as e:
            print("Error executing query:", e)
            # handle the error here

        # Get the first row of results if available
        user = cursor.fetchone()
        print(user)

        # username = user[1]
        # hashed_password = user[2]

        if user:
            if check_password_hash(user[2], password1):
                session['user'] = user[1]
                return redirect(url_for('dashboard'))
            else:
                error = "Password did not match"
        else:
            error = "Username/email did not match"
        # conn.commit()
        # resp = jsonify('Employee added successfully!')
        # resp.status_code = 200

    return render_template('login.html', loginerror=error, user=user)


@app.route('/register', methods=['POST', 'GET'])
def register():
    user = get_current_user()
    if request.method == 'POST':

        conn = mysql.connect()
        cursor = conn.cursor()

        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", [username])
        except Exception as e:
            print("Error executing query:", e)
            # handle the error here

        # Get the first row of results if available
        user = cursor.fetchone()

        if user:
            return render_template('register.html', registererror='Username already taken, try different username.')

        sql = "INSERT INTO users(username,password) VALUES(%s, %s)"
        data = (username, hashed_password)
        # conn = mysql.connect()
        # cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        # resp = jsonify('Employee added successfully!')
        # resp.status_code = 200
        return redirect(url_for('index'))

    return render_template('register.html', user=user)


@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    user = get_current_user()
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM employees")
    allemp = cursor.fetchall()
    print(allemp)
    return render_template('dashboard.html', user=user, allemp=allemp)


@app.route('/addnewemployee', methods=['POST', 'GET'])
def addnewemployee():
    user = get_current_user()
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        emp_id = request.form['emp_id']
        emp_name = request.form['emp_name']
        emp_email = request.form['emp_email']
        bu = request.form['bu']
        du = request.form['du']
        manager_name = request.form['manager_name']
        project = request.form['project']
        location = request.form['location']

        happiness_index = "0.00"  # default value for new employees
        sql = "INSERT INTO employees(emp_id, emp_name, emp_email, bu, du, manager_name, project, location, happiness_index) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (emp_id, emp_name, emp_email, bu, du, manager_name, project, location, happiness_index)
        cursor.execute(sql, data)
        conn.commit()
        flash('Employee added successfully!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('All fields are required.', 'error')
    return render_template('addnewemployee.html', user=user)
        # validate the received values
    #     happiness_index = "0.00"
    #     print(emp_id,emp_name,emp_email)
    #     sql = "INSERT INTO employees(emp_id, emp_name, emp_email, bu ,du , manager_name , project , location , happiness_index) VALUES(%s, %s, %s ,  %s,  %s,  %s,  %s,  %s,%s)"
    #     data = (emp_id, emp_name, emp_email, bu, du, manager_name, project, location, happiness_index)
    #     print(data)
    #     cursor.execute(sql, data)
    #     conn.commit()
    #     # resp = jsonify('Employee added successfully!')
    #     # resp.status_code = 200
    #     return redirect(url_for('dashboard'))
    #
    #
    # return render_template('addnewemployee.html', user=user)


@app.route('/singleemployeeprofile/<int:emp_id>')
def singleemployeeprofile(emp_id):
    user = get_current_user()
    conn = mysql.connect()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM employees WHERE emp_id = %s", [emp_id])
    except Exception as e:
        print("Error executing query:", e)
        # handle the error here

    # Get the first row of results if available
    single_emp = cursor.fetchone()
    print(single_emp)
    return render_template('singleemployeeprofile.html', user=user,  single_emp=single_emp)


@app.route('/fetchone/<int:emp_id>')
def fetchone(emp_id):
    user = get_current_user()
    conn = mysql.connect()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM employees WHERE emp_id = %s", [emp_id])
    except Exception as e:
        print("Error executing query:", e)
        # handle the error here

    # Get the first row of results if available
    single_emp = cursor.fetchone()
    print(single_emp)
    return render_template('updateemployee.html', user=user, single_emp=single_emp)

@app.route('/updateemployee',methods=["POST","GET"])
def updateemployee():
    user = get_current_user()
    if request.method == "POST":
        conn = mysql.connect()
        cursor = conn.cursor()
        emp_id = request.form['emp_id']
        emp_name = request.form['emp_name']
        # emp_email = request.form['emp_email']
        bu = request.form['bu']
        manager_name = request.form['manager_name']
        location = request.form['location']
        cursor.execute("UPDATE employees SET emp_name =%s,bu =%s,manager_name =%s,location =%s WHERE emp_id=%s", [emp_name,bu,manager_name,location,emp_id])
        conn.commit()
        return redirect(url_for('dashboard'))

    return render_template('updateemployee.html', user=user)

@app.route('/deleteemployee/<int:emp_id>',methods=["GET","POST"])
def deleteemployee(emp_id):
    user = get_current_user()
    if request.method=="GET":
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE emp_id=%s", [emp_id])
        conn.commit()
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', user=user)


@app.route('/logout')
def logout():
    session.clear()
    close_database()
    return render_template('home.html')


# for front-end and survey form
@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        # Get answers to all the questions from the form
        name = request.form['name']
        q1_answer = request.form['emotion']
        q2_answer = request.form['emotion1']
        q3_answer = request.form['emotion2']
        q4_answer = request.form['emotion3']
        q5_answer = request.form['emotion4']
        q6_answer = request.form['emotion5']
        q7_answer = request.form['emotion6']
        q8_answer = request.form['emotion7']
        q9_answer = request.form['emotion8']
        q10_answer = request.form['emotion9']
        q11_answer = request.form['emotion10']
        q12_answer = request.form['emotion11']
        q13_answer = request.form['emotion12']
        q14_answer = request.form['emotion13']
        q15_answer = request.form['emotion14']
        q16_answer = request.form['emotion15']
        print(q1_answer)
        print(q2_answer)

        # Create a dictionary to store the counts of each emotion
        emotions_count = {'happy': 0, 'neutral': 0, 'sad': 0, 'stressed': 0, 'angry': 0}

        # Count the number of times each emotion was selected
        emotions_count[q1_answer] += 1
        emotions_count[q2_answer] += 1
        emotions_count[q3_answer] += 1
        emotions_count[q4_answer] += 1
        emotions_count[q5_answer] += 1
        emotions_count[q6_answer] += 1
        emotions_count[q7_answer] += 1
        emotions_count[q8_answer] += 1
        emotions_count[q9_answer] += 1
        emotions_count[q10_answer] += 1
        emotions_count[q11_answer] += 1
        emotions_count[q12_answer] += 1
        emotions_count[q13_answer] += 1
        emotions_count[q14_answer] += 1
        emotions_count[q15_answer] += 1
        emotions_count[q16_answer] += 1

        # Get the emotion with the maximum count
        max_emotion = max(emotions_count, key=emotions_count.get)
        if max_emotion=="sad":
            sad="sad";
            return render_template('result.html', sad=sad, name=name)
        if max_emotion == "happy":
            happy = "happy";
            return render_template('result.html', happy=happy, name=name)


        if max_emotion == "neutral":
            neutral = "neutral";
            return render_template('result.html', neutral=neutral, name=name)

        if max_emotion == "stressed":
            stressed = "stressed";
            return render_template('result.html', stressed=stressed, name=name)

        if max_emotion == "angry":
            angry = "angry";
            return render_template('result.html', angry=angry, name=name)

# Pass the maximum emotion to the result template


    # Render the survey template if the request method is GET

    return render_template('survey.html')
















# Run the app
if __name__ == '__main__':
    app.run(debug=True)




