from flask import (
    Blueprint,
    request,
    jsonify,
    current_app,
    Response,
    stream_with_context,
)
from app import db
from app.models import Task, Drone, Image
from app.decorators.auth_helpers import role_required, token_required
from app.decorators.db_helpers import session_app
from app.sse import connected_clients, notify_clients
import threading

bp = Blueprint("task_operations", __name__, url_prefix="/api/tasks")

# Task Status : Assigned, Not-Assigned, On-Progress, Completed


@bp.route("", methods=["POST"])
@session_app
@role_required("admin")
def add_task():
    try:
        data = request.get_json()

        if not data or not "task_name" in data or not "description" in data:
            return jsonify({"error": "Invalid input data"}), 400

        drone_ids = data.get("drone_ids", [])
        drones = []
        for drone_id in drone_ids:
            drone = Drone.query.get(drone_id)
            if not drone:
                return jsonify({"error": f"Drone with id {drone_id} not found"}), 404
            if drone.status != "assigned":
                drone.status = "assigned"
                db.session.add(drone)
            drones.append(drone)

        task_status = "assigned" if drones else "not-assigned"

        new_task = Task(
            task_name=data["task_name"],
            description=data["description"],
            status=task_status,
            drones=drones,  # Assigning the list of drones to the task
        )
        db.session.add(new_task)
        db.session.commit()

        # notify_clients('tasks_connection', new_task.to_dict())
        return jsonify(new_task.to_dict()), 201

    except Exception as e:
        return (
            jsonify(
                {
                    "error": "An unexpected error occurred at /api/tasks POST",
                    "details": str(e),
                }
            ),
            500,
        )


@bp.route("", methods=["GET"])
@session_app
@role_required("user", "admin")
def get_tasks():
    try:
        tasks = Task.query.all()
        tasks_details = [task.to_dict(task.status) for task in tasks]

        return jsonify(tasks_details), 200

    except Exception as e:
        return (
            jsonify(
                {
                    "error": "An unexpected error occurred at /api/tasks/ GET",
                    "details": str(e),
                }
            ),
            500,
        )


@bp.route("", methods=["PUT"])
@session_app
@role_required("admin")
def update_task():
    try:
        data = request.get_json()
        print("Gelen Veri:", data) 

        task_id = data.get("id")

        if not task_id:
            return jsonify({"error": "Task ID is required"}), 400

        task = Task.query.get(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        if isinstance(data.get("drone_ids", []), list) and all(isinstance(d, dict) for d in data["drone_ids"]):
            drone_ids = [drone['id'] for drone in data["drone_ids"]]
        else:
            drone_ids = data.get("drone_ids", [])

        print("Drone IDs:", drone_ids)  
        if task.status == 'completed':
            task_drone_ids = [d.id for d in task.drones]
            all_drones_exist = set(drone_ids) == set(task_drone_ids)
            if not all_drones_exist:
                return jsonify({"error": "Task already completed. You can not change the drones"}), 400

            if "task_name" in data:
                task.task_name = data["task_name"]
            else:
                return jsonify({"error": "Task name cannot be empty"}), 400

            if "description" in data:
                task.description = data["description"]
            else:
                return jsonify({"error": "Description cannot be empty"}), 400

            try:
                db.session.commit()
            except Exception as commit_error:
                db.session.rollback()
                print(f"Commit error: {commit_error}")
                return jsonify({"error": "Failed to commit changes", "details": str(commit_error)}), 500

            return jsonify(task.to_dict()), 200

        if "task_name" in data:
            task.task_name = data["task_name"]
        else:
            return jsonify({"error": "Task name cannot be empty"}), 400

        if "description" in data:
            task.description = data["description"]
        else:
            return jsonify({"error": "Description cannot be empty"}), 400

        if drone_ids is not None:
            current_drone_ids = {drone.id for drone in task.drones}
            new_drone_ids = set(drone_ids)
            
            drones_to_add = new_drone_ids - current_drone_ids
            drones_to_remove = current_drone_ids - new_drone_ids

            for drone_id in drones_to_remove:
                drone = Drone.query.get(drone_id)
                if drone:
                    task.drones.remove(drone)
                    drone.status = "offline"  

            # Add new drones to the task
            for drone_id in drones_to_add:
                drone = Drone.query.get(drone_id)
                if not drone:
                    return jsonify({"error": f"Drone with id {drone_id} not found"}), 404
                drone.status = "assigned"
                task.drones.append(drone)
                task.status = "assigned" 
                db.session.add(task)
                db.session.commit()               
                print(f"Drone {drone_id} added to task {task_id} and status set to assigned")

        if "status" in data:
            if data["status"] not in ["completed", "on-progress", "assigned", "not-assigned"]:
                return jsonify({"error": "Invalid status"}), 400
            if data["status"] == "completed":
                return jsonify({"message": "Already completed", "data": task.to_dict()}), 308
            task.status = data["status"]

        try:
            db.session.commit()
        except Exception as commit_error:
            db.session.rollback()
            print(f"Commit error: {commit_error}")
            return jsonify({"error": "Failed to commit changes", "details": str(commit_error)}), 500

        return jsonify(task.to_dict()), 200

    except Exception as e:
        print(f"Overall error: {e}")
        return jsonify(
            {
                "error": "An unexpected error occurred at /api/tasks/ PUT",
                "details": str(e),
            }
        ), 500
            
        
@bp.route("/<int:task_id>", methods=["GET"])
@session_app
@role_required("user", "admin")
def get_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        if task.status == "completed":
            return jsonify(task.to_dict(completed=True)), 200
        else:
            return jsonify(task.to_dict()), 200

    except Exception as e:
        return (
            jsonify(
                {
                    "error": "An unexpected error occurred at /api/tasks/task_id",
                    "details": str(e),
                }
            ),
            500,
        )


@bp.route("/<int:task_id>/execute", methods=["POST"])
@session_app
@role_required("admin")
def execute_task(task_id):
    try:
        task = Task.query.get_or_404(task_id)

        if not task.drones:
            return jsonify({"error": "No drones assigned to this task"}), 400

        if task.status == 'completed':
            return jsonify({"error": "Task already completed"}), 400

        task.status = "on-progress"
        for drone in task.drones:
            drone.status = "on-mission"
            db.session.add(drone)
        db.session.add(task)
        db.session.commit()

        app = current_app._get_current_object()

        threads = []
        for drone in task.drones:
            # It will probably change to dodrone.id because it is an thread
            stream = connected_clients[f"task_{task.id}_drone_{drone.id}"]
            thread = threading.Thread(
                target=drone.generate_and_store_images, args=(app, task.id, stream)
            )
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # After task is completed, check if drones are assigned to another task
        task.status = "completed"
        db.session.add(task)
        db.session.commit()
        for drone in task.drones:
            # Check if the drone is assigned to any other ongoing task
            ongoing_tasks = Task.query.filter(
                Task.drones.contains(drone), Task.status == "on-progress"
            ).all()
            if not ongoing_tasks:
                drone.status = "online"
            db.session.add(drone)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "Task execution completed",
                    "data": task.to_dict(completed=True),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "error": "An unexpected error occurred at /api/tasks/<task_id>/execute POST",
                    "details": str(e),
                }
            ),
            500,
        )


from app.utils.custom_redirect import custom_redirect_url, generate
from queue import Queue


@bp.route("/<int:id>/images", methods=["GET"])
@session_app
@token_required
def get_task_images(id):
    try:
        task = Task.query.get_or_404(id)

        # if task.status == 'completed':
        #     return task.to_dict(completed=True)

        custom_urls = []
        server_url = request.host_url
        for drone in task.drones:
            custom_url = f"{server_url}/api/tasks_{id}_drone_{drone.id}/stream"
            custom_urls.append(custom_url)

        queue = Queue()
        threads = []
        for url in custom_urls:
            thread = threading.Thread(target=custom_redirect_url, args=(url, queue))
            threads.append(thread)
            thread.start()

        return Response(
            stream_with_context(generate(threads, queue)),
            content_type="text/event-stream",
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "error": f"An unexpected error occurred at /api/tasks/{id}/images",
                    "details": str(e),
                }
            ),
            500,
        )
