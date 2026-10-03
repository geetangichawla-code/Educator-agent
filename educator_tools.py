from llm_client import call_llm

def answer_curriculum_question(question: str, history: list = None) -> str:
    return call_llm(
        system_prompt="""You are an expert educator assistant.
Answer curriculum questions clearly and concisely for teachers and students.""",
        user_message=question,
        history=history
    )

def generate_quiz(topic: str, num_questions: int = 5, history: list = None) -> str:
    return call_llm(
        system_prompt="""You are a quiz generator for educators.
Generate multiple choice questions with 4 options each.
Clearly mark the correct answer at the end of each question.""",
        user_message=f"Generate {num_questions} multiple choice questions about: {topic}",
        history=history
    )

def generate_study_plan(subject: str, duration_weeks: int = 4, history: list = None) -> str:
    return call_llm(
        system_prompt="""You are a personalised study plan creator.
Create structured, week-by-week study plans that are realistic and actionable.""",
        user_message=f"Create a {duration_weeks}-week study plan for: {subject}",
        history=history
    )