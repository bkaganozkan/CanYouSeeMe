def register_routes(app):
    from app.routes.task_operations import bp as task_bp
    from app.routes.drone_operations import bp as drone_bp
    from app.routes.user_operations import bp as user_bp
    from app.sse import sse 

    app.register_blueprint(task_bp)
    app.register_blueprint(drone_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(sse)