from flask import Blueprint, request, jsonify
from app import db
from app.models import Drone
from app.decorators.auth_helpers import role_required
from app.decorators.db_helpers import session_app
from app.decorators.notify_on_change import notify_on_change

bp = Blueprint('drone_operations', __name__, url_prefix='/api/drones')

# Drone status cases; Offline, Online, Assigned, On-Mission

@bp.route('', methods=['GET' ])
@role_required('user','admin')
def get_drones():
    try:
        drones = Drone.query.all()
        
        drone_data = [drone.to_dict() for drone in drones]
        return jsonify(drone_data), 200

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred at /api/drones GET', 'details': str(e)}), 500


@bp.route('', methods=['POST'])
@session_app
@role_required('admin')
def add_drone():
    try:
        data = request.get_json()
        new_drone = Drone(name=data['name'], model=data['model'], status=data['status'])  # Statüs 'offline' olarak ayarlandı
        db.session.add(new_drone)
        db.session.commit()        
        # notify_clients('drones', message)

        return jsonify(new_drone.to_dict()), 201

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred at /api/drones POST', 'details': str(e)}), 500


@bp.route('', methods=['PUT'])
@session_app
@role_required('admin')
def update_drone():
    data = request.get_json()
    
    drone_id = data['id']
    if not drone_id:
            return jsonify({'error': 'Drone ID is required'}), 400
    
    drone = Drone.query.get(drone_id)
    if not drone:
        return jsonify({'error': 'Drone not found'}), 404
    if 'name' in data:
        drone.name = data['name']
    if 'model' in data:
        drone.model = data['model']
    if 'status' in data:
        if data['status'] not in ['offline', 'online', 'on-mission', 'assigned']:  # Input validation
            return jsonify({'error': 'Invalid status parameter'}), 400
        drone.status = data['status']

    db.session.commit()

    return jsonify(drone.to_dict()), 200


@bp.route('<int:id>', methods=['DELETE'])
@role_required('admin')
def delete_drone(id):
    try:
        # ID kontrolü
        if not id:
            return jsonify({'error': 'ID Required'}), 400
        
        # Drone varlığını kontrol etme
        drone = Drone.query.get(id)
        if not drone:
            return jsonify({'error': 'Drone not found'}), 404
        
        drone.delete_with_related()

        # Drone silme işlemi
        db.session.delete(drone)
        db.session.commit()

        # Başarılı silme işlemi mesajı ve silinen drone ID'si
        return jsonify({'message': 'Drone deleted successfully', 'id': id}), 200

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred at /api/drones DELETE', 'details': str(e)}), 500