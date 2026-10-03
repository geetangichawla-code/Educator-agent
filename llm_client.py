# llm_client.py - Groq LLM client

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file")
    return Groq(api_key=api_key)

def call_llm(system_prompt: str, user_message: str, temperature: float = 0.7, history: list = None) -> str:
    """
    Core LLM call function - used by all tools.
    This is the single point of contact with the LLM.

    history: optional list of prior turns, e.g.
             [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
             Inserted between the system prompt and the current user message so the
             model has conversational context.
    """
    client = get_groq_client()

    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        temperature=temperature,
        max_tokens=1024
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    print("Testing Groq connection...")
    result = call_llm(
        system_prompt="You are a helpful assistant.",
        user_message="Say hello in one sentence."
    )
    print("Response:", result)
    print("Groq connection successful!")