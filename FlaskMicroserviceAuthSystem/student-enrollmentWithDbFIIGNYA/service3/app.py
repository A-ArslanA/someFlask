from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('dbURI')
db = SQLAlchemy(app)


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(255), nullable=False)
    course = db.Column(db.String(255), nullable=False)


with app.app_context():
    db.create_all()

@app.route('/enroll', methods=['POST'])
def enroll_student():
    data = request.get_json()
    student_name = data.get("name")
    course = data.get("course")
    
    enrollment = Enrollment(student_name=student_name, course=course)
    db.session.add(enrollment)
    db.session.commit()

    return jsonify({"message": f"{student_name} enrolled in {course}"})

if __name__ == '__main__':
    app.run(port=5002)