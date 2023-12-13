from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

restaurants = [
    {'id': 1, 'name': 'Restaurant A', 'location': 'City A'},
    {'id': 2, 'name': 'Restaurant B', 'location': 'City B'},
    # Add more restaurant data
]

@app.route('/discover', methods=['GET'])
def discover_restaurants():
    user_location = request.args.get('location')
    restaurants = get_restaurants(user_location)
    return jsonify(restaurants)

def get_restaurants(location):
    matching_restaurants = [r for r in restaurants if r['location'] == location]
    return matching_restaurants

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)