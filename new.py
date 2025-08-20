from flask import Flask, request, jsonify
import string
import random
import requests

app = Flask(__name__)

url = {}

# random shortcode
def generate(length=5):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to  URL!"})

@app.route('/shorturls', methods=['POST'])
def create_short_url():
    data = request.get_json()
    original = data.get('url')
    validity = data.get('validity', 30)  
    shortcode = data.get('shortcode', generate())

    # URL mapping
    url[shortcode] = {
        'original_url': original,
        'validity': validity
    }

    # Return output type
    return jsonify({
        'shortcode': shortcode,
        'short_url': f"http://localhost:5000/{shortcode}",
        'original_url': original,
        'validity': validity
    }), 201

@app.route('/shorturls', methods=['GET'])
def list():
    return jsonify(url)

# endpoint
@app.route('/<shortcode>', methods=['GET'])
def redirect_url(shortcode):
    if shortcode in url:
        return jsonify(url[shortcode])  # For demo
    else:
        return jsonify({'error': 'Shortcode not found'}), 404

# endpoint 
@app.route('/register', methods=['POST'])
def register_remote():
    remote_url = "http://20.244.56.144/evaluation-service/register"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJyYXRoZXNoYTQ4QGdtYWlsLmNvbSIsImV4cCI6MTc1NTY3MDAwMSwiaWF0IjoxNzU1NjY5MTAxLCJpc3MiOiJBZmZvcmQgTWVkaWNhbCBUZWNobm9sb2dpZXMgUHJpdmF0ZSBMaW1pdGVkIiwianRpIjoiYzEwZjAxZTQtNTZmOC00YWZhLTg2ODgtMzI2NjQ0ZmRmYjdlIiwibG9jYWxlIjoiZW4tSU4iLCJuYW1lIjoicmF0aGVzaGEgc20iLCJzdWIiOiIxNDIxMTFhZi1kMzlkLTRhNTctYjljMS03NWIzNzJkYWQ1YzQifSwiZW1haWwiOiJyYXRoZXNoYTQ4QGdtYWlsLmNvbSIsIm5hbWUiOiJyYXRoZXNoYSBzbSIsInJvbGxObyI6IjIyMTcwMTciLCJhY2Nlc3NDb2RlIjoieHNaVFRuIiwiY2xpZW50SUQiOiIxNDIxMTFhZi1kMzlkLTRhNTctYjljMS03NWIzNzJkYWQ1YzQiLCJjbGllbnRTZWNyZXQiOiJoV3RRR2F5d3hmWVdGcFBmIn0.YU9ytfgU7ceGHKOqSAXzwNsxACoc2fGlFAYcE3bYX-M"
    }

    # JSON 
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "No JSON body provided"}), 400

    # boolean(Flase/True)
    for key, value in payload.items():
        if isinstance(value, str):
            if value.lower() == "true":
                payload[key] = True
            elif value.lower() == "false":
                payload[key] = False

    # Send  API
    try:
        response = requests.post(remote_url, headers=headers, json=payload, timeout=10)
        try:
            resp_json = response.json()
        except Exception:
            resp_json = response.text

        return jsonify({
            "status_code": response.status_code,
            "response": resp_json
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)