"""Simple test script for the AWS Support Agent."""

from agent.support_agent import SupportAgent


def main() -> None:
    """Test the SupportAgent with simple interactions."""
    print("Initializing AWS Support Agent...")
    
    # Create the support agent
    agent = SupportAgent()
    
    print("Agent initialized! You can now ask questions about AWS.")
    print("Type 'quit' to exit.\n")
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Get agent response (SupportAgent is now a Strands Agent)
            print("Agent: Thinking...")
            result = agent(user_input)
            print(f"Agent: {str(result)}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
