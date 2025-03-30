from flask import Flask, request, jsonify
from chatbot_1 import get_response
from longterm_memory import summarise
from summary_upsertion import summary_upsert
import threading
from vectordb_upsertion import insert_data
import os
from flask_cors import CORS

app = Flask(__name__)

# Allow localhost (for development) and production frontend
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

# Handle preflight OPTIONS requests
@app.route("/voicecare-form", methods=["OPTIONS"])
@app.route("/voicecare-processing", methods=["OPTIONS"])
def handle_options():
    return '', 204

@app.route("/voicecare-processing", methods=["POST"])
def voicecare_processing():
    try:
        data = request.json
        user_query = data.get("text")
        username = data.get("user_id")

        if not user_query or not username:
            return jsonify({"error": "Missing text or user_id"}), 400

        try:
            response = get_response(user_query, username)
        except Exception as e:
            return jsonify({"error": f"Chatbot processing failed: {str(e)}"}), 500

        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/voicecare-form", methods=["POST"])
def voicecare_form():
    try:
        data = request.json
        insert_data(data)
        return jsonify({"form_flag": "form_done"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
