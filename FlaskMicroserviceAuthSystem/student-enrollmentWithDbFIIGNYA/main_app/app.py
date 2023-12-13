# students enroll system

from flask import Flask, jsonify, render_template, redirect, request
import requests
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('dbURI')
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Communicate with service1 to get available courses
    courses_response = requests.get('http://localhost:5000/courses')
    courses = courses_response.json()["courses"]

    # Communicate with service2 to get information about enrolled students
    students_response = requests.get('http://localhost:5001/students')
    students = students_response.json()["students"]

    return render_template('index.html', courses=courses, students=students)


@app.route('/enroll', methods=['POST'])
def enroll():
    data = {"name": request.form["name"], "course": request.form["course"]}
    enrollment_response = requests.post('http://localhost:5002/enroll', json=data)

    # Перенаправление на главную страницу после зачисления
    return redirect('/')


if __name__ == '__main__':
    app.run(port=5003)
