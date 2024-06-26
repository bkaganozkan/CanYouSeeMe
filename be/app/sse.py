from flask import Blueprint, Response, stream_with_context, request, jsonify
import json
from queue import Queue
from collections import defaultdict
from app.decorators.auth_helpers  import role_required

sse = Blueprint('sse', __name__)

# Global dictionary to keep track of clients for each custom URL
clients = defaultdict(list)
connected_clients = defaultdict(bool)

@role_required('user')  
@sse.route('/api/<custom_url>/stream', methods=['GET'])
def stream(custom_url):
    def event_stream():
        messages = Queue()
        clients[custom_url].append(messages)
        connected_clients[custom_url] = True
        try:
            while True:
                message = messages.get()
                yield f'data: {message}\n\n'
        except GeneratorExit:
            clients[custom_url].remove(messages)
            if not clients[custom_url]:
                connected_clients[custom_url] = False
    
    return Response(stream_with_context(event_stream()), content_type='text/event-stream')

def notify_clients(custom_url, data):
    for client in clients[custom_url]:
            client.put(json.dumps(data))
            
