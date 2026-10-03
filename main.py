from agent import run_agent

def main():
    print("=" * 50)
    print("🎓 Educator AI Agent")
    print("=" * 50)
    print("Commands: ask a question, request a quiz, or ask for a study plan")
    print("Type 'quit' to exit\n")

    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye! 👋")
            break
        
        try:
            response = run_agent(user_input)
            print(f"\n🤖 Agent:\n{response}\n")
            print("-" * 50)
        except Exception as e:
            print(f"❌ Error: {e}\n")

if __name__ == "__main__":
    main()