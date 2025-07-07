from flask import Blueprint, request, jsonify, session
from src.models.bloodbank import Donor, BloodRequest, Donation, BloodStock, db

bloodbank_bp = Blueprint('bloodbank', __name__)

# Helper function to check if user is logged in
def require_login():
    if 'logged_in' not in session:
        return False
    return True

def require_admin():
    if not require_login() or session.get('role') != 'admin':
        return False
    return True

def require_user():
    if not require_login() or session.get('role') != 'user':
        return False
    return True

# Donor routes
@bloodbank_bp.route('/donors', methods=['POST'])
def register_donor():
    if not require_user():
        return jsonify({'message': 'Unauthorized access', 'status': 'error'}), 401
    
    try:
        data = request.get_json()
        
        donor = Donor(
            name=data['name'],
            age=data['age'],
            blood_group=data['blood_group'],
            email=data['email']
        )
        
        db.session.add(donor)
        db.session.commit()
        
        return jsonify({'message': 'Donor registered successfully', 'status': 'success'}), 201
    
    except Exception as e:
        return jsonify({'message': 'Donor registration failed', 'status': 'error', 'error': str(e)}), 400

@bloodbank_bp.route('/donors', methods=['GET'])
def get_donors():
    if not require_admin():
        return jsonify({'message': 'Unauthorized access', 'status': 'error'}), 401
    
    try:
        donors = Donor.query.order_by(Donor.registered_at.desc()).all()
        return jsonify({
            'donors': [donor.to_dict() for donor in donors],
            'status': 'success'
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to fetch donors', 'status': 'error', 'error': str(e)}), 400

# Blood request routes
@bloodbank_bp.route('/requests', methods=['POST'])
def create_request():
    if not require_user():
        return jsonify({'message': 'Unauthorized access', 'status': 'error'}), 401
    
    try:
        data = request.get_json()
        
        blood_request = BloodRequest(
            name=data['name'],
            blood_group=data['blood_group'],
            packets=data['packets'],
            address=data['address']
        )
        
        db.session.add(blood_request)
        db.session.commit()
        
        return jsonify({'message': 'Blood request submitted successfully', 'status': 'success'}), 201
    
    except Exception as e:
        return jsonify({'message': 'Request submission failed', 'status': 'error', 'error': str(e)}), 400

@bloodbank_bp.route('/requests', methods=['GET'])
def get_requests():
    if not require_admin():
        return jsonify({'message': 'Unauthorized access', 'status': 'error'}), 401
    
    try:
        requests = BloodRequest.query.order_by(BloodRequest.requested_at.desc()).all()
        return jsonify({
            'requests': [req.to_dict() for req in requests],
            'status': 'success'
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to fetch requests', 'status': 'error', 'error': str(e)}), 400

@bloodbank_bp.route('/requests/<int:request_id>/accept', methods=['PUT'])
def accept_request(request_id):
    if not require_admin():
        return jsonify({'message': 'Unauthorized access', 'status': 'error'}), 401
    
    try:
        blood_request = BloodRequest.query.get_or_404(request_id)
        blood_request.status = 'accepted'
        db.session.commit()
        
        return jsonify({'message': 'Request accepted successfully', 'status': 'success'}), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to accept request', 'status': 'error', 'error': str(e)}), 400

# Donation routes
@bloodbank_bp.route('/donations', methods=['POST'])
def log_donation():
    if not require_admin():
        return jsonify({'message': 'Unauthorized access', 'status': 'error'}), 401
    
    try:
        data = request.get_json()
        
        # Create donation record
        donation = Donation(
            donor_id=data['donor_id'],
            blood_group=data['blood_group'],
            packets=data['packets']
        )
        
        db.session.add(donation)
        
        # Update blood stock
        stock = BloodStock.query.filter_by(blood_group=data['blood_group']).first()
        if stock:
            stock.total_packets += data['packets']
        else:
            stock = BloodStock(
                blood_group=data['blood_group'],
                total_packets=data['packets']
            )
            db.session.add(stock)
        
        db.session.commit()
        
        return jsonify({'message': 'Donation logged successfully', 'status': 'success'}), 201
    
    except Exception as e:
        return jsonify({'message': 'Failed to log donation', 'status': 'error', 'error': str(e)}), 400

@bloodbank_bp.route('/donations', methods=['GET'])
def get_donations():
    if not require_admin():
        return jsonify({'message': 'Unauthorized access', 'status': 'error'}), 401
    
    try:
        donations = Donation.query.order_by(Donation.donated_at.desc()).all()
        return jsonify({
            'donations': [donation.to_dict() for donation in donations],
            'status': 'success'
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to fetch donations', 'status': 'error', 'error': str(e)}), 400

# Blood stock routes
@bloodbank_bp.route('/stock', methods=['GET'])
def get_blood_stock():
    if not require_admin():
        return jsonify({'message': 'Unauthorized access', 'status': 'error'}), 401
    
    try:
        stock = BloodStock.query.order_by(BloodStock.blood_group).all()
        return jsonify({
            'blood_stock': [s.to_dict() for s in stock],
            'status': 'success'
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to fetch blood stock', 'status': 'error', 'error': str(e)}), 400

# Combined logs endpoint for admin dashboard
@bloodbank_bp.route('/logs', methods=['GET'])
def get_logs():
    if not require_admin():
        return jsonify({'message': 'Unauthorized access', 'status': 'error'}), 401
    
    try:
        donations = Donation.query.order_by(Donation.donated_at.desc()).all()
        blood_stock = BloodStock.query.order_by(BloodStock.blood_group).all()
        
        return jsonify({
            'donations': [donation.to_dict() for donation in donations],
            'blood_stock': [stock.to_dict() for stock in blood_stock],
            'status': 'success'
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to fetch logs', 'status': 'error', 'error': str(e)}), 400

