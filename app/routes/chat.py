from flask import Blueprint, request, jsonify, session
from app.logic.nlp import detect_intent, resolve_context
from app.logic.handlers import (
    handle_timetable, handle_syllabus, handle_faculty,
    handle_exam, handle_greeting, handle_farewell, handle_help,
)
from app.logic.ai_handler import get_ai_response
from app.models.models import ChatHistory
from app import db
from functools import wraps
import uuid

chat_bp = Blueprint("chat", __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify({"error": "unauthorized", "message": "Please login to use the chatbot."}), 401
        return f(*args, **kwargs)
    return decorated


def get_or_create_session():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    if "context" not in session:
        session["context"] = {}
    if "history" not in session:
        session["history"] = []
    return session["session_id"]


@chat_bp.route("/chat", methods=["POST"])
@login_required
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    session_id = get_or_create_session()
    context = session.get("context", {})

    if "branch" in data:
        context["branch"] = data["branch"]
    if "year" in data:
        context["year"] = int(data["year"])

    follow_up_intent = resolve_context(user_message, context)
    intent = follow_up_intent or detect_intent(user_message)

    db_response = ""
    extra_context = {}

    if intent == "timetable":
        db_response, extra_context = handle_timetable(user_message, context)
    elif intent == "syllabus":
        db_response, extra_context = handle_syllabus(user_message, context)
    elif intent == "faculty":
        db_response, extra_context = handle_faculty(user_message, context)
    elif intent == "exam":
        db_response, extra_context = handle_exam(user_message, context)
    elif intent == "greeting":
        db_response, extra_context = handle_greeting()
    elif intent == "farewell":
        db_response, extra_context = handle_farewell()
    elif intent == "help":
        db_response, extra_context = handle_help()
    else:
        db_response = ("🤔 I'm not sure about that. Try asking about:\n"
                       "  • Timetable\n  • Syllabus\n  • Faculty\n  • Exam Schedule\n\n"
                       "Type <b>help</b> for more options.")

    ai_reply = get_ai_response(user_message, context, db_response)
    final_response = ai_reply if ai_reply else db_response

    context.update(extra_context)
    context["last_intent"] = intent
    session["context"] = context
    session.modified = True

    history_entry_user = ChatHistory(session_id=session_id, role="user", message=user_message)
    history_entry_bot = ChatHistory(session_id=session_id, role="bot", message=final_response)
    db.session.add(history_entry_user)
    db.session.add(history_entry_bot)
    db.session.commit()

    return jsonify({
        "response": final_response,
        "intent": intent,
        "context": {"branch": context.get("branch"), "year": context.get("year")},
    })


@chat_bp.route("/chat/history", methods=["GET"])
@login_required
def get_history():
    session_id = session.get("session_id")
    if not session_id:
        return jsonify({"history": []})
    records = ChatHistory.query.filter_by(session_id=session_id).order_by(ChatHistory.timestamp).all()
    return jsonify({"history": [{"role": r.role, "message": r.message} for r in records]})


@chat_bp.route("/chat/clear", methods=["POST"])
@login_required
def clear_chat():
    session_id = session.get("session_id")
    if session_id:
        ChatHistory.query.filter_by(session_id=session_id).delete()
        db.session.commit()
    session.pop("history", None)
    session.pop("context", None)
    return jsonify({"status": "cleared"})
