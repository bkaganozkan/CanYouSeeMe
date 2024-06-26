import requests as req
from queue import Queue, Empty

def custom_redirect_url(custom_url, queue):
    response = req.get(custom_url, stream=True)
    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                data = line.decode('utf-8')
                queue.put(data)
    else:
        error_message = f"Error: Received status code {response.status_code} from {custom_url}"
        print(error_message)
        queue.put(error_message)
        
def generate(threads, queue):
            timeout = 10
            while any(thread.is_alive() for thread in threads) or not queue.empty():
                try:
                    data = queue.get()
                    yield f'data: {data}\n\n'
                except Empty:
                    yield f'data: Timeout error: No data received in the last {timeout} seconds\n\n'
                    yield f'\n\n'