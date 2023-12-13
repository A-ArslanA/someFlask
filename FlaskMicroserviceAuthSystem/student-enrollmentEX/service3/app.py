from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/reserve', methods=['POST'])
def make_reservation():
    data = request.json
    reservation_status = reserve_seats(data['restaurant_id'], data['user_info'], data['seats'], data['time'])
    return jsonify({'status': reservation_status})

def reserve_seats(restaurant_id, user_info, seats, time):
    # Simulate making a reservation using a reservation API
    return 'Success'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)