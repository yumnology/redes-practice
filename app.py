from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://security_system_user:TLhZbPvnttmPuTwGrWrAdPUaT3HkAa4m@dpg-cq1jencs1f4s738ifgog-a.oregon-postgres.render.com/security_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doorstatus = db.Column(db.String(10), nullable=True)
    windowstatus = db.Column(db.String(10), nullable=True)
    doorbell = db.Column(db.String(10), nullable=True)
    temperature = db.Column(db.Float, nullable=True)
    laser = db.Column(db.String(10), nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'doorstatus': self.doorstatus,
            'windowstatus': self.windowstatus,
            'doorbell': self.doorbell,
            'temperature': self.temperature,
            'laser': self.laser
        }

BASE_URL = '/api/'

@app.route('/')
def home():
    return 'Welcome to the State API'

@app.route(BASE_URL + 'state', methods=['POST'])
def create_state():
    if not request.json:
        abort(400, description='Missing JSON data in request')
    
    state = State(
        doorstatus=request.json.get('doorstatus'),
        windowstatus=request.json.get('windowstatus'),
        doorbell=request.json.get('doorbell'),
        temperature=request.json.get('temperature'),
        laser=request.json.get('laser')
    )
    db.session.add(state)
    db.session.commit()
    return jsonify(state.to_json()), 201

@app.route(BASE_URL + 'state', methods=['GET'])
def get_latest_state():
    state = State.query.order_by(State.id.desc()).first()
    if not state:
        abort(404, description='State not found')
    return jsonify(state.to_json())

@app.route(BASE_URL + 'state/<int:id>', methods=['GET'])
def get_state(id):
    state = State.query.get(id)
    if not state:
        abort(404, description='State not found')
    return jsonify(state.to_json(), 201)

@app.route(BASE_URL + 'state/<int:id>', methods=['PUT'])
def update_state(id):
    state = State.query.get(id)
    if not state:
        abort(404, description='State not found')

    if 'doorstatus' in request.json:
        state.doorstatus = request.json['doorstatus']
    if 'windowstatus' in request.json:
        state.windowstatus = request.json['windowstatus']
    if 'doorbell' in request.json:
        state.doorbell = request.json['doorbell']
    if 'temperature' in request.json:
        state.temperature = request.json['temperature']
    if 'laser' in request.json:
        state.laser = request.json['laser']

    db.session.commit()
    return jsonify(state.to_json())

@app.route(BASE_URL + 'state/<int:id>', methods=['DELETE'])
def delete_state(id):
    state = State.query.get(id)
    if not state:
        abort(404, description='State not found')
    db.session.delete(state)
    db.session.commit()
    return jsonify({'result': True})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)