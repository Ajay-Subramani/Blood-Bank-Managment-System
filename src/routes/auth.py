from flask import Blueprint, request, jsonify, session
from src.models.user import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'message': 'Email already registered', 'status': 'error'}), 400
        
        # Create new user
        user = User(
            name=data['name'],
            email=data['email'],
            role=data.get('role', 'user')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'User registered successfully', 'status': 'success'}), 201
    
    except Exception as e:
        return jsonify({'message': 'Registration failed', 'status': 'error', 'error': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        user = User.query.filter_by(email=data['email']).first()
        
        if user and user.check_password(data['password']):
            session['logged_in'] = True
            session['user_id'] = user.id
            session['email'] = user.email
            session['role'] = user.role
            session['name'] = user.name
            
            return jsonify({
                'message': 'Login successful',
                'status': 'success',
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({'message': 'Invalid credentials', 'status': 'error'}), 401
    
    except Exception as e:
        return jsonify({'message': 'Login failed', 'status': 'error', 'error': str(e)}), 400

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully', 'status': 'success'}), 200

@auth_bp.route('/session', methods=['GET'])
def get_session():
    if 'logged_in' in session:
        return jsonify({
            'logged_in': True,
            'user_id': session.get('user_id'),
            'email': session.get('email'),
            'role': session.get('role'),
            'name': session.get('name')
        }), 200
    else:
        return jsonify({'logged_in': False}), 200

