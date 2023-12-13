from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/enroll', methods=['POST'])
def enroll_student():
    data = request.get_json()
    student_name = data.get("name")
    course = data.get("course")
    # Implement enrollment logic here
    return jsonify({"message": f"{student_name} enrolled in {course}"})

if __name__ == '__main__':
    app.run(port=5002)