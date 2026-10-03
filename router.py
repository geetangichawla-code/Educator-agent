from llm_client import call_llm
def classify_intent(user_message: str) -> str:
    result = call_llm(
        system_prompt="""You are an intent classifier for an educational AI agent.
Classify the user's message into exactly one of these categories:
- quiz: user wants a quiz, test, or practice questions generated
- study_plan: user wants a study plan, schedule, or learning roadmap
- curriculum_qa: user has a question about a topic, concept, or subject

Respond with ONLY the category name, nothing else. No explanation, no punctuation.""",
        user_message=user_message
    )
    
    intent = result.strip().lower()
    
    # Fallback if model returns something unexpected
    if intent not in ["quiz", "study_plan", "curriculum_qa"]:
        intent = "curriculum_qa"
    
    return intent