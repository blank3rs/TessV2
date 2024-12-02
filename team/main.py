import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from swarm import Swarm
from team.agents.agent_definitions import current_agent, agents

# Load environment variables from .env file
load_dotenv()

# First create the Azure OpenAI client
azure_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Initialize Swarm with the Azure OpenAI client
client = Swarm(
    client=azure_client
)

def chat():
    global current_agent
    print("Chat started. Type 'quit' to exit.")
    print(f"Currently talking to: {current_agent.agent.name}")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'quit':
            break
            
        current_agent.add_to_memory({"role": "user", "content": user_input})
        
        response = client.run(
            agent=current_agent.agent,
            messages=current_agent.get_memory()
        )
        
        # Handle function calls
        if hasattr(response, 'function_calls') and response.function_calls:
            for func_call in response.function_calls:
                func_name = func_call.name
                func_args = func_call.arguments if hasattr(func_call, 'arguments') else {}
                # Execute the function with its arguments
                if func_name in globals():
                    result = globals()[func_name](**func_args)
                    # Add function response to memory
                    current_agent.add_to_memory({
                        "role": "function",
                        "name": func_name,
                        "content": str(result)
                    })
        
        # Update current agent's memory with final response
        if response.messages:
            current_agent.memory = response.messages
        
        # Print the assistant's response
        print(f"\n{current_agent.agent.name}: {response.messages[-1]['content']}")

if __name__ == "__main__":
    chat() 