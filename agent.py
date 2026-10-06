from router import classify_intent
from educator_tools import answer_curriculum_question, generate_quiz, generate_study_plan


def run_agent(user_message: str, history: list = None, context: str = None):
    """Returns (reply, intent) so callers don't need to classify again."""
    print(f"\nClassifying intent...")
    intent = classify_intent(user_message)   # classify the ORIGINAL short message
    print(f"Intent: {intent}")

    if context:
        user_message = (
            "Use the following document as your source material. "
            "Base your answer on it, and say so if the document doesn't cover the request.\n\n"
            f"--- DOCUMENT START ---\n{context}\n--- DOCUMENT END ---\n\n"
            f"Request: {user_message}"
        )

    if intent == "quiz":
        print(f"Generating quiz...")
        return generate_quiz(user_message, history=history), intent

    elif intent == "study_plan":
        print(f"Generating study plan...")
        return generate_study_plan(user_message, history=history), intent

    elif intent == "curriculum_qa":
        print(f"Answering curriculum question...")
        return answer_curriculum_question(user_message, history=history), intent

    else:
        return (
            "I'm not sure how to help with that. Try asking a question, requesting a quiz, or asking for a study plan.",
            intent,
        )