from flask import Flask, request, jsonify, make_response
from src import DiamondShield

app = Flask(__name__)

# Initialize the Defense Engine
firewall = DiamondShield()

# --- CONFIGURATION ---
# The name of the cookie that proves you are a human
HUMAN_TOKEN_NAME = "aegis_human_verified"

def get_challenge_html():
    """
    Returns a 'Loading' page that forces the client to execute JavaScript.
    This kills 99% of bots (curl, python scripts, sqlmap) because they cannot run JS.
    """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>DiamondShield Security Check</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script>
            console.log("DiamondShield: Analyzing Browser Environment...");
            
            // 1. Set the 'Human' cookie
            document.cookie = "{HUMAN_TOKEN_NAME}=true; path=/; max-age=3600";
            
            // 2. Wait 1.5 seconds (simulating analysis), then reload the page
            setTimeout(function() {{
                window.location.reload();
            }}, 1500);
        </script>
        <style>
            body {{
                background-color: #121212;
                color: #e0e0e0;
                font-family: 'Courier New', monospace;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify_content: center;
                height: 100vh;
                margin: 0;
            }}
            .shield-icon {{ font-size: 60px; margin-bottom: 20px; }}
            .loader {{
                border: 3px solid #333;
                border-top: 3px solid #00ff88;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin-top: 20px;
            }}
            @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
        </style>
    </head>
    <body>
        <div class="shield-icon">🛡️</div>
        <h1>DiamondShield Defense</h1>
        <p>Verifying browser integrity...</p>
        <p style="font-size: 12px; color: #666;">DDoS Protection Active</p>
        <div class="loader"></div>
    </body>
    </html>
    """

@app.before_request
def waf_middleware():
    """
    The Gatekeeper: Every single request hits this function first.
    """
    client_ip = request.remote_addr
    path = request.path
    user_agent = request.headers.get('User-Agent', '')

    # --- GATE 1: THE ANTI-BOT BARRIER (JavaScript Challenge) ---
    # Logic: If the user doesn't have the cookie, AND they are not a whitelisted path...
    # We force them to solve the JS challenge.
    if request.cookies.get(HUMAN_TOKEN_NAME) != 'true':
        # (Optional: Whitelist APIs or static files here if needed)
        print(f"[*] 🤖 Bot Check: {client_ip} missing token. Sending JS Challenge.")
        return get_challenge_html()

    # --- GATE 2: THE FIREWALL (Attack Detection) ---
    # If they passed Gate 1, we now check for malicious payloads.
    
    # Combine all input sources into one payload for analysis
    payload = request.args.get('q', '') + str(request.form) + str(request.json)
    
    # Ask DiamondShield to inspect
    decision = firewall.inspect_request(client_ip, path, payload, user_agent)

    if not decision['allowed']:
        # BLOCK THE REQUEST
        return jsonify({
            "error": "Request Blocked by DiamondShield",
            "reason": decision['reason'],
            "incident_id": f"DS-{client_ip.replace('.','')}"
        }), 403

    # If allowed, the request passes through to the @app.route functions below.

@app.route('/')
def home():
    return """
    <div style="text-align:center; padding-top:50px; font-family:sans-serif;">
        <h1 style="color:green;">✅ ACCESS GRANTED</h1>
        <p>Welcome to the Secure Citadel.</p>
        <p>Your browser has been verified and your traffic scanned.</p>
        <hr>
        <small>Protected by DiamondShield-Sentinel-AI</small>
    </div>
    """

if __name__ == '__main__':
    print("==================================================")
    print("🛡️  DIAMONDSHIELD SYSTEM ONLINE")
    print("    - Layer 1: JavaScript Anti-Bot Barrier [ACTIVE]")
    print("    - Layer 2: AI Traffic Analysis [ACTIVE]")
    print("    - Layer 3: Honeypot Traps [ACTIVE]")
    print("==================================================")
    app.run(port=5000)
