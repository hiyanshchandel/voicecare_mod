from flask import Flask, request, jsonify
from chatbot_1 import get_response
from longterm_memory import summarise
from summary_upsertion import summary_upsert
import threading
from vectordb_upsertion import insert_data

app = Flask(__name__)

chat_histories = {}

def check_and_summarize(chat_history, username):
    """Summarize the last 2 messages and upsert into memory."""
    if len(chat_history) >= 2 and len(chat_history) % 2 == 0:
        summary = summarise(chat_history[-2:])
        summary_upsert(username, summary)

def summarize_in_background(chat_history, username):
    """Run summarization in a background thread safely."""
    chat_history_copy = chat_history[:]
    threading.Thread(target=check_and_summarize, args=(chat_history_copy, username), daemon=True).start()


@app.route("/voicecare-processing", methods=["POST"])
def voicecare_processing():
    try:
        data = request.json
        user_query = data.get("text")
        username = data.get("user_id")

        if not user_query or not username:
            return jsonify({"error": "Missing text or user_id"}), 400
        
        if username not in chat_histories:
            chat_histories[username] = []
        
        # Process the text (Placeholder for actual processing logic)
        response = get_response(user_query, username)
        chat_histories[username].append({"role": "user", "content": user_query})
        chat_histories[username].append({"role": "assistant", "content": response})
        
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
    app.run(host="0.0.0.0", port=5000, debug=True)
