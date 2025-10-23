from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time

class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({"status": "healthy", "timestamp": int(time.time())})
            self.wfile.write(response.encode())
            print("✅ Health check received")
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/sms/batch':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            print(f"📱 Received {len(data.get('contacts', []))} contacts")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = json.dumps({
                "results": [{"status": "sent", "error": None} for _ in data.get('contacts', [])],
                "total": len(data.get('contacts', [])),
                "successful": len(data.get('contacts', [])),
                "batch_id": f"mock_{int(time.time())}"
            })
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        print(f"🌐 {self.address_string()} - {format % args}")

print("🚀 Starting simple mock server on http://localhost:8080")
server = HTTPServer(('localhost', 8080), MockHandler)
server.serve_forever()