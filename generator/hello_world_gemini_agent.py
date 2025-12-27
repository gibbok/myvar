"""
Basic LangGraph agent that uses Gemini API to respond to a greeting.
"""
import os
from typing import TypedDict
from langgraph.graph import StateGraph, END


# Define the state structure
class AgentState(TypedDict):
    message: str
    response: str


def call_gemini(state: AgentState) -> AgentState:
    """
    Calls the Gemini API with a message and returns the response.
    """
    from google import genai
    
    # Get API key from environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    
    # Create client
    client = genai.Client(api_key=api_key)
    
    # Generate response
    response = client.models.generate_content(
        model='gemini-3-flash-preview',
        contents=state["message"]
    )
    
    # Update state with response
    return {
        "message": state["message"],
        "response": response.text
    }


def create_agent():
    """
    Creates and returns a LangGraph agent.
    """
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add the node
    workflow.add_node("gemini", call_gemini)
    
    # Set entry point
    workflow.set_entry_point("gemini")
    
    # Add edge to end
    workflow.add_edge("gemini", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app


def main():
    """
    Main function to run the agent.
    """
    # Create the agent
    agent = create_agent()
    
    # Initial state with greeting
    initial_state = {
        "message": "How are you?",
        "response": ""
    }
    
    # Run the agent
    result = agent.invoke(initial_state)
    
    # Print the results
    print(f"Question: {result['message']}")
    print(f"Response: {result['response']}")
    
    return result


if __name__ == "__main__":
    main()
