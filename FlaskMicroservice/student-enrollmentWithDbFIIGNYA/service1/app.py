# Course Management Service

from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('dbURI')
db = SQLAlchemy(app)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

with app.app_context():
        db.create_all()

@app.route('/courses', methods=['GET'])
def get_courses():
    courses = ['Math', 'Biology', 'Programming']
    return jsonify({'courses': courses})

if __name__ == '__main__':
    app.run(port=5000)
