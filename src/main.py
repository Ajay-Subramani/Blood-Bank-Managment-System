import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, render_template, session, redirect, url_for, flash, request
from src.models.user import db, User
from src.models.bloodbank import Donor, BloodRequest, Donation, BloodStock
from src.routes.auth import auth_bp
from src.routes.bloodbank import bloodbank_bp

app = Flask(__name__, 
           static_folder=os.path.join(os.path.dirname(__file__), 'static'),
           template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(bloodbank_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# Web routes for HTML pages
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'danger')
            return render_template('register.html')

        # Create new user
        user = User(name=name, email=email, role=role)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['logged_in'] = True
            session['user_id'] = user.id
            session['email'] = user.email
            session['role'] = user.role
            session['name'] = user.name
            
            flash('You are now logged in', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid login credentials', 'danger')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        flash('Please log in to access dashboard', 'danger')
        return redirect(url_for('login'))
    
    if session['role'] == 'admin':
        return render_template('admin_dashboard.html')
    else:
        return render_template('user_dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('home'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if 'logged_in' not in session or session['role'] != 'user':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        blood_group = request.form['blood_group']
        packets = request.form['packets']
        address = request.form['address']

        blood_request = BloodRequest(
            name=name,
            blood_group=blood_group,
            packets=packets,
            address=address
        )
        
        db.session.add(blood_request)
        db.session.commit()
        
        flash('Blood request submitted successfully', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('contact.html')

@app.route('/donor', methods=['GET', 'POST'])
def donor():
    if 'logged_in' not in session or session['role'] != 'user':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        blood_group = request.form['blood_group']
        email = request.form['email']

        donor = Donor(
            name=name,
            age=age,
            blood_group=blood_group,
            email=email
        )
        
        db.session.add(donor)
        db.session.commit()
        
        flash('Donor registered successfully', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('donor.html')

@app.route('/requests')
def requests_admin():
    if 'logged_in' not in session or session['role'] != 'admin':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    requests = BloodRequest.query.order_by(BloodRequest.requested_at.desc()).all()
    return render_template('requests.html', requests=requests)

@app.route('/requests/<int:id>/accept', methods=['POST'])
def accept_request(id):
    if 'logged_in' not in session or session['role'] != 'admin':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    blood_request = BloodRequest.query.get_or_404(id)
    blood_request.status = 'accepted'
    db.session.commit()
    
    flash('Request accepted successfully', 'success')
    return redirect(url_for('requests_admin'))

@app.route('/donors')
def donor_list():
    if 'logged_in' not in session or session['role'] != 'admin':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    donors = Donor.query.order_by(Donor.registered_at.desc()).all()
    return render_template('donor_list.html', donors=donors)

@app.route('/donate', methods=['GET', 'POST'])
def donate_log():
    if 'logged_in' not in session or session['role'] != 'admin':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        donor_id = request.form['donor_id']
        blood_group = request.form['blood_group']
        packets = int(request.form['packets'])

        # Create donation record
        donation = Donation(
            donor_id=donor_id,
            blood_group=blood_group,
            packets=packets
        )
        
        db.session.add(donation)
        
        # Update blood stock
        stock = BloodStock.query.filter_by(blood_group=blood_group).first()
        if stock:
            stock.total_packets += packets
        else:
            stock = BloodStock(
                blood_group=blood_group,
                total_packets=packets
            )
            db.session.add(stock)
        
        db.session.commit()
        
        flash('Donation logged and stock updated successfully', 'success')
        return redirect(url_for('donate_log'))
    
    donations = Donation.query.order_by(Donation.donated_at.desc()).all()
    blood_stock = BloodStock.query.order_by(BloodStock.blood_group).all()
    return render_template('donate_log.html', donations=donations, blood_stock=blood_stock)

# Serve static files
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

