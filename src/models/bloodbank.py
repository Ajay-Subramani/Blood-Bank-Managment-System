from src.models.user import db
from datetime import datetime

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'blood_group': self.blood_group,
            'email': self.email,
            'registered_at': self.registered_at.isoformat() if self.registered_at else None
        }

class BloodRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    packets = db.Column(db.Integer, nullable=False)
    address = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(10), default='pending')  # 'pending' or 'accepted'
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'blood_group': self.blood_group,
            'packets': self.packets,
            'address': self.address,
            'status': self.status,
            'requested_at': self.requested_at.isoformat() if self.requested_at else None
        }

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donor.id'), nullable=True)
    blood_group = db.Column(db.String(5), nullable=False)
    packets = db.Column(db.Integer, nullable=False)
    donated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    donor = db.relationship('Donor', backref=db.backref('donations', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'donor_id': self.donor_id,
            'donor_name': self.donor.name if self.donor else None,
            'blood_group': self.blood_group,
            'packets': self.packets,
            'donated_at': self.donated_at.isoformat() if self.donated_at else None
        }

class BloodStock(db.Model):
    blood_group = db.Column(db.String(5), primary_key=True)
    total_packets = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'blood_group': self.blood_group,
            'total_packets': self.total_packets
        }

