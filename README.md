# Blood Bank Management System 🩸

A comprehensive web-based blood bank management system built with Flask and Bootstrap, featuring user authentication, blood request management, donor registration, and admin dashboard functionality.

## ✨ Features

### User Features:
- User registration and authentication
- Blood request submission with patient details
- Donor registration with eligibility criteria
- Responsive design
- Dashboard with quick actions

### Admin Features:
- Admin dashboard with system overview
- Blood request management (approve/reject)
- Donor list management
- Blood stock tracking and donation logs
- Complete blood inventory management

## 🛠️ Technology Stack

- **Backend:** Flask (Python)
- **Database:** MySQL
- **Frontend:** HTML5, Bootstrap 5, Font Awesome
- **Authentication:** Flask sessions with password hashing
- **Styling:** Bootstrap 

## 📁 Project Structure

```
bloodbank_final/
├── src/
│   ├── main.py                 # Main Flask application
│   ├── models/
│   │   ├── user.py            # User model and authentication
│   │   └── bloodbank.py       # Blood bank related models
│   ├── routes/
│   │   ├── auth.py            # Authentication routes
│   │   └── bloodbank.py       # Blood bank management routes
│   ├── templates/             # HTML templates
│   │   ├── layout.html        # Base template
│   │   ├── home.html          # Home page
│   │   ├── register.html      # User registration
│   │   ├── login.html         # User login
│   │   ├── admin_dashboard.html
│   │   ├── user_dashboard.html
│   │   ├── contact.html       # Blood request form
│   │   ├── donor.html         # Donor registration
│   │   ├── requests.html      # Admin request management
│   │   ├── donor_list.html    # Admin donor list
│   │   └── donate_log.html    # Admin donation logs
│   └── database/              # Database files
├── venv/                      # Virtual environment
├── requirements.txt           # Python dependencies
├── run_app.py                # Application runner
└── README.md                 # This file
```

## 🚀 Local Setup Instructions

### Prerequisites:
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps:

1. **Extract the project:**
   clone the project on your pc
   ```bash
   git clone <repo url>
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python run_app.py
   ```

5. **Access the application:**
   - Open the link generated on the termonal with port  number
   - press ctrl + c to terminate running project

### Default Admin Account:
- **Email:** admin@bloodbank.com
- **Password:** admin123

## 🗄️ Database Setup

The application uses SQLite by default for easy setup. The database is automatically created when you first run the application.

### For MySQL (Production):
1. Install MySQL server
2. Create a database named `bloodbank`
3. Update the database configuration in `src/main.py`
4. Install MySQL client: `pip install mysqlclient`

## 📋 Usage Guide

### For Regular Users:
1. **Register:** Create an account as a "User"
2. **Login:** Use your credentials to access the dashboard
3. **Request Blood:** Fill out the blood request form with patient details
4. **Register as Donor:** Complete the donor registration form

### For Administrators:
1. **Login:** Use admin credentials
2. **Manage Requests:** View and approve/reject blood requests
3. **View Donors:** Access the complete donor database
4. **Track Donations:** Monitor blood stock and donation logs
5. **Update Stock:** Manage blood inventory levels

## 🎨 Design Features

- **Responsive Design:** Works on desktop, tablet, and mobile devices
- **Reddish Theme:** Professional medical-themed color scheme
- **Bootstrap Integration:** Modern UI components and styling
- **Font Awesome Icons:** Professional iconography throughout
- **User-Friendly Forms:** Intuitive form design with validation

## 🔧 API Endpoints

### Authentication:
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/logout` - User logout

### Blood Bank Management:
- `POST /api/blood-request` - Submit blood request
- `POST /api/donor-register` - Register as donor
- `GET /api/requests` - Get all requests (Admin)
- `POST /api/approve-request` - Approve request (Admin)
- `GET /api/donors` - Get all donors (Admin)
- `POST /api/add-donation` - Add donation log (Admin)

## 🚀 Deployment and live demo

The application is already deployed and accessible at: https://w5hni7cozqqm.manus.space

### For Custom Deployment:
1. Set up a production server (Ubuntu/CentOS)
2. Install Python, pip, and required dependencies
3. Configure a production WSGI server (Gunicorn)
4. Set up a reverse proxy (Nginx)
5. Configure SSL certificates for HTTPS

## 🔒 Security Features

- Password hashing using Werkzeug security
- Session-based authentication
- CSRF protection on forms
- Input validation and sanitization
- Role-based access control (Admin/User)

## 📝 College Project Notes

This project is designed as a comprehensive college-level assignment demonstrating:
- Full-stack web development skills
- Database design and management
- User authentication and authorization
- RESTful API development
- Responsive web design
- Professional code organization

## 🤝 Contributing

This is a college project, but suggestions for improvements are welcome:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is created for educational purposes as part of a college assignment. Not for any production use.


## 📞 Support

For any issues or questions regarding this project, please refer to the code comments and documentation within the source files.
For commercial purpose conctact me through
ajaysubramani.career@gmail.com


**Note:** This is a college project demonstrating blood bank management system functionality. For production use, additional security measures and testing would be required.
