# Multi-Agent Content Generation System

A powerful, multi-agent orchestrator powered by Gemini AI and LangGraph to generate, review, and publish high-quality technical documentation.

## 🚀 Overview

This system utilizes three specialized agents to automate the content lifecycle:
1.  **🤖 Generator**: Synthesizes raw input into structured technical articles.
2.  **🔍 Reviewer**: Critiques the content for accuracy and clarity (with up to 4 refinement loops).
3.  **📤 Publisher**: Extracts SEO metadata and saves the final product with TOML front-matter.

## 🛠️ Setup

### 1. Requirements
- Python 3.12+ (managed via `uv`)
- A Gemini API Key from [Google AI Studio](https://aistudio.google.com/)

### 2. Environment Configuration
Set your API key as an environment variable:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### 3. Git Hook Configuration
To prevent your local drafts from being committed to git, run the setup script:
```bash
bash setup_hooks.sh
```
This installs a `post-checkout` hook that applies `git assume-unchanged` to your local draft file.

## 📖 How to Use

1.  **Prepare Content**: Edit the draft file at `generator/drafts/content.md`.
2.  **Run the Generator**:
    ```bash
    uv run main.py
    ```
3.  **Check Output**: Published files will appear in `website/content/[topic]/`.

## ⚙️ Customization

### Modifying Prompts
The LLM logic is separated from the execution code. You can find and edit the prompts in these files:
- `generator/prompt_generator.txt`: Instructions for article synthesis.
- `generator/prompt_reviewer.txt`: Criteria for content evaluation.
- `generator/prompt_publisher.txt`: Instructions for metadata extraction.

### Metadata Constraints
The system automatically enforces several quality and SEO constraints:
- **Titles**: Maximum 100 characters.
- **Descriptions**: Maximum 120 characters.
- **Filenames**: Maximum 80 characters (SEO-friendly slugs).
- **Tags**: Maximum 3 short, hyphenated tags (e.g., `Tree-Shaking`).
- **Dates**: Automatically set to one day before current execution.

## 📁 Project Structure

```
generator/
├── drafts/
│   └── content.md      # Your current working draft
├── prompt_*.txt        # Externalized LLM prompt templates
├── main.py             # Agent orchestration logic (LangGraph)
├── setup_hooks.sh      # Git hook configuration script
└── pyproject.toml      # Project dependencies
```
