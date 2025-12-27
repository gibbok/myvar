"""
Multi-Agent Content Generation System with Gemini AI
Orchestrates Generator, Reviewer, and Publisher agents.
"""

import os, re
from datetime import datetime, timedelta
from pathlib import Path
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# Config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
BASE_DIR = Path(__file__).parent.parent.absolute()
OUTPUT_CONTENT_DIR = BASE_DIR / "website/content"
INPUT_CONTENT_DRAFT= BASE_DIR / "generator/drafts/content.md"

# Helpers
def get_llm(temp=0.7):
    """Initialize the Gemini LLM with a specific temperature."""
    return ChatGoogleGenerativeAI(model=GEMINI_MODEL, api_key=GEMINI_API_KEY, temperature=temp)

def ensure_str(content) -> str:
    """Safely convert LLM response content to a flat string."""
    if isinstance(content, list):
        return "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)
    return str(content)

def read_prompt(name: str) -> str:
    """Read a prompt template from an external text file."""
    return (Path(__file__).parent / f"prompt_{name}.txt").read_text()

class AgentState(TypedDict):
    """The shared state passed between agents in the graph."""
    content: str
    feedback: str
    count: int
    approved: bool
    title: str
    meta: dict

def slugify(text: str) -> str:
    """Convert text to an SEO-friendly URL slug."""
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9\s-]', '', text.lower()).replace(' ', '-')).strip('-')

# Agent Nodes
def generator_node(state: AgentState):
    """Generates or refines the technical article based on input or feedback."""
    print(f"🤖 Generator - Iteration {state['count']}")
    llm = get_llm(0.7)
    
    prompt = read_prompt("generator").format(
        content=state['content'],
        feedback=state['feedback'] if state['feedback'] else 'None (First run)'
    )
    
    res = ensure_str(llm.invoke(prompt).content)
    state['content'] = res
    if state['count'] == 1:
        state['title'] = res.strip().split('\n')[0].replace('#', '').strip()[:100]
    return state

def reviewer_node(state: AgentState):
    """Reviews the content and decides whether to approve or request revisions."""
    print(f"🔍 Reviewer - Iteration {state['count']}")
    llm = get_llm(0.1)
    
    prompt = read_prompt("reviewer").format(content=state['content'])
    
    res = ensure_str(llm.invoke(prompt).content)
    decision = 'APPROVE' if 'DECISION: APPROVE' in res.upper() else 'REVISE'
    feedback = res.split('FEEDBACK:')[-1].strip() if 'FEEDBACK:' in res else ""
    
    if state['count'] >= 4: decision = 'APPROVE' # Force exit to prevent hanging/loops
    
    state.update({"approved": decision == 'APPROVE', "feedback": feedback})
    if not state['approved']: state['count'] += 1
    return state

def publisher_node(state: AgentState):
    """Extracts metadata, formats the article with front-matter, and saves it to disk."""
    print("📤 Publisher - Finalizing...")
    llm = get_llm(0.1)
    prompt = read_prompt("publisher").format(content=state['content'][:2000])
    res = ensure_str(llm.invoke(prompt).content)
    
    # Simple extraction
    title_raw = re.search(r'TITLE:\s*(.*)', res, re.I).group(1).strip() if 'TITLE:' in res else state['title']
    title = re.split(r'\s*[|]\s*|TOPIC:|TAGS:', title_raw, flags=re.I)[0].strip()
    
    topic = re.search(r'TOPIC:\s*(.*)', res, re.I).group(1).strip() if 'TOPIC:' in res else "content"
    tags_raw = re.search(r'TAGS:\s*(.*)', res, re.I).group(1).strip() if 'TAGS:' in res else 'tech'
    tags_clean = re.split(r'\s*[|]\s*|DESC:', tags_raw, flags=re.I)[0].strip()
    tags = [t.strip().replace(' ', '-') for t in tags_clean.split(',') if t.strip()][:3]
    desc = re.search(r'DESC:\s*(.*)', res, re.I).group(1).strip() if 'DESC:' in res else "No description."
    
    folder = slugify(topic.split()[0]) or "content"
    filename = slugify(title)[:80] + ".md"
    path = OUTPUT_CONTENT_DIR / folder / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    
    frontmatter = f"+++\ntitle = '{title}'\ndate = {(datetime.now() - timedelta(days=1)).isoformat()}\ndraft = false\ntags = {tags}\ndescription = '{desc}'\n+++\n\n"
    with open(path, 'w') as f: f.write(frontmatter + state['content'])
    
    print(f"✅ Published: {path}")
    return state

def main():
    """Builds and executes the LangGraph workflow."""
    input_path = INPUT_CONTENT_DRAFT
    if not input_path.exists():
        print(f"Error: {input_path} not found.")
        return

    with open(input_path, 'r') as f: raw = f.read()
    
    workflow = StateGraph(AgentState)
    workflow.add_node("gen", generator_node)
    workflow.add_node("rev", reviewer_node)
    workflow.add_node("pub", publisher_node)
    
    workflow.set_entry_point("gen")
    workflow.add_edge("gen", "rev")
    workflow.add_conditional_edges("rev", lambda x: "pub" if x["approved"] else "gen")
    workflow.add_edge("pub", END)
    
    app = workflow.compile()
    app.invoke({"content": raw, "count": 1, "approved": False, "feedback": "", "title": "", "meta": {}})

if __name__ == "__main__":
    main()
