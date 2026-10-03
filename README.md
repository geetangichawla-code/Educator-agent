# Educator AI Agent

A Flask-based AI chat assistant built for learning and education. Features user authentication, persistent multi-conversation history, intent classification, and voice input/output.

## Features

- AI-powered chat — ask curriculum questions, request quizzes, or get study plans
- Intent routing — classifies each message before sending it to the agent
- Multi-conversation history — all chats saved per user, switchable from the sidebar
- Voice input — speak your message via the Web Speech API
- Voice output — AI replies are read aloud (toggle on/off)
- Auth system — sign up, log in, sessions, hashed passwords

## Setup

### 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/educator-agent.git
cd educator-agent

### 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Create your .env file
Copy .env.example to .env and fill in your values:
FLASK_SECRET_KEY=your_random_secret_here
ANTHROPIC_API_KEY=your_api_key_here

Generate a secret key with:
python -c "import secrets; print(secrets.token_hex(32))"

### 5. Run the app
python app.py

Open http://127.0.0.1:5000 in your browser.

## Tech Stack

- Backend: Python, Flask, SQLite
- AI: Groq + LangChain + LangGraph
- Frontend: Vanilla JS, Web Speech API, marked.js
