from flask import Flask, request, jsonify
from chatbot_1 import get_response
from longterm_memory import summarise
from summary_upsertion import summary_upsert
import threading
from vectordb_upsertion import insert_data
import os
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
chat_histories = {}
# Configure CORS with specific settings
CORS(app, supports_credentials=True)

#chat_histories = {}
def check_and_summarize(chat_history, username):
    """Summarize the last 2 messages and upsert into memory."""
    if len(chat_history) >= 2 and len(chat_history) % 2 == 0:
        summary = summarise(chat_history[-2:])
        summary_upsert(username, summary)

def summarize_in_background(chat_history, username):
    """Run summarization in a background thread safely."""
    chat_history_copy = chat_history[:]
    threading.Thread(target=check_and_summarize, args=(chat_history_copy, username), daemon=True).start()

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


# Handle preflight OPTIONS requests
@app.route("/voicecare-form", methods=["OPTIONS"])
@app.route("/voicecare-processing", methods=["OPTIONS"])
def handle_options():
    response = jsonify({"message": "OK"})
    origin = request.headers.get('Origin')
    if origin in ["https://voicecare-ten.vercel.app", "http://localhost:5173"]:
        response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Max-Age"] = "3600"
    return response

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
            if username not in chat_histories:
                chat_histories[username] = []  # Initialize if not present


            chat_histories[username].append({"role": "user", "content": user_query})
            chat_histories[username].append({"role": "assistant", "content": response})
            summarize_in_background(chat_histories[username], username)
            return jsonify({"response": response}), 200
        except Exception as e:
            return jsonify({"error": f"Chatbot processing failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/voicecare-form", methods=["POST"])
def voicecare_form():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        insert_data(data)
        return jsonify({"form_flag": "form_done"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4000))
    debug_mode = os.environ.get("DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
