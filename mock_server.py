# mock_server.py (เวอร์ชัน Production)
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import os

# เพิ่ม path เพื่อ import database.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import DatabaseManager

class RegisterHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <!DOCTYPE html>
            <html>
            <head><title>RPA System</title></head>
            <body>
                <h2>🚀 RPA System Status</h2>
                <p>✅ Web Server Running</p>
                <p>📊 <a href="/dashboard">Dashboard</a></p>
                <p>📝 <a href="/register">Registration Form</a></p>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
            
        elif self.path == "/register":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <!DOCTYPE html>
            <html>
            <head><title>Registration Form</title></head>
            <body>
                <h2>📝 Registration Form</h2>
                <form id="registerForm">
                    <label>Username: <input type="text" id="username" name="username"></label><br><br>
                    <label>Email: <input type="email" id="email" name="email"></label><br><br>
                    <label>Phone: <input type="text" id="phone" name="phone"></label><br><br>
                    <button type="button" id="register_btn" onclick="submitForm()">Register</button>
                </form>
                <div id="result"></div>
                <script>
                    function submitForm() {
                        const data = {
                            username: document.getElementById('username').value,
                            email: document.getElementById('email').value,
                            phone: document.getElementById('phone').value
                        };
                        fetch('/api/register', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify(data)
                        })
                        .then(res => res.json())
                        .then(result => {
                            document.getElementById('result').innerHTML = 
                                `<p style="color:green;">✅ ${result.message}</p>`;
                        });
                    }
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
            
        elif self.path == "/dashboard":
            # เปลี่ยนเส้นทางไปยัง Flask Dashboard
            self.send_response(302)
            self.send_header('Location', 'http://localhost:5000')
            self.end_headers()
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == "/api/register":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            print(f"📝 Received: {data}")
            
            # จำลองการบันทึก
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "success", "message": "Registration successful!"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=80):
    server_address = ('0.0.0.0', port)  # 0.0.0.0 = เปิดให้เข้าถึงจากภายนอก
    httpd = HTTPServer(server_address, RegisterHandler)
    print(f"🚀 Mock Server running on http://localhost:{port}")
    print(f"📝 Registration: http://localhost:{port}/register")
    print(f"📊 Dashboard: http://localhost:{port}/dashboard")
    print("Press Ctrl+C to stop")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()