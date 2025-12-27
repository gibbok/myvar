"""
Multi-Agent Content Generation System with Gemini AI
Orchestrates Generator, Reviewer, and Publisher agents.
"""

import os, re
from datetime import datetime
from pathlib import Path
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI

# Config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
BASE_DIR = Path("/Users/gibbok/Documents/repos/myvar")
OUTPUT_CONTENT_DIR = BASE_DIR / "website/content"

def get_llm(temp=0.7):
    return ChatGoogleGenerativeAI(model='gemini-3-flash-preview', api_key=GEMINI_API_KEY, temperature=temp)

def ensure_str(content) -> str:
    if isinstance(content, list):
        return "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)
    return str(content)

class AgentState(TypedDict):
    content: str
    feedback: str
    count: int
    approved: bool
    title: str
    meta: dict

def slugify(text: str) -> str:
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9\s-]', '', text.lower()).replace(' ', '-')).strip('-')

def generator_node(state: AgentState):
    print(f"🤖 Generator - Iteration {state['count']}")
    llm = get_llm(0.7)
    
    prompt = f"""Synthesize this content into a professional technical article with Markdown:
{state['content'] if state['count'] == 1 else state['content']}
Feedback to address: {state['feedback'] if state['feedback'] else 'None (First run)'}
Requirements: Key insights, clear headings, professional tone."""
    
    res = ensure_str(llm.invoke(prompt).content)
    state['content'] = res
    if state['count'] == 1:
        state['title'] = res.strip().split('\n')[0].replace('#', '').strip()[:100]
    return state

def reviewer_node(state: AgentState):
    print(f"🔍 Reviewer - Iteration {state['count']}")
    llm = get_llm(0.1)
    
    prompt = f"""Review this content. Decision must be 'APPROVE' or 'REVISE'.
Content: {state['content']}
Format: 
DECISION: [APPROVE|REVISE]
FEEDBACK: [Details if REVISE]"""
    
    res = ensure_str(llm.invoke(prompt).content)
    decision = 'APPROVE' if 'DECISION: APPROVE' in res.upper() else 'REVISE'
    feedback = res.split('FEEDBACK:')[-1].strip() if 'FEEDBACK:' in res else ""
    
    if state['count'] >= 4: decision = 'APPROVE' # Force exit to prevent hanging/loops
    
    state.update({"approved": decision == 'APPROVE', "feedback": feedback})
    if not state['approved']: state['count'] += 1
    return state

def publisher_node(state: AgentState):
    print("📤 Publisher - Finalizing...")
    llm = get_llm(0.1)
    prompt = f"Extract metadata from this article (format: TITLE: ... | TAGS: ... | DESC: ...):\n{state['content'][:2000]}"
    res = ensure_str(llm.invoke(prompt).content)
    
    # Simple extraction
    title = re.search(r'TITLE:\s*(.*)', res, re.I).group(1).strip() if 'TITLE:' in res else state['title']
    tags = re.search(r'TAGS:\s*(.*)', res, re.I).group(1).strip().split(',') if 'TAGS:' in res else ['tech']
    desc = re.search(r'DESC:\s*(.*)', res, re.I).group(1).strip() if 'DESC:' in res else "No description."
    
    folder = slugify(' '.join(title.split()[:3])) or "content"
    path = OUTPUT_CONTENT_DIR / folder / (slugify(title) + ".md")
    path.parent.mkdir(parents=True, exist_ok=True)
    
    frontmatter = f"+++\ntitle = '{title}'\ndate = {datetime.now().isoformat()}\ndraft = false\ntags = {tags}\ndescription = '{desc}'\n+++\n\n"
    with open(path, 'w') as f: f.write(frontmatter + state['content'])
    
    print(f"✅ Published: {path}")
    return state

def main():
    input_path = BASE_DIR / "generator/drafts/content.md"
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
