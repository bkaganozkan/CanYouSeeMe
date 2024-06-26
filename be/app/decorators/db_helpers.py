from sqlalchemy.orm import scoped_session, sessionmaker
from flask import current_app
from app import db

def init_session():
    app = current_app._get_current_object()
    print("Current App:", app)  # Debug statement to check the current app
    try:
        engine = db.get_engine(bind_key='drones_db')
        print("Engine:", engine)  # Debug statement to check the engine
    except KeyError as e:
        print("KeyError:", e)  # Debug statement to print the KeyError
        raise RuntimeError("Database engine not found. Ensure the app context is correctly set and the database is initialized.")
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory, scopefunc=lambda: current_app._get_current_object())

def session_app(func):
    def wrapper(*args, **kwargs):
        with current_app.app_context():  # Ensure the app context is set
            session = init_session()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.remove()
    wrapper.__name__ = func.__name__  # Ensuring the function name stays the same
    return wrapper
