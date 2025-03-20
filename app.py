from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields
from flask_cors import CORS  # Ensure CORS is imported
from flask import render_template

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments21.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize Flask-RESTX for Swagger documentation
api = Api(app, version='1.0', title='Appointment API', description='Manage Appointments')
ns = api.namespace('appointments', description='Appointment operations')

# Enable CORS to handle cross-origin requests
CORS(app)

# Define Appointment Model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    appointment_date = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Appointment {self.full_name}>'

# Swagger Model for input validation
appointment_model = api.model('Appointment', {
    'full_name': fields.String(required=True, description='Full Name of the user'),
    'phone_number': fields.String(required=True, description='Contact number'),
    'email': fields.String(required=True, description='User email'),
    'appointment_date': fields.String(required=True, description='Preferred appointment date'),
    'message': fields.String(description='Additional message')
})

# Create Database Tables
with app.app_context():
    db.create_all()

# Define the GET and POST APIs
@ns.route('/')
class AppointmentList(Resource):
    def get(self):
        """Get all appointments"""
        appointments = Appointment.query.all()
        return jsonify([
            {
                'id': appointment.id,
                'full_name': appointment.full_name,
                'phone_number': appointment.phone_number,
                'email': appointment.email,
                'appointment_date': appointment.appointment_date,
                'message': appointment.message
            }
            for appointment in appointments
        ])

    @api.expect(appointment_model)
    def post(self):
        """Create a new appointment"""
        data = request.json
        new_appointment = Appointment(
            full_name=data['full_name'],
            phone_number=data['phone_number'],
            email=data['email'],
            appointment_date=data['appointment_date'],
            message=data.get('message', '')
        )
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({
            'id': new_appointment.id,
            'full_name': new_appointment.full_name,
            'phone_number': new_appointment.phone_number,
            'email': new_appointment.email,
            'appointment_date': new_appointment.appointment_date,
            'message': new_appointment.message
        })
@app.route('/drappointment')
def drappointment_page():
    appointments = Appointment.query.all()
    return render_template('drappointment.html', appointments=appointments)

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
