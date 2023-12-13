# Course Management Service

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/courses', methods=['GET'])
def get_courses():
    courses = ['Math', 'Biology', 'Programming']
    return jsonify({'courses': courses})

if __name__ == '__main__':
    app.run(port=5000)
