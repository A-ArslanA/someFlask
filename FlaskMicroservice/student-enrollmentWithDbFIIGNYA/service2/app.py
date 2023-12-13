# Student Information Service

from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('dbURI')
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    course = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/students')
def get_students():
    students = Student.query.all()
    student_info = [{"name": student.name, "course": student.course} for student in students]
    return jsonify({"students": student_info})

if __name__ == '__main__':
    app.run(port=5001)