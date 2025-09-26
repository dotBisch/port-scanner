from flask import Flask, request, jsonify, render_template_string
from secure_port_scanner import SecurePortScanner
import time

app = Flask(__name__)

# Rate limiting storage (in production, use Redis or database)
request_history = {}

def is_rate_limited(client_ip, limit=5, window=60):
    """Simple rate limiting: 5 requests per minute"""
    now = time.time()
    if client_ip not in request_history:
        request_history[client_ip] = []
    
    # Clean old requests
    request_history[client_ip] = [
        req_time for req_time in request_history[client_ip] 
        if now - req_time < window
    ]
    
    if len(request_history[client_ip]) >= limit:
        return True
    
    request_history[client_ip].append(now)
    return False

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Educational Port Scanner</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .warning { background: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .form-group { margin: 15px 0; }
            input, button { padding: 8px; margin: 5px; }
            button { background: #007bff; color: white; border: none; border-radius: 3px; }
            pre { background: #f8f9fa; padding: 15px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>Educational Port Scanner</h1>
        
        <div class="warning">
            <strong>⚠️ Educational Use Only</strong><br>
            This tool is for educational purposes only. Only scan systems you own or have permission to test.
            Unauthorized scanning may violate terms of service or local laws.
        </div>
        
        <form id="scanForm">
            <div class="form-group">
                <label>Target (allowed: scanme.nmap.org, testphp.vulnweb.com):</label><br>
                <input type="text" id="target" value="scanme.nmap.org" required>
            </div>
            
            <div class="form-group">
                <label>Start Port:</label><br>
                <input type="number" id="startPort" value="20" min="1" max="65535" required>
            </div>
            
            <div class="form-group">
                <label>End Port:</label><br>
                <input type="number" id="endPort" value="80" min="1" max="65535" required>
            </div>
            
            <div class="form-group">
                <label>
                    <input type="checkbox" id="verbose"> Verbose output
                </label>
            </div>
            
            <button type="submit">Scan Ports</button>
        </form>
        
        <div id="result"></div>
        
        <script>
            document.getElementById('scanForm').onsubmit = function(e) {
                e.preventDefault();
                
                const target = document.getElementById('target').value;
                const startPort = document.getElementById('startPort').value;
                const endPort = document.getElementById('endPort').value;
                const verbose = document.getElementById('verbose').checked;
                
                document.getElementById('result').innerHTML = '<p>Scanning... Please wait.</p>';
                
                fetch('/scan', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        target: target,
                        port_range: [parseInt(startPort), parseInt(endPort)],
                        verbose: verbose
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById('result').innerHTML = 
                            '<div style="color: red;"><strong>Error:</strong> ' + data.error + '</div>';
                    } else {
                        document.getElementById('result').innerHTML = 
                            '<h3>Results:</h3><pre>' + JSON.stringify(data.result, null, 2) + '</pre>';
                    }
                })
                .catch(error => {
                    document.getElementById('result').innerHTML = 
                        '<div style="color: red;"><strong>Error:</strong> ' + error + '</div>';
                });
            };
        </script>
    </body>
    </html>
    ''')

@app.route('/scan', methods=['POST'])
def scan_ports():
    client_ip = request.remote_addr
    
    # Rate limiting
    if is_rate_limited(client_ip):
        return jsonify({'error': 'Rate limit exceeded. Please wait before scanning again.'}), 429
    
    try:
        data = request.get_json()
        target = data.get('target')
        port_range = data.get('port_range')
        verbose = data.get('verbose', False)
        
        if not target or not port_range:
            return jsonify({'error': 'Missing required parameters'}), 400
        
        scanner = SecurePortScanner()
        result = scanner.get_open_ports(target, port_range, verbose)
        
        return jsonify({'result': result})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("⚠️  Educational Port Scanner - Use Responsibly")
    print("📚 Only scan systems you own or have permission to test")
    app.run(debug=True, host='127.0.0.1', port=5000)