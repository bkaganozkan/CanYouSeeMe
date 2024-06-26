from datetime import datetime
from app import db
from app.sse import notify_clients, connected_clients
from app.utils.images import generate_noisy_image
from flask import current_app
import time
from sqlalchemy import event

task_drone = db.Table('task_drone',
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True),
    db.Column('drone_id', db.Integer, db.ForeignKey('drones.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role
        }

class Drone(db.Model):
    __tablename__ = 'drones'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="offline")  # active, offline, on_mission, assigned

    tasks = db.relationship('Task', secondary=task_drone, back_populates='drones')

    def __repr__(self):
        return f'<Drone {self.name}>'


    def to_dict(self, include_images=False, task_id=None):
        drone_dict = {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'status': self.status,
        }
        if include_images and task_id is not None:
            
            images = Image.query.filter_by(drone_id=self.id, task_id=task_id).all()
            drone_dict['images'] = [{'id': image.id, 'image_path': image.from_server(current_app)} for image in images]
        return drone_dict
    
    def generate_and_store_images(self, app, task_id, stream=False):
        
        custom_url = f"task_{task_id}_drone_{self.id}"
        server_url = app.config['SERVER_URL']
        
        if stream:
            while not connected_clients[custom_url]:  
                time.sleep(1) 
        
        with app.app_context():
            for i in range(5):  
                if stream and not connected_clients[custom_url]:  
                    break
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"{custom_url}_image_{i}_{timestamp}.jpg"
                image_path = generate_noisy_image(filename)
                image_url = f"{server_url}/static/images/{filename}"
                
                # Actually it is the best option for the "live connection"
                # But I follow the tasks requirements.
                
                # if stream:
                #     notify_clients(custom_url, {'image_path': image_url})
                image = Image(data=image_path, drone_id=self.id, task_id=task_id)
                db.session.add(image)
                db.session.commit()
                time.sleep(1)

    def delete_with_related(self):
        # Silinecek ilişkili tüm görevler ve resimler
        Image.query.filter_by(drone_id=self.id).delete()
        db.session.delete(self)
        db.session.commit()
    
def drone_event_listener(mapper, connection, target):
    custom_url = "drones"
    event_data = {
        'action': 'insert',
        'drone': target.to_dict(include_images=True)
    }
    notify_clients(custom_url, event_data)

def drone_update_listener(mapper, connection, target):
    custom_url = "drones"
    event_data = {
        'action': 'update',
        'drone': target.to_dict()
    }
    notify_clients(custom_url, event_data)

def drone_delete_listener(mapper, connection, target):
    custom_url = f"drones"
    event_data = {
        'action': 'delete',
        'drone_id': target.id
    }
    notify_clients(custom_url,event_data)
  
    
event.listen(Drone, 'after_insert', drone_event_listener)  
event.listen(Drone, 'after_update', drone_update_listener)  
event.listen(Drone, 'after_delete', drone_delete_listener)  



class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), nullable=False) # on-progress, completed, assigned, not-assigned
    # created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    drones = db.relationship('Drone', secondary=task_drone, back_populates='tasks')

    def __repr__(self):
        return f'<Task {self.description}>'

    def to_dict(self, completed=False):
        return {
            'id': self.id,
            'task_name': self.task_name,
            'description': self.description,
            'status': self.status,
            'drones': [drone.to_dict(include_images=True, task_id=self.id) for drone in self.drones] if completed else [drone.to_dict() for drone in self.drones],
            'drones_id': [drone.id for drone in self.drones]
        }

def task_event_listener(mapper, connection, target):
    custom_url = "tasks"
    event_data = {
        'action': 'insert',
        'task': target.to_dict(completed=(target.status == 'completed'))
    }
    notify_clients(custom_url, event_data)

def task_update_listener(mapper, connection, target):
    custom_url = "tasks"
    event_data = {
        'action': 'update',
        'task': target.to_dict(completed=(target.status == 'completed'))
    }
    notify_clients(custom_url, event_data)

def task_delete_listener(mapper, connection, target):
    custom_url = f"tasks"
    event_data = {
        'action': 'delete',
        'task_id': target.id
    }
    notify_clients(custom_url,event_data)
  
    
event.listen(Task, 'after_insert', task_event_listener)  
event.listen(Task, 'after_update', task_update_listener)  
event.listen(Task, 'after_delete', task_delete_listener)  





class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    drone_id = db.Column(db.Integer, db.ForeignKey('drones.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    drone = db.relationship('Drone', backref='images')
    task = db.relationship('Task', backref='images')

    def __repr__(self):
        return f'<Image {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'image_path': self.data,
            'created': self.created.isoformat(),
            'drone_id': self.drone_id,
            'task_id': self.task_id
        }

    def from_server(self, app):
        server_url = app.config['SERVER_URL']
        return f"{server_url}/{self.data}"
    
    
def image_insert_listener(mapper, connection, target):
    custom_url = f"tasks_{target.task_id}_drone_{target.drone_id}"
    notify_clients(custom_url, { "id": target.id, "task_id":target.task_id,'drone_id': target.drone_id, 'image_path': target.from_server(current_app)})

event.listen(Image, 'after_insert', image_insert_listener)  

    
    
    
    
class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'jti': self.jti,
            'created_at': self.created_at.isoformat()
        }
