# Myvar Website

A note-keeping website that transforms brief notes into polished articles using AI agents.

I use this project to create content about technologies and software engineering for my website.\
<https://gibbok.github.io/myvar/>

## What it does

Send draft notes to the system, and AI agents automatically generate, review, and publish website articles.

## Tech Stack

- **Architecture**: JAMstack with Hugo hosted on GitHub Pages
- **AI Orchestration**: LangGraph with Google Gemini LLM
- **Search**: Pagefind - fully static search library
- **Agents**:
  - **Generator**: Creates content from draft notes
  - **Reviewer**: Reviews and provides feedback for improvements
  - **Publisher**: Finalizes content and generates metadata for publication

## How it works

1. Write any notes in `generator/drafts/content.md`
2. Run the generator: `cd generator && make start`
3. Agents collaborate to refine and publish the article
4. Output appears in `website/content/` ready for Hugo to build
5. OG images for social sharing are created automatically at build time

## Setup

```bash
# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Add your GEMINI_API_KEY to .env
```

## Usage

```bash
# Run the generator
cd generator && make start

```
Make a pull request to deploy\
The site will be automatically deployed to GitHub Pages when the PR is merged

## Makefile Commands

**Generator (generator/)**
- `make start` - Run the AI agent pipeline to generate articles

**Website (website/)**
- `make serve` - Start Hugo development server
- `make build` - Build the static site

## Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key
- `GEMINI_MODEL`: Model to use (default: gemini-2.5-flash)
- `DEBUG_MODE`: Enable debug output (default: false)

