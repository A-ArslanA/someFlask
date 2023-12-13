from flask import Flask, jsonify, request

app = Flask(__name__)

restaurants = [
    {'id': 1, 'name': 'Restaurant A', 'location': 'City A'},
    {'id': 2, 'name': 'Restaurant B', 'location': 'City B'},
    # Add more restaurant data
]

@app.route('/metadata', methods=['GET'])
def get_metadata():
    location = request.args.get('location')
    matching_restaurants = [r for r in restaurants if r['location'] == location]
    return jsonify(matching_restaurants)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)