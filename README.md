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

screenshots 
<img width="1917" height="857" alt="image" src="https://github.com/user-attachments/assets/dab45fd3-c503-4760-84a6-915ec0fdcc6b" />
<img width="1916" height="882" alt="image" src="https://github.com/user-attachments/assets/f15ef86e-8590-49b6-ba30-35c710984740" />
<img width="1915" height="856" alt="image" src="https://github.com/user-attachments/assets/1711a65d-7417-4346-96b6-13387cb8d395" />
<img width="1912" height="866" alt="image" src="https://github.com/user-attachments/assets/36c92e47-8c6b-4c43-8806-cfaff8208ff9" />





## Tech Stack

- Backend: Python, Flask, SQLite
- AI: Groq + LangChain + LangGraph
- Frontend: Vanilla JS, Web Speech API, marked.js
