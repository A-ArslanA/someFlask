# Student Information Service

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/students', methods=['GET'])
def get_students():
    students = [
        {"name": "John Doe", "course": "Math"},
        {"name": "Jane Doe", "course": "Programming"}
        ]
    return jsonify({"students": students})

if __name__ == '__main__':
    app.run(port=5001)