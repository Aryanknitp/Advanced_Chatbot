# Advanced Chatbot Web Application

A lightweight, responsive web application featuring an AI-driven chatbot built with Flask and powered by Google Gemini. The application includes dynamic front-end interactions and a session-based rolling memory container that allows the model to retain conversational context during active sessions.

## 🚀 Key Features

*   **Google Gemini Integration:** Powered by the fast and highly efficient `gemini-2.5-flash` model via an OpenAI-compatible API interface.
*   **Active Session Memory:** Remembers user inputs (e.g., names, preferences) using encrypted Flask browser sessions.
*   **Automated Clean Text Outputs:** Custom processing layer removes Markdown bolding, heading markers, and bullet strings for clean UI delivery.
*   **Fully Responsive Web Interface:** Clean HTML/CSS construction optimized for both desktop and mobile client access.
*   **Secure Credential Handling:** Decoupled environmental variable management using `python-dotenv`.

---

## 📂 Project Architecture

```text
CHATBOT/
├── __pycache__/        # Compiled Python runtime bytecode cache files
├── .venv/               # Isolated virtual environment dependencies
├── static/              # Client-side UI stylesheet and logic layers
│   ├── script.js        # Asynchronous API fetch execution script
│   └── style.css        # Custom UI presentation configuration file
├── templates/
│   └── index.html       # Primary application front-end landing view
├── .env                 # Protected environment key configurations
├── .gitignore           # Filter patterns preventing credential leaks
├── app.py               # Main Flask web framework orchestration module
├── chatbot.py           # Core algorithmic API communication pipeline
├── intents.json         # Structured local dataset for targeted classification
└── requirements.txt     # Complete Python package dependency registry
```

---

## 🛠️ Step-by-Step Installation & Setup

Follow these precise initialization steps to deploy the application on your local machine:

### 1. Clone the Codebase
```bash
git clone https://github.com/Aryanknitp/Advanced_Chatbot.git
cd Advanced_Chatbot
```

### 2. Configure Your Virtual Environment
Create and initialize an isolated workspace dependency folder:
```bash
# For Windows environments
python -m venv .venv
.venv\Scripts\activate

# For macOS / Linux environments
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Package Prerequisites
Install all core system packages using the project dependency registry:
```bash
pip install -r requirements.txt
```

### 4. Inject Environment Credentials
Generate a file named `.env` inside your primary workspace folder root. Register for a free API key inside **[Google AI Studio](https://google.com)** and append it to the configuration:
```env
GEMINI_API_KEY=your_actual_free_gemini_api_key_here
```

### 5. Launch the Local Application Server
Execute the main server launch script via your active terminal session:
```bash
python app.py
```
Open your preferred browser client and navigate directly to **`http://127.0.0.1:5000`** to begin chatting with the conversational engine.

---

## ⚙️ How the Engine Functions

### Context Retention Logic
Every user prompt sent to the server route `/chat` updates a session-level state list array. This structure is packaged together with localized system directives and dispatched directly to the Google endpoint using an OpenAI compatibility layer structure:

```python
# Extracting history arrays securely from the browser session context
history = session["chat_history"]
history.append({"role": "user", "content": user_message})

# Transmitting full payload context arrays down to Gemini
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[system_instruction] + history
)
```

### Markdown Text Stripping Functionality
Before the final model text outputs hit the client browser window view, regex filtering operations intercept and remove raw Markdown syntax components:
```python
text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)   # Strips bold asterisks
text = re.sub(r"###|##|#", "", text)           # Strips hash headings
text = re.sub(r"- ", "", text)                 # Strips bullet fragment symbols
```

---

## 📝 Technical Dependencies

*   **Python 3.8+**
*   **Flask** - Micro web application routing core
*   **openai** - Official communication engine SDK wrapper
*   **python-dotenv** - System variable management security tool

---

## 📄 License

This software project is open-source and structured completely under the guidelines of the **MIT License**.
