from flask import Flask, request, jsonify
import os

app = Flask(__name__)

DEVELOPER_NAME = "Satyam Pandey"
# Security ke liye token aap Render ki Environment Variables se bhi read kar sakte hain
VALID_TOKEN = os.getenv("SECRET_TOKEN", "my_secret_secure_token_123")

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Message Server",
        "developer": DEVELOPER_NAME,
        "status": "Running on Render"
    })

@app.route('/send-message', methods=['POST'])
def send_message():
    auth_token = request.headers.get('Authorization')
    
    if not auth_token:
        return jsonify({"error": "Missing token!"}), 401
    
    if auth_token.startswith("Bearer "):
        auth_token = auth_token.split(" ")[1]

    if auth_token != VALID_TOKEN:
        return jsonify({"error": "Invalid token!"}), 403

    data = request.get_json()
    if not data or 'message' not in data or 'receiver' not in data:
        return jsonify({"error": "Please provide 'receiver' and 'message' in JSON body."}), 400

    receiver = data.get('receiver')
    message_body = data.get('message')

    print(f"[{DEVELOPER_NAME}'s Server] Sending message to {receiver}: {message_body}")

    return jsonify({
        "status": "Success",
        "sender_server_by": DEVELOPER_NAME,
        "details": f"Message successfully sent to {receiver}"
    }), 200

if __name__ == '__main__':
    # Render port dynamic allocate karta hai, isliye os.environ.get use kiya hai
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
