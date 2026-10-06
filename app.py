from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import database
import documents
from agent import run_agent
from router import classify_intent
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # reject uploads over 5 MB
MAX_DOC_CHARS = 8000  # keeps requests small; longer documents are cut
app.secret_key = os.getenv("FLASK_SECRET_KEY")
if not app.secret_key:
    raise ValueError("FLASK_SECRET_KEY not found in .env file")

database.init_db()

MAX_HISTORY_MESSAGES = 6  # last 3 user+assistant turns given to the model as context


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


@app.route("/")
@login_required
def index():
    return render_template(
        "index.html",
        username=session["username"],
        conversation_id=session.get("conversation_id", "")
    )


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]
        if len(password) < 6:
            return render_template("signup.html", error="Password must be at least 6 characters")
        ok, msg = database.create_user(username, email, password)
        if ok:
            return redirect(url_for("login"))
        return render_template("signup.html", error=msg)
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = database.verify_user(request.form["username"].strip(), request.form["password"])
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["conversation_id"] = (
                database.get_latest_conversation_id(user["id"])
                or database.new_conversation_id()
            )
            return redirect(url_for("index"))
        return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/chat", methods=["POST"])
@login_required
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"response": "Please enter a message."})

    uid = session["user_id"]
    conv_id = session["conversation_id"]

    # Pull recent context BEFORE saving this turn, so the current message isn't duplicated
    prior_rows = database.get_chat_history(uid, conv_id)
    history = [
        {"role": row["role"], "content": row["message"]}
        for row in prior_rows[-MAX_HISTORY_MESSAGES:]
    ]

    database.save_message(uid, conv_id, "user", user_message)

    intent = classify_intent(user_message)
    doc = database.get_document(uid, conv_id)
    context = doc["content"] if doc else None
    response = run_agent(user_message, history=history, context=context)

    database.save_message(uid, conv_id, "assistant", response, intent)
    return jsonify({"response": response})


@app.route("/history")
@login_required
def history():
    rows = database.get_chat_history(session["user_id"], session["conversation_id"])
    return jsonify([dict(r) for r in rows])


@app.route("/conversations")
@login_required
def conversations():
    rows = database.get_conversations(session["user_id"])
    return jsonify([dict(r) for r in rows])


@app.route("/switch_chat", methods=["POST"])
@login_required
def switch_chat():
    data = request.get_json()
    conv_id = data.get("conversation_id")
    if not conv_id:
        return jsonify({"error": "Missing conversation_id"}), 400
    session["conversation_id"] = conv_id
    return jsonify({"status": "ok"})


@app.route("/new_chat", methods=["POST"])
@login_required
def new_chat():
    new_id = database.new_conversation_id()
    session["conversation_id"] = new_id
    return jsonify({"conversation_id": new_id})
@app.route("/delete_chat", methods=["POST"])
@login_required
def delete_chat():
    data = request.get_json()
    conv_id = data.get("conversation_id")
    if not conv_id:
        return jsonify({"error": "Missing conversation_id"}), 400

    uid = session["user_id"]
    database.delete_conversation(uid, conv_id)

    # If the user deleted the chat they were viewing, move them to another one
    if session.get("conversation_id") == conv_id:
        session["conversation_id"] = (
            database.get_latest_conversation_id(uid)
            or database.new_conversation_id()
        )

    return jsonify({"status": "ok", "conversation_id": session["conversation_id"]})
@app.route("/rename_chat", methods=["POST"])
@login_required
def rename_chat():
    data = request.get_json()
    conv_id = data.get("conversation_id")
    title = (data.get("title") or "").strip()[:80]
    if not conv_id or not title:
        return jsonify({"error": "Missing conversation_id or title"}), 400
    if not database.rename_conversation(session["user_id"], conv_id, title):
        return jsonify({"error": "Chat not found"}), 404
    return jsonify({"status": "ok"})
@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File too large (max 5 MB)."}), 413


@app.route("/upload", methods=["POST"])
@login_required
def upload():
    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify({"error": "No file selected."}), 400
    if documents.extension_of(file.filename) not in documents.ALLOWED_EXTENSIONS:
        return jsonify({"error": "Only PDF, DOCX and TXT files are supported."}), 400

    try:
        text = documents.extract_text(file.filename, file.read())
    except Exception:
        return jsonify({"error": "Could not read that file."}), 400
    if not text:
        return jsonify({"error": "No readable text found (is it a scanned PDF?)."}), 400

    truncated = len(text) > MAX_DOC_CHARS
    database.save_document(session["user_id"], session["conversation_id"],
                           file.filename, text[:MAX_DOC_CHARS])
    return jsonify({"status": "ok", "filename": file.filename, "truncated": truncated})
if __name__ == "__main__":
    app.run(debug=True, port=5000)