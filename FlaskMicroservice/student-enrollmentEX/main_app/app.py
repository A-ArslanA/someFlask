from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

locations = ['City A', 'City B', 'City C', 'City D']

@app.route('/')
def index():
    return render_template('index.html', locations=locations, reservation_result=None)

@app.route('/make_reservation', methods=['POST'])
def make_full_reservation():
    data = {
        'location': request.form['location'],
        'user_info': request.form['user_info'],
        'seats': int(request.form['seats']),
        'time': request.form['time']
    }

    restaurants = get_restaurants(data['location'])
    if not restaurants:
        flash('No available restaurants for the selected location. Please choose another location.', 'error')
        return redirect(url_for('index'))

    chosen_restaurant = choose_restaurant(restaurants)
    reservation_status = make_reservation(chosen_restaurant['id'], data['user_info'], data['seats'], data['time'])

    if reservation_status == 'Success':
        flash(f'Reservation successful at {chosen_restaurant["name"]} in {chosen_restaurant["location"]}!', 'success')
    else:
        flash(f'Reservation failed: {reservation_status}', 'error')

    return redirect(url_for('index'))

def get_restaurants(location):
    service1_url = 'http://localhost:5000/discover'
    response = requests.get(service1_url, params={'location': location})
    return response.json()

def choose_restaurant(restaurants):
    return restaurants[0]

def make_reservation(restaurant_id, user_info, seats, time):
    service3_url = 'http://localhost:5002/reserve'
    reservation_data = {
        'restaurant_id': restaurant_id,
        'user_info': user_info,
        'seats': seats,
        'time': time
    }
    response = requests.post(service3_url, json=reservation_data)
    return response.json()['status']

if __name__ == '__main__':
    app.run(debug=True, port=5003)