"""
Multi-Agent Content Generation System with Gemini AI
This system orchestrates three agents: Generator, Reviewer, and Publisher
to create, refine, and publish technical documentation content using Gemini LLM.
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI


# Configure Gemini API
# Set your API key as an environment variable: export GEMINI_API_KEY="your-api-key"
# Or replace the placeholder below with your actual key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")


def get_llm(temperature: float = 0.7) -> ChatGoogleGenerativeAI:
    """Initialize and return a Gemini LLM instance."""
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        api_key=GEMINI_API_KEY,
        temperature=temperature
    )


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
    tags: list[str]
    description: str


# Technical Documentation Guidelines
TECHNICAL_GUIDELINES = """
You are a technical documentation expert. Your task is to synthesize high-quality technical content.

Guidelines for Technical Documentation:
1. Use clear, concise language appropriate for technical audiences
2. Structure content with proper headings and sections
3. Include relevant technical details and data
4. Maintain consistent professional tone
5. Ensure logical flow and organization
6. Use examples and evidence to support points
7. Keep paragraphs focused and coherent
8. Format using Markdown where appropriate
9. Ensure accuracy and credibility

You should create engaging, well-structured technical content that is both informative and accessible.
"""

# Review Criteria
REVIEW_CRITERIA = """
You are a content reviewer evaluating technical documentation.

Evaluation Criteria:
1. **Technical Accuracy**: Content is factually correct and credible
2. **Structure**: Clear organization with proper headings and sections
3. **Depth**: Appropriate detail level for the target audience
4. **Clarity**: Easy to understand, well-written prose
5. **Completeness**: All important aspects are covered
6. **Formatting**: Proper Markdown formatting and readability
7. **Flow**: Logical progression of ideas

Scoring:
- APPROVE: Content meets all criteria and is publication-ready
- REVISE: Content needs improvement in specific areas

When suggesting revisions, be specific about what needs improvement and why.
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
    Uses Gemini to read raw content and synthesize it based on technical guidelines.
    Incorporates feedback from Reviewer if available.
    """
    print(f"\n{'='*60}")
    print(f"🤖 GENERATOR AGENT - Iteration {state['iteration_count']}")
    print(f"{'='*60}")
    
    llm = get_llm(temperature=0.7)
    
    # On first iteration, process raw content
    if state['iteration_count'] == 1:
        print("📖 Processing raw content with Gemini AI...")
        raw_content = state['raw_content']
        print(f"   Raw content length: {len(raw_content)} characters")
        
        # Limit input to avoid token limits (take first portion)
        content_sample = raw_content[:8000] if len(raw_content) > 8000 else raw_content
        
        prompt = f"""{TECHNICAL_GUIDELINES}

Based on the following raw content, create a well-structured technical article:

{content_sample}

Requirements:
- Extract the key insights and information
- Create clear sections with proper headings
- Maintain technical accuracy
- Use Markdown formatting
- Create an engaging, professional article

Generate the article now:"""
        
        print("🔄 Calling Gemini API for content generation...")
        response = llm.invoke(prompt)
        generated = response.content
        
        # Extract title from generated content
        title = extract_title_from_content(generated)
        state['title'] = title
        print(f"\n📌 Generated title: {title}")
        
    else:
        # Subsequent iterations: refine based on feedback
        print(f"\n📝 Refining content based on reviewer feedback...")
        print(f"   Feedback: {state['review_feedback']}")
        
        prompt = f"""{TECHNICAL_GUIDELINES}

You previously generated this content:

{state['generated_content']}

The reviewer provided this feedback:

{state['review_feedback']}

Please revise the content to address all the feedback points. Maintain the overall structure but improve based on the specific suggestions.

Generate the revised article now:"""
        
        print("🔄 Calling Gemini API for content refinement...")
        response = llm.invoke(prompt)
        generated = response.content
    
    state['generated_content'] = generated
    print(f"\n✅ Generated content length: {len(generated)} characters")
    
    return state


def reviewer_node(state: AgentState) -> AgentState:
    """
    Agent 2: Reviewer/Critic
    Uses Gemini to evaluate content against criteria and provide feedback.
    Routes content back to Generator if not approved (max 4 iterations).
    """
    print(f"\n{'='*60}")
    print(f"🔍 REVIEWER AGENT - Iteration {state['iteration_count']}")
    print(f"{'='*60}")
    
    content = state['generated_content']
    print(f"📊 Reviewing content with Gemini AI ({len(content)} characters)...")
    
    llm = get_llm(temperature=0.3)  # Lower temperature for more consistent evaluation
    
    prompt = f"""{REVIEW_CRITERIA}

Please review the following technical content:

{content}

Provide your evaluation in the following format:

DECISION: [APPROVE or REVISE]
REASONING: [Brief explanation of your decision]
FEEDBACK: [If REVISE, provide specific suggestions for improvement. If APPROVE, leave empty]

Your evaluation:"""
    
    print("🔄 Calling Gemini API for content review...")
    response = llm.invoke(prompt)
    evaluation = response.content
    
    print(f"\n📋 Review Result:")
    print(f"   {evaluation[:200]}...")
    
    # Parse the evaluation
    decision_match = re.search(r'DECISION:\s*(APPROVE|REVISE)', evaluation, re.IGNORECASE)
    feedback_match = re.search(r'FEEDBACK:\s*(.+?)(?:\n\n|\Z)', evaluation, re.DOTALL | re.IGNORECASE)
    
    if decision_match:
        decision = decision_match.group(1).upper()
    else:
        # Fallback: look for keywords in the response
        if 'APPROVE' in evaluation.upper():
            decision = 'APPROVE'
        else:
            decision = 'REVISE'
    
    # Check if we've hit max iterations
    if state['iteration_count'] >= 4 and decision == 'REVISE':
        raise RuntimeError(
            f"❌ Maximum iterations (4) reached without approval.\n"
            f"Latest feedback: {evaluation}"
        )
    
    # Determine approval
    if decision == 'APPROVE':
        state['approved'] = True
        state['review_feedback'] = ""
        state['final_content'] = content
        print(f"\n✅ Content APPROVED after {state['iteration_count']} iteration(s)")
    else:
        state['approved'] = False
        # Extract feedback
        if feedback_match:
            feedback = feedback_match.group(1).strip()
        else:
            # Fallback: use the entire evaluation as feedback
            feedback = evaluation
        
        state['review_feedback'] = feedback
        state['iteration_count'] += 1
        print(f"\n⚠️  Content NEEDS REVISION")
        print(f"   Feedback: {feedback[:200]}...")
    
    return state


def publisher_node(state: AgentState) -> AgentState:
    """
    Agent 3: Publisher/Formatter
    Uses Gemini to extract metadata and format approved content with TOML front-matter.
    """
    print(f"\n{'='*60}")
    print(f"📤 PUBLISHER AGENT")
    print(f"{'='*60}")
    
    content = state['final_content']
    
    # Use Gemini to extract metadata
    llm = get_llm(temperature=0.3)
    
    prompt = f"""Analyze this technical article and extract metadata:

{content[:2000]}

Provide the following in this exact format:

TITLE: [A clear, concise title for the article]
TAGS: [3-5 relevant tags, comma-separated]
DESCRIPTION: [A one-sentence description, max 150 characters]

Your metadata:"""
    
    print("🔄 Calling Gemini API for metadata extraction...")
    response = llm.invoke(prompt)
    metadata = response.content
    
    # Parse metadata
    title_match = re.search(r'TITLE:\s*(.+?)(?:\n|$)', metadata)
    tags_match = re.search(r'TAGS:\s*(.+?)(?:\n|$)', metadata)
    desc_match = re.search(r'DESCRIPTION:\s*(.+?)(?:\n|$)', metadata)
    
    # Extract or use defaults
    if title_match:
        title = title_match.group(1).strip()
        state['title'] = title
    else:
        title = state.get('title', extract_title_from_content(content))
    
    if tags_match:
        tags_str = tags_match.group(1).strip()
        tags = [tag.strip() for tag in tags_str.split(',')]
        state['tags'] = tags
    else:
        tags = ['technical', 'documentation']
        state['tags'] = tags
    
    if desc_match:
        description = desc_match.group(1).strip()
        state['description'] = description
    else:
        description = content.replace('\n', ' ').strip()[:150] + '...'
        state['description'] = description
    
    print(f"\n📊 Extracted Metadata:")
    print(f"   Title: {title}")
    print(f"   Tags: {tags}")
    print(f"   Description: {description[:80]}...")
    
    # Generate folder name
    folder_name = slugify(' '.join(title.split()[0:3]))  # First 3 words
    if not folder_name:
        folder_name = "content"
    state['folder_name'] = folder_name
    
    # Generate filename
    filename = slugify(title) + '.md'
    
    # Create TOML front-matter
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
    print("   Powered by Gemini AI")
    print("="*60)
    print("\nSystem Components:")
    print("  🤖 Agent 1: Generator - Synthesizes content with Gemini")
    print("  🔍 Agent 2: Reviewer - Evaluates with Gemini")
    print("  📤 Agent 3: Publisher - Extracts metadata and publishes")
    print("="*60)
    
    # Check API key
    if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("\n⚠️  WARNING: Using placeholder API key!")
        print("   Set GEMINI_API_KEY environment variable or update the code.")
        print("   Example: export GEMINI_API_KEY='your-actual-key'\n")
    
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
        'folder_name': '',
        'tags': [],
        'description': ''
    }
    
    # Create and compile workflow
    print("\n🔧 Building workflow graph...")
    workflow = create_workflow()
    app = workflow.compile()
    
    # Execute the workflow
    print("\n▶️  Executing workflow with Gemini AI...\n")
    
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
        print(f"🏷️  Tags: {result['tags']}")
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
