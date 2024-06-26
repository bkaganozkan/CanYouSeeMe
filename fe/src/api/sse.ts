
const API_BASE_URL = process.env.VUE_APP_API_BASE_URL;

class SSEClient {
  private eventSource: EventSource | null = null;
  private listeners: Array<(data: any) => void> = [];
  private url: string;

  constructor(url: string, tokenReq = false) {
    const token = localStorage.getItem('authToken');
    if (tokenReq)
      this.url = `${API_BASE_URL}${url}?token=${token}`;
    else
      this.url = `${API_BASE_URL}${url}`;
    this.connect();
  }

  private connect() {
    this.eventSource = new EventSource(this.url);

    this.eventSource.onopen = () => {
      console.log('SSE connection established');
    };

    this.eventSource.onmessage = (event: MessageEvent) => {
      const rawData = event.data;
      try {
        const data = JSON.parse(rawData.replace(/^data: /, ''));
        this.listeners.forEach((listener) => listener(data));
      } catch (error) {
        console.error('Error parsing SSE data:', error);
        console.error('Received raw data:', rawData);
        this.eventSource?.close();
      }
    };

    this.eventSource.onerror = (error) => {
      this.flushMessages();
      this.eventSource?.close();
      setTimeout(() => this.connect(), 5000); // reconnect after 5 seconds
    };
  }

  public addListener(listener: (data: any) => void) {
    this.listeners.push(listener);
  }

  public close() {
    if (this.eventSource) {
      this.eventSource.close();
    }
  }

  private flushMessages() {
    this.listeners = [];
    console.log('Flushed all messages');
  }
}

export default SSEClient;
