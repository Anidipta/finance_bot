import asyncio
from model import process_chat

async def main():
    print("AI Finance Assistant - Interactive Test Console")
    print("Type 'exit' to quit the program.")
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check for exit condition
            if user_input.lower() == 'exit':
                print("Exiting the AI Assistant...")
                break
            
            # Process the chat message
            if user_input:
                print("\nAI: Processing your request...", flush=True)
                intent,response = await process_chat(user_input)
                
                print("\nAI: Intent:", intent)
                print("\nAI:", response)
        
        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting...")
            break
        
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())