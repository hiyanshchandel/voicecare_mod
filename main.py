from flask import Flask, request, jsonify
from chatbot_1 import get_response
from longterm_memory import summarise
from summary_upsertion import summary_upsert
import threading
from vectordb_upsertion import insert_data
import os

app = Flask(__name__)

from collections import defaultdict
chat_histories = defaultdict(list)  # Thread-safe initialization

def check_and_summarize(chat_history, username):
    """Summarize the last 2 messages and upsert into memory."""
    try:
        if len(chat_history) >= 2 and len(chat_history) % 2 == 0:
            summary = summarise(chat_history[-2:])
            summary_upsert(username, summary)
    except Exception as e:
        print(f"Summarization error for {username}: {str(e)}")  # Logging

def summarize_in_background(chat_history, username):
    """Run summarization in a background thread safely."""
    chat_history_copy = chat_history[:]
    thread = threading.Thread(target=check_and_summarize, args=(chat_history_copy, username), daemon=True)
    thread.start()

@app.route("/voicecare-processing", methods=["POST"])
def voicecare_processing():
    try:
        data = request.json
        user_query = data.get("text")
        username = data.get("user_id")

        if not user_query or not username:
            return jsonify({"error": "Missing text or user_id"}), 400

        # Process the text safely
        try:
            response = get_response(user_query, username)
        except Exception as e:
            return jsonify({"error": f"Chatbot processing failed: {str(e)}"}), 500

        # Update chat history
        chat_histories[username].append({"role": "user", "content": user_query})
        chat_histories[username].append({"role": "assistant", "content": response})

        # Background summarization
        summarize_in_background(chat_histories[username], username)

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
