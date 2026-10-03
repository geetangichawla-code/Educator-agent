from router import classify_intent
from educator_tools import answer_curriculum_question, generate_quiz, generate_study_plan

def run_agent(user_message: str, history: list = None) -> str:
    print(f"\nClassifying intent...")
    intent = classify_intent(user_message)
    print(f"Intent: {intent}")

    if intent == "quiz":
        topic = user_message
        print(f"Generating quiz on: {topic}")
        return generate_quiz(topic, history=history)

    elif intent == "study_plan":
        subject = user_message
        print(f"Generating study plan for: {subject}")
        return generate_study_plan(subject, history=history)

    elif intent == "curriculum_qa":
        print(f"Answering curriculum question...")
        return answer_curriculum_question(user_message, history=history)

    else:
        return "I'm not sure how to help with that. Try asking a question, requesting a quiz, or asking for a study plan."