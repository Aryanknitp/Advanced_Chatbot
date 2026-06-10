import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables before importing the chatbot logic.
load_dotenv()

# Import your core automated text processing blocks safely
from chatbot import get_response, process_tokens_with_nltk

app = Flask(__name__)

@app.route("/")
def home():
    """
    Renders your newly updated interactive index.html workspace webpage interface.
    """
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """
    POST API Endpoint that expects a JSON payload matching format: {"message": "Your text here"}
    """
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"status": "error", "error": "Missing 'message' field in requested JSON payload"}), 400
    
    user_message = data["message"]
    
    # Generate the clean plain-text response from your Groq architecture
    bot_reply = get_response(user_message)
    
    # Run NLTK tokenization metrics on the bot's response string
    tokenized_words = process_tokens_with_nltk(bot_reply)
    
    # Construct complete JSON response payload object to match your Javascript structure
    return jsonify({
        "status": "success",
        "reply": bot_reply,
        "metrics": {
            "token_count": len(tokenized_words)
        }
    })

if __name__ == "__main__":
    # Safety Check: Warn the developer if they forgot to paste their key inside the .env file
    if not os.getenv("GROQ_API_KEY"):
        print("\n[WARNING] GROQ_API_KEY is missing from your .env file environment configurations!\n")
        
    # Run the Flask app on a reliable local port.
    app.run(debug=True, host="127.0.0.1", port=5000)
