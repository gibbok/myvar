# LangGraph Hello World Application

A simple Python project demonstrating LangGraph 1.0.5 functionality with a basic state graph workflow.

## Project Setup

This project uses `uv` for Python package management and includes:
- **Python**: 3.13.7
- **LangGraph**: 1.0.5

## What This Application Does

This is a simple "Hello World" application that demonstrates LangGraph's core concepts:

1. **State Management**: Uses a `TypedDict` to define the application state with `message` and `count` fields
2. **Graph Nodes**: Two processing nodes that transform the state:
   - `hello_node`: Adds a greeting to the message
   - `world_node`: Adds a welcome message
3. **Graph Flow**: Defines a linear workflow: `hello → world → END`

## How to Run

### Option 1: Using `uv run` (Recommended)
```bash
cd /Users/gibbok/Documents/repos/myvar/generator
uv run main.py
```

### Option 2: Using the virtual environment directly
```bash
cd /Users/gibbok/Documents/repos/myvar/generator
source .venv/bin/activate
python main.py
```

## Expected Output

```
============================================================
LangGraph Hello World Application (v1.0.5)
============================================================

Initial State:
  Message: LangGraph User
  Count: 0

Executing graph...

Hello Node: Processing message 'LangGraph User'
World Node: Processing message 'Hello, LangGraph User!'

============================================================
Final Result:
  Message: Hello, LangGraph User! Welcome to LangGraph!
  Count: 2
============================================================
```

## Project Structure

```
generator/
├── .python-version    # Python version specification
├── .venv/            # Virtual environment (created by uv)
├── main.py           # Main application code
├── pyproject.toml    # Project dependencies and metadata
├── uv.lock           # Locked dependency versions
└── README.md         # This file
```

## Key LangGraph Concepts Demonstrated

- **StateGraph**: The main graph structure that manages workflow
- **Nodes**: Functions that process and transform state
- **Edges**: Define the flow between nodes
- **State**: TypedDict-based state management
- **Compilation**: Converting the graph definition into an executable application

## Dependencies

All dependencies are managed via `uv` and defined in `pyproject.toml`. Main dependencies include:
- `langgraph==1.0.5` - The main LangGraph library
- `langchain-core` - Core LangChain functionality
- `langgraph-checkpoint` - Checkpointing support
- Plus various supporting libraries

## Modifying the Application

To customize the workflow:
1. Modify the `State` TypedDict to add/remove state fields
2. Create new node functions that process the state
3. Add nodes to the workflow using `workflow.add_node()`
4. Define the flow using `workflow.add_edge()` or conditional edges
5. Run with `uv run main.py`
