import os
import re
from flask import Flask, request, jsonify
import nltk
from nltk.tokenize import word_tokenize
from openai import OpenAI

# Initialize the Flask application instance
app = Flask(__name__)

# Download the required NLTK punctuation data resource package safely
# Download the modern required NLTK tokenization packages safely
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)


# Use Groq's official OpenAI-compatible API endpoint.
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)


# def clean_text(text):
#     if not text:
#         return ""
#     # Strip markdown bolding asterisks, heading syntax, and bullet indicators
#     text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
#     text = re.sub(r"###|##|#", "", text)
#     text = re.sub(r"- ", "", text)
#     return text.strip()
def clean_text(text):
    if not text:
        return ""
    # Strip markdown bolding asterisks and heading syntax headers
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"###|##|#", "", text)
    return text.strip()


def process_tokens_with_nltk(text):
    """
    Demonstrates NLTK utility by tokenizing the final chatbot text.
    You can use this step to run safety filters, log word counts, or analyze sentiment.
    """
    if not text:
        return []
    return word_tokenize(text)

def get_response(user_input):
    try:
        # Request completion from Groq using official OpenAI compatibility patterns
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Flagship ultra-speed model on Groq's cloud infrastructure
            messages=[
                {
                    "role": "system",
                    # "content": (
                    #     "You are a helpful chatbot. "
                    #     "Reply in plain text only. "
                    #     "Do NOT use markdown, headings, bullet points, **, ###, or formatting symbols."
                    # )

                    # "content": (
                    #     "You are a helpful chatbot. "
                    #     "Always structure your answers point-by-point as a clean list. "
                    #     "Keep each point brief, direct, and actionable. "
                    #     "Do NOT use markdown bolding like **. Just use numbers or simple bullet dashes."
                    # )
                    "content": (
                        "You are a helpful chatbot assistant. "
                        "Always structure your answers point-by-point as a clean list using numerical bullets (1., 2., etc.). "
                        "When referencing websites, platforms, documentation, or links, ALWAYS provide them as standard markdown hyperlinks. "
                        "Example format: [Visit Google](https://google.com) "
                        "Do NOT write raw text URLs like 'google.com' or 'https://google.com'. Always wrap them in descriptive anchor names."
                    )
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )
        # CORRECTED: Fixed the python spacing indentation error and added standard choice selection
        raw_text = response.choices[0].message.content
        return clean_text(raw_text)
        
    except Exception as e:
        return f"Groq API Error: {str(e)}"

@app.route("/chat", methods=["POST"])
def chat_endpoint():
    """
    POST API Endpoint that expects a JSON payload matching format: {"message": "Your text here"}
    """
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field in requested JSON payload"}), 400
    
    user_message = data["message"]
    
    # Generate response from Groq architecture
    bot_reply = get_response(user_message)
    
    # Process text using NLTK functions
    tokenized_words = process_tokens_with_nltk(bot_reply)
    
    # Construct complete JSON response payload object
    return jsonify({
        "status": "success",
        "reply": bot_reply,
        "metrics": {
            "token_count": len(tokenized_words)
        }
    })

if __name__ == "__main__":
    # Ensure the environment variable is configured before executing startup
    if not os.environ.get("GROQ_API_KEY"):
        print("Warning: GROQ_API_KEY environment variable is not defined.")
    
    # Run server locally on default port 5000
    app.run(debug=True, port=5000)
