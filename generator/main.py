"""
Multi-Agent Content Generation System
This system orchestrates three agents: Generator, Reviewer, and Publisher
to create, refine, and publish technical documentation content.
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END


# Define the state structure for the multi-agent workflow
class AgentState(TypedDict):
    raw_content: str
    generated_content: str
    review_feedback: str
    iteration_count: int
    approved: bool
    final_content: str
    output_path: str
    summary: str
    title: str
    folder_name: str


# Technical Documentation Guidelines (scaffolded)
TECHNICAL_GUIDELINES = """
Guidelines for Technical Documentation:
1. Use clear, concise language
2. Structure content with proper headings and sections
3. Include technical details where relevant
4. Maintain consistent professional tone
5. Ensure logical flow and organization
6. Use examples and data to support points
7. Keep paragraphs focused and coherent
"""

# Review Criteria (scaffolded)
REVIEW_CRITERIA = """
Content Review Criteria:
1. Technical accuracy and credibility
2. Clear structure and organization
3. Appropriate depth for target audience
4. Proper formatting and readability
5. No major grammatical errors
6. Logical flow of ideas
7. Adequate supporting evidence
"""


def read_input_content(file_path: str) -> str:
    """Read raw content from the input markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {file_path}")


def extract_title_from_content(content: str) -> str:
    """Extract a title from the content (first meaningful line or heading)."""
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line:
            # Remove markdown heading markers
            title = re.sub(r'^#+\s*', '', line)
            # Take first sentence or first 100 chars
            if '.' in title:
                title = title.split('.')[0]
            return title[:100].strip()
    return "Untitled Document"


def slugify(text: str) -> str:
    """Convert text to slug format: first-word-second-word"""
    # Convert to lowercase
    text = text.lower()
    # Remove special characters, keep only alphanumeric and spaces
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    # Replace spaces with hyphens
    text = re.sub(r'\s+', '-', text)
    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)
    # Remove leading/trailing hyphens
    text = text.strip('-')
    return text


def generator_node(state: AgentState) -> AgentState:
    """
    Agent 1: Generator
    Reads raw content and synthesizes it based on technical guidelines.
    Incorporates feedback from Reviewer if available.
    """
    print(f"\n{'='*60}")
    print(f"🤖 GENERATOR AGENT - Iteration {state['iteration_count']}")
    print(f"{'='*60}")
    
    # On first iteration, read the raw content
    if state['iteration_count'] == 1:
        print("📖 Reading raw content from file...")
        raw_content = state['raw_content']
        print(f"   Content length: {len(raw_content)} characters")
    
    # If there's feedback, show it
    if state['review_feedback']:
        print(f"\n📝 Incorporating reviewer feedback:")
        print(f"   {state['review_feedback']}")
    
    # In a real implementation, this would use an LLM to generate/refine content
    # For this scaffold, we'll do basic processing
    if state['iteration_count'] == 1:
        # First pass: extract a meaningful section
        lines = state['raw_content'].split('\n')
        # Take first few meaningful paragraphs
        content_lines = []
        for line in lines[:50]:  # Limit to first 50 lines for demo
            if line.strip():
                content_lines.append(line)
        
        generated = '\n'.join(content_lines)
        
        # Extract title
        title = extract_title_from_content(generated)
        state['title'] = title
        print(f"\n📌 Extracted title: {title}")
    else:
        # Subsequent iterations: simulate refinement
        generated = state['generated_content']
        # Add improvement marker (in real implementation, LLM would refine)
        generated = f"{generated}\n\n[Refined based on feedback: {state['review_feedback']}]"
    
    state['generated_content'] = generated
    print(f"\n✅ Generated content length: {len(generated)} characters")
    
    return state


def reviewer_node(state: AgentState) -> AgentState:
    """
    Agent 2: Reviewer/Critic
    Evaluates content against criteria and provides feedback.
    Routes content back to Generator if not approved (max 4 iterations).
    """
    print(f"\n{'='*60}")
    print(f"🔍 REVIEWER AGENT - Iteration {state['iteration_count']}")
    print(f"{'='*60}")
    
    content = state['generated_content']
    print(f"📊 Reviewing content ({len(content)} characters)...")
    
    # In a real implementation, this would use an LLM to evaluate content
    # For this scaffold, we'll use simple heuristics
    
    # Criteria checks (simplified)
    has_adequate_length = len(content) > 200
    has_structure = '\n' in content
    has_title = bool(state.get('title'))
    
    # Simple scoring
    score = sum([has_adequate_length, has_structure, has_title])
    passing_score = 3
    
    print(f"\n📋 Review Checklist:")
    print(f"   ✓ Adequate length: {has_adequate_length}")
    print(f"   ✓ Has structure: {has_structure}")
    print(f"   ✓ Has title: {has_title}")
    print(f"   Score: {score}/{passing_score}")
    
    # Check if we've hit max iterations
    if state['iteration_count'] >= 4 and score < passing_score:
        raise RuntimeError(
            f"❌ Maximum iterations (4) reached without approval. "
            f"Final score: {score}/{passing_score}"
        )
    
    # Determine approval
    if score >= passing_score:
        state['approved'] = True
        state['review_feedback'] = ""
        state['final_content'] = content
        print(f"\n✅ Content APPROVED after {state['iteration_count']} iteration(s)")
    else:
        state['approved'] = False
        # Provide feedback based on what's missing
        feedback_items = []
        if not has_adequate_length:
            feedback_items.append("Content needs more depth and detail")
        if not has_structure:
            feedback_items.append("Improve content structure with sections")
        if not has_title:
            feedback_items.append("Add a clear title")
        
        state['review_feedback'] = "; ".join(feedback_items)
        state['iteration_count'] += 1
        print(f"\n⚠️  Content NEEDS REVISION")
        print(f"   Feedback: {state['review_feedback']}")
    
    return state


def publisher_node(state: AgentState) -> AgentState:
    """
    Agent 3: Publisher/Formatter
    Formats approved content with TOML front-matter and saves to file.
    """
    print(f"\n{'='*60}")
    print(f"📤 PUBLISHER AGENT")
    print(f"{'='*60}")
    
    # Extract metadata
    title = state['title']
    content = state['final_content']
    
    # Generate folder name
    folder_name = slugify(' '.join(title.split()[0:3]))  # First 3 words
    if not folder_name:
        folder_name = "content"
    state['folder_name'] = folder_name
    
    # Generate filename
    filename = slugify(title) + '.md'
    
    # Generate tags (simplified - in real implementation, use LLM)
    tags = ['technical', 'documentation', 'generated']
    
    # Extract description (first sentence or first 150 chars)
    description_text = content.replace('\n', ' ').strip()
    if '.' in description_text:
        description = description_text.split('.')[0] + '.'
    else:
        description = description_text[:150] + '...'
    
    # Create TOML front-matter
    current_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
    if not current_date.endswith(('Z', '+00:00', '-07:00')):
        # Add timezone offset format
        current_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S-07:00')
    
    toml_frontmatter = f"""+++
title = '{title}'
date = {current_date}
draft = false
tags = {tags}
description = '{description}'
+++

"""
    
    # Combine frontmatter with content
    final_document = toml_frontmatter + content
    
    # Create output directory
    output_dir = Path('/Users/gibbok/Documents/repos/myvar/website/content') / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save file
    output_path = output_dir / filename
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_document)
    
    state['output_path'] = str(output_path)
    
    print(f"\n📁 Created directory: {output_dir}")
    print(f"💾 Saved file: {output_path}")
    print(f"📊 Title: {title}")
    print(f"🏷️  Tags: {tags}")
    print(f"✅ Publishing complete!")
    
    return state


def should_continue_or_publish(state: AgentState) -> Literal["generator", "publisher"]:
    """
    Conditional edge function to determine next step after review.
    """
    if state['approved']:
        return "publisher"
    else:
        return "generator"


def create_workflow() -> StateGraph:
    """Create and configure the multi-agent workflow graph."""
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("generator", generator_node)
    workflow.add_node("reviewer", reviewer_node)
    workflow.add_node("publisher", publisher_node)
    
    # Define edges
    workflow.set_entry_point("generator")
    workflow.add_edge("generator", "reviewer")
    workflow.add_conditional_edges(
        "reviewer",
        should_continue_or_publish,
        {
            "generator": "generator",  # Loop back for refinement
            "publisher": "publisher"   # Move to publishing
        }
    )
    workflow.add_edge("publisher", END)
    
    return workflow


def main():
    """Main function to run the multi-agent content generation system."""
    print("="*60)
    print("🚀 MULTI-AGENT CONTENT GENERATION SYSTEM")
    print("="*60)
    print("\nSystem Components:")
    print("  🤖 Agent 1: Generator - Synthesizes content")
    print("  🔍 Agent 2: Reviewer - Evaluates and provides feedback")
    print("  📤 Agent 3: Publisher - Formats and saves content")
    print("="*60)
    
    # Input file path
    input_file = "/Users/gibbok/Documents/repos/myvar/generator/drafts/content.md"
    
    # Read raw content
    print(f"\n📂 Reading input from: {input_file}")
    raw_content = read_input_content(input_file)
    
    # Initialize state
    initial_state: AgentState = {
        'raw_content': raw_content,
        'generated_content': '',
        'review_feedback': '',
        'iteration_count': 1,
        'approved': False,
        'final_content': '',
        'output_path': '',
        'summary': '',
        'title': '',
        'folder_name': ''
    }
    
    # Create and compile workflow
    print("\n🔧 Building workflow graph...")
    workflow = create_workflow()
    app = workflow.compile()
    
    # Execute the workflow
    print("\n▶️  Executing workflow...\n")
    
    try:
        result = app.invoke(initial_state)
        
        # Generate summary
        print(f"\n{'='*60}")
        print("📊 EXECUTION SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Status: SUCCESS")
        print(f"🔄 Iterations: {result['iteration_count']}")
        print(f"📝 Title: {result['title']}")
        print(f"📁 Folder: {result['folder_name']}")
        print(f"💾 Output Path: {result['output_path']}")
        print(f"📄 Content Length: {len(result['final_content'])} characters")
        print(f"{'='*60}")
        
        return result
        
    except RuntimeError as e:
        print(f"\n{'='*60}")
        print("❌ EXECUTION FAILED")
        print(f"{'='*60}")
        print(f"Error: {str(e)}")
        print(f"{'='*60}")
        raise


if __name__ == "__main__":
    main()
