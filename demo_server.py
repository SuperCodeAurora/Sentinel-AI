from flask import Flask, request, jsonify
# Import the new class name
from src import DiamondShield

app = Flask(__name__)
# Initialize the Firewall Engine
firewall = DiamondShield()

@app.before_request
def waf_middleware():
    """
    Middleware that intercepts every request before it reaches the endpoint.
    """
    client_ip = request.remote_addr
    payload = request.args.get('q', '') + str(request.form) + str(request.json)
    user_agent = request.headers.get('User-Agent', '')

    # Send to Firewall
    decision = firewall.inspect_request(client_ip, payload, user_agent)

    if not decision['allowed']:
        return jsonify({
            "error": "Request Blocked by DiamondShield",
            "reason": decision['reason']
        }), 403

@app.route('/')
def home():
    return "<h1>Secure Server Online</h1><p>DiamondShield is Active.</p>"

if __name__ == '__main__':
    print(f"🛡️  DiamondShield-Sentinel-AI Initialized...")
    app.run(port=5000)
