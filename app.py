from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import random
from datetime import datetime, timedelta
import hashlib
import os

app = Flask(__name__)
app.secret_key = 'ap-bus-booking-secret-key'

# Domain configuration
DOMAIN = os.environ.get('DOMAIN', 'localhost')
SERVER_NAME = f"{DOMAIN}" if DOMAIN != 'localhost' else None

# Andhra Pradesh cities
CITIES = [
    "Hyderabad", "Visakhapatnam", "Vijayawada", "Guntur", "Nellore", 
    "Kurnool", "Tirupati", "Warangal", "Kakinada", "Anantapur",
    "Eluru", "Rajahmundry", "Nizamabad", "Karimnagar", "Machilipatnam",
    "Ongole", "Chittoor", "Anakapalli", "Srikakulam", "Vizianagaram",
    "Proddatur", "Markapur", "Nandyal", "Adoni", "Madanapalle"
]

# Bus operators
BUS_OPERATORS = [
    "APSRTC", "Orange Travels", "SRS Travels", "VRL Logistics", 
    "Kaveri Travels", "Morning Star Travels", "Diwakar Travels", 
    "Kesineni Travels", "SVR Tours & Travels", "Ramana Travels"
]

# Bus types with pricing
BUS_TYPES = {
    "AC Sleeper": {"price_multiplier": 2.5, "seats_per_row": 2, "total_seats": 24},
    "AC Semi-Sleeper": {"price_multiplier": 2.0, "seats_per_row": 2, "total_seats": 36},
    "Non-AC Sleeper": {"price_multiplier": 1.5, "seats_per_row": 2, "total_seats": 28},
    "Non-AC Seater": {"price_multiplier": 1.0, "seats_per_row": 2, "total_seats": 40},
    "Volvo AC": {"price_multiplier": 3.0, "seats_per_row": 2, "total_seats": 45},
    "Garuda Plus": {"price_multiplier": 3.5, "seats_per_row": 2, "total_seats": 42},
    "Express": {"price_multiplier": 1.8, "seats_per_row": 2, "total_seats": 38}
}

# In-memory storage (use database in production)
buses = []
bookings = {}
users_db = {}
user_bookings = {}

def generate_sample_buses():
    """Generate realistic bus data for Andhra Pradesh routes"""
    global buses
    buses = []
    
    # Popular routes with realistic pricing
    popular_routes = [
        ("Hyderabad", "Visakhapatnam", 650, 8),
        ("Hyderabad", "Vijayawada", 280, 4),
        ("Hyderabad", "Tirupati", 580, 7),
        ("Visakhapatnam", "Vijayawada", 350, 5),
        ("Vijayawada", "Tirupati", 220, 3),
        ("Hyderabad", "Kurnool", 210, 4),
        ("Visakhapatnam", "Rajahmundry", 200, 3),
        ("Vijayawada", "Eluru", 180, 2),
        ("Hyderabad", "Warangal", 150, 2),
        ("Tirupati", "Chennai", 150, 3)
    ]
    
    for i in range(200):  # Generate 200 buses
        if i < len(popular_routes):
            from_city, to_city, base_price, hours = popular_routes[i]
        else:
            # Random routes
            from_city = random.choice(CITIES)
            to_city = random.choice([c for c in CITIES if c != from_city])
            base_price = random.randint(150, 800)
            hours = random.randint(2, 10)
        
        # Generate realistic departure times
        departure_hour = random.choice([5, 6, 7, 8, 9, 10, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])
        departure_minute = random.choice([0, 15, 30, 45])
        departure_time = f"{departure_hour:02d}:{departure_minute:02d}"
        
        # Calculate arrival time
        arrival_hour = (departure_hour + hours) % 24
        arrival_minute = departure_minute
        if arrival_hour < departure_hour:
            arrival_date = (datetime.now() + timedelta(days=1)).day
        else:
            arrival_date = datetime.now().day
        arrival_time = f"{arrival_hour:02d}:{arrival_minute:02d}"
        
        # Select bus type and operator
        bus_type = random.choice(list(BUS_TYPES.keys()))
        operator = random.choice(BUS_OPERATORS)
        
        # Calculate available seats (realistic availability)
        total_seats = BUS_TYPES[bus_type]["total_seats"]
        if random.random() < 0.3:  # 30% of buses nearly full
            available_seats = random.randint(1, 8)
        elif random.random() < 0.6:  # 60% moderate availability
            available_seats = random.randint(9, total_seats // 2)
        else:  # 10% good availability
            available_seats = random.randint(total_seats // 2 + 1, total_seats - 5)
        
        bus_data = {
            "id": f"AP{1000 + i}",
            "operator": operator,
            "bus_type": bus_type,
            "from_city": from_city,
            "to_city": to_city,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
            "duration": f"{hours}h {random.randint(0, 59)}m",
            "base_price": base_price,
            "price": int(base_price * BUS_TYPES[bus_type]["price_multiplier"]),
            "total_seats": total_seats,
            "available_seats": available_seats,
            "rating": round(random.uniform(3.8, 4.9), 1),
            "amenities": random.sample([
                "WiFi", "Charging Points", "Water Bottle", "Blanket", 
                "Snacks", "AC", "Video Entertainment", "Emergency Exit",
                "Reading Light", "Curtains", "Pillow"
            ], k=random.randint(4, 7)),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "arrival_date": arrival_date
        }
        buses.append(bus_data)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    return hash_password(password) == password_hash

@app.route('/')
def index():
    return render_template('index.html', cities=CITIES)

@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register')
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password required'}), 400
    
    if username not in users_db:
        return jsonify({'success': False, 'error': 'Invalid username or password'}), 401
    
    if not verify_password(password, users_db[username]['password_hash']):
        return jsonify({'success': False, 'error': 'Invalid username or password'}), 401
    
    session['user_id'] = username
    session['username'] = username
    
    return jsonify({'success': True, 'message': 'Login successful'})

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    phone = data.get('phone', '').strip()
    
    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password required'}), 400
    
    if len(username) < 3:
        return jsonify({'success': False, 'error': 'Username must be at least 3 characters'}), 400
    
    if len(password) < 6:
        return jsonify({'success': False, 'error': 'Password must be at least 6 characters'}), 400
    
    if username in users_db:
        return jsonify({'success': False, 'error': 'Username already exists'}), 409
    
    users_db[username] = {
        'password_hash': hash_password(password),
        'email': email,
        'phone': phone,
        'created_at': datetime.now().isoformat()
    }
    
    return jsonify({'success': True, 'message': 'Account created successfully'})

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/search')
def search():
    from_city = request.args.get('from')
    to_city = request.args.get('to')
    date = request.args.get('date')
    
    if not from_city or not to_city:
        return redirect(url_for('index'))
    
    # Filter buses
    filtered_buses = [
        bus for bus in buses 
        if bus['from_city'].lower() == from_city.lower() 
        and bus['to_city'].lower() == to_city.lower()
        and bus['date'] == date
    ]
    
    return render_template('search.html', 
                         buses=filtered_buses, 
                         from_city=from_city, 
                         to_city=to_city, 
                         date=date)

@app.route('/bus/<bus_id>')
def bus_details(bus_id):
    bus = next((b for b in buses if b['id'] == bus_id), None)
    if not bus:
        return redirect(url_for('index'))
    
    # Generate seat layout
    bus_type_info = BUS_TYPES[bus['bus_type']]
    seats = []
    
    rows = bus_type_info['total_seats'] // bus_type_info['seats_per_row']
    for row in range(1, rows + 1):
        for seat_num in range(1, bus_type_info['seats_per_row'] + 1):
            seat_id = f"{row}{chr(64 + seat_num)}"
            # Simulate some seats already booked
            is_booked = random.random() < 0.25  # 25% chance seat is booked
            
            seats.append({
                'id': seat_id,
                'row': row,
                'number': seat_id,
                'is_booked': is_booked,
                'price': bus['price']
            })
    
    return render_template('bus_details.html', bus=bus, seats=seats)

@app.route('/api/book', methods=['POST'])
def book_bus():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Please login to book tickets'}), 401
    
    data = request.get_json()
    bus_id = data.get('bus_id')
    seats = data.get('seats', [])
    passenger_info = data.get('passenger_info', [])
    
    if not bus_id or not seats or not passenger_info:
        return jsonify({'success': False, 'error': 'Missing booking information'}), 400
    
    bus = next((b for b in buses if b['id'] == bus_id), None)
    if not bus:
        return jsonify({'success': False, 'error': 'Bus not found'}), 404
    
    # Calculate total price
    total_price = len(seats) * bus['price']
    
    # Apply discount
    discount = 0
    if len(seats) >= 3:
        discount = 0.1  # 10% discount for 3+ passengers
    elif len(seats) >= 2:
        discount = 0.05  # 5% discount for 2 passengers
    
    final_price = int(total_price * (1 - discount))
    
    # Generate booking ID
    booking_id = f"AP{datetime.now().strftime('%Y%m%d')}{random.randint(10000, 99999)}"
    
    # Store booking
    booking_data = {
        'booking_id': booking_id,
        'user_id': session['user_id'],
        'bus_id': bus_id,
        'bus_info': bus,
        'seats': seats,
        'passenger_info': passenger_info,
        'total_price': final_price,
        'original_price': total_price,
        'discount': discount,
        'booking_time': datetime.now().isoformat(),
        'status': 'confirmed'
    }
    
    bookings[booking_id] = booking_data
    
    if session['user_id'] not in user_bookings:
        user_bookings[session['user_id']] = []
    user_bookings[session['user_id']].append(booking_id)
    
    return jsonify({
        'success': True,
        'booking_id': booking_id,
        'total_price': final_price,
        'message': 'Booking confirmed successfully'
    })

@app.route('/booking/<booking_id>')
def booking_confirmation(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    booking = bookings.get(booking_id)
    if not booking or booking['user_id'] != session['user_id']:
        return redirect(url_for('index'))
    
    return render_template('booking_confirmation.html', booking=booking)

@app.route('/my-bookings')
def my_bookings():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_booking_ids = user_bookings.get(session['user_id'], [])
    user_booking_list = [bookings[bid] for bid in user_booking_ids if bid in bookings]
    
    return render_template('my_bookings.html', bookings=user_booking_list)

@app.route('/api/popular-routes')
def popular_routes():
    """Return popular routes for homepage"""
    routes = {}
    for bus in buses[:50]:  # Sample first 50 buses
        route = f"{bus['from_city']}-{bus['to_city']}"
        if route not in routes:
            routes[route] = {
                'from_city': bus['from_city'],
                'to_city': bus['to_city'],
                'min_price': bus['price'],
                'buses': 0
            }
        routes[route]['buses'] += 1
        routes[route]['min_price'] = min(routes[route]['min_price'], bus['price'])
    
    return jsonify(list(routes.values())[:12])

# Initialize sample data
generate_sample_buses()

# Create demo user
if 'demo' not in users_db:
    users_db['demo'] = {
        'password_hash': hash_password('demo123'),
        'email': 'demo@apbusbooking.com',
        'phone': '9876543210',
        'created_at': datetime.now().isoformat()
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
