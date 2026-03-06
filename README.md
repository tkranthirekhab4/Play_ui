# AP Bus Booking - Andhra Pradesh Bus Ticket Booking System

A comprehensive bus booking website for Andhra Pradesh with real-time seat selection, user authentication, and booking management.

## Features

### 🚌 Core Functionality
- **Route Search**: Search buses between any Andhra Pradesh cities
- **Real-time Data**: 200+ sample buses with realistic schedules
- **Seat Selection**: Interactive seat layout with visual feedback
- **User Authentication**: Secure login/registration system
- **Booking Management**: Complete booking history and management
- **Payment Simulation**: Discount calculation and confirmation
- **Responsive Design**: Mobile-friendly modern UI

### 🏙‍♂️ User Features
- Account registration and login
- Demo account for testing (demo/demo123)
- Booking history management
- Ticket download and printing
- Cancellation functionality

### 🎨 UI/UX Features
- Modern gradient design
- Interactive seat selection
- Real-time filtering and sorting
- Loading states and notifications
- Mobile-responsive layout
- Accessibility features

## Quick Start

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/tkranthirekhab4/Play_ui
cd Play_ui

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Access the Website
Open your browser and go to: `http://localhost:5000`

## Demo Account
For quick testing, use the demo account:
- **Username**: demo
- **Password**: demo123

## Available Cities
The system includes all major Andhra Pradesh cities:
- Hyderabad, Visakhapatnam, Vijayawada, Guntur, Nellore
- Kurnool, Tirupati, Warangal, Kakinada, Anantapur
- Eluru, Rajahmundry, Nizamabad, Karimnagar, Machilipatnam
- And 15 more cities...

## Bus Operators
Multiple operators including:
- APSRTC (Andhra Pradesh State Road Transport Corporation)
- Orange Travels, SRS Travels, VRL Logistics
- Kaveri Travels, Morning Star Travels, Diwakar Travels
- Kesineni Travels and more...

## Bus Types
- AC Sleeper, AC Semi-Sleeper, Non-AC Sleeper
- Non-AC Seater, Volvo AC, Garuda Plus, Express

## Project Structure

```
Play_ui/
├── app.py                 # Main Flask application
├── requirements.txt         # Python dependencies
├── templates/             # HTML templates
│   ├── index.html          # Homepage with search
│   ├── search.html         # Bus search results
│   ├── bus_details.html    # Seat selection page
│   ├── login.html          # User login
│   ├── register.html       # User registration
│   ├── booking_confirmation.html  # Booking confirmation
│   └── my_bookings.html   # User booking history
└── README.md             # This file
```

## API Endpoints

### Authentication
- `GET /` - Homepage
- `GET /login` - Login page
- `GET /register` - Registration page
- `POST /api/login` - Login API
- `POST /api/register` - Registration API
- `POST /api/logout` - Logout API

### Booking
- `GET /search?from=X&to=Y&date=Z` - Search buses
- `GET /bus/<bus_id>` - Bus details and seat selection
- `POST /api/book` - Book seats
- `GET /booking/<booking_id>` - Booking confirmation
- `GET /my-bookings` - User booking history
- `GET /api/popular-routes` - Popular routes API

## Sample Data

The application generates realistic sample data including:
- **200+ buses** across Andhra Pradesh routes
- **Realistic schedules** with departure/arrival times
- **Dynamic pricing** based on bus type and distance
- **Seat availability** simulation
- **Popular routes** with multiple daily options

## Technologies Used

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Tailwind CSS
- **Icons**: Font Awesome
- **Data**: JSON-based in-memory storage
- **Authentication**: Session-based with password hashing

## Features in Detail

### 🔍 Smart Search
- City autocomplete
- Date picker with validation
- Passenger count selection
- Bus type filtering
- Popular routes quick access

### 💺 Interactive Seat Selection
- Visual seat layout
- Real-time availability
- Click to select/deselect
- Price calculation
- Passenger form generation

### 📱 Responsive Design
- Mobile-first approach
- Touch-friendly interface
- Adaptive layouts
- Optimized performance

### 🔐 Security Features
- Password hashing (SHA-256)
- Session management
- Input validation
- XSS protection
- CSRF protection

## Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
For production deployment:
1. Use a proper database (PostgreSQL/MySQL)
2. Set up environment variables
3. Configure production web server (Gunicorn/Nginx)
4. Set up SSL certificates
5. Configure domain and DNS

## Future Enhancements

- 📧 Real-time GPS tracking
- 💳 Payment gateway integration
- 📱 Mobile app development
- 🔄 Real-time notifications
- 📊 Analytics dashboard
- 🎫 Multi-language support

## Support

For any queries or support:
- 📧 Technical: Check the code documentation
- 📧 Features: Review the implemented functionality
- 🚀 Deployment: Follow the deployment guide
- 📞 Issues: Report via GitHub issues

## License

This project is for educational and demonstration purposes. Feel free to modify and enhance according to your needs.

---

**Happy Coding! 🚍**
