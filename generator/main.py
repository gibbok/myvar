"""
Simple LangGraph Hello World Application
This demonstrates a basic LangGraph workflow with state management.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END


# Define the state structure
class State(TypedDict):
    message: str
    count: int


# Define node functions
def hello_node(state: State) -> State:
    """First node that adds a greeting"""
    print(f"Hello Node: Processing message '{state['message']}'")
    state["message"] = f"Hello, {state['message']}!"
    state["count"] = state.get("count", 0) + 1
    return state


def world_node(state: State) -> State:
    """Second node that adds more to the message"""
    print(f"World Node: Processing message '{state['message']}'")
    state["message"] = f"{state['message']} Welcome to LangGraph!"
    state["count"] = state.get("count", 0) + 1
    return state


def main():
    """Main function to create and run the LangGraph workflow"""
    print("=" * 60)
    print("LangGraph Hello World Application (v1.0.5)")
    print("=" * 60)
    
    # Create the graph
    workflow = StateGraph(State)
    
    # Add nodes to the graph
    workflow.add_node("hello", hello_node)
    workflow.add_node("world", world_node)
    
    # Define the flow: hello -> world -> END
    workflow.set_entry_point("hello")
    workflow.add_edge("hello", "world")
    workflow.add_edge("world", END)
    
    # Compile the graph
    app = workflow.compile()
    
    # Run the graph with initial state
    initial_state = {
        "message": "LangGraph User",
        "count": 0
    }
    
    print("\nInitial State:")
    print(f"  Message: {initial_state['message']}")
    print(f"  Count: {initial_state['count']}")
    print("\nExecuting graph...\n")
    
    # Execute the graph
    result = app.invoke(initial_state)
    
    print("\n" + "=" * 60)
    print("Final Result:")
    print(f"  Message: {result['message']}")
    print(f"  Count: {result['count']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
