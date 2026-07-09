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

1. For local generation, write notes in `generator/drafts/content.md`
2. Run the generator: `cd generator && make start`
3. Agents generate, review, and publish the article
4. Output is written to `website/content/`
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
# Generate content locally
cd generator && make start

```
The `generator/drafts/` folder is only for local content creation and should not be committed.

You can also generate content in GitHub:

1. Open **Actions**.
2. Run **Generate content**.
3. Paste your notes into the `content` input.
4. The workflow generates the article and opens a draft PR with changes in `website/content/`.

Merge the PR to deploy the site to GitHub Pages.

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
