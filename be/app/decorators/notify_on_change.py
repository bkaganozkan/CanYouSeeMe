from functools import wraps
from flask import jsonify
from app.sse import notify_clients

def notify_on_change(*custom_url_templates):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            response, status_code = result if isinstance(result, tuple) else (result, None)
            if isinstance(response, (dict, list)):
                for url_template in custom_url_templates:
                    custom_url = url_template.format(**kwargs)
                    notify_clients(custom_url, response)
            elif hasattr(response, 'get_json'):
                for url_template in custom_url_templates:
                    custom_url = url_template.format(**kwargs)
                    notify_clients(custom_url, response.get_json())
            return result
        return wrapper
    return decorator