# Gemini API Key Setup

## Setting Your API Key

The multi-agent system uses Google's Gemini API for intelligent content generation, review, and metadata extraction.

### Option 1: Environment Variable (Recommended)

Set the `GEMINI_API_KEY` environment variable:

```bash
export GEMINI_API_KEY="your-actual-gemini-api-key-here"
```

To make it permanent, add it to your shell configuration file (`~/.zshrc` or `~/.bashrc`):

```bash
echo 'export GEMINI_API_KEY="your-actual-gemini-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### Option 2: Update main.py

Edit `main.py` and replace the placeholder on line 18:

```python
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-actual-gemini-api-key-here")
```

## Getting a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

## Testing the Integration

Once you've set your API key, run:

```bash
uv run python main.py
```

The system will:
- ✅ Generate content using Gemini based on technical guidelines
- ✅ Review the content with AI-powered evaluation
- ✅ Extract metadata (title, tags, description) intelligently
- ✅ Publish formatted content with TOML front-matter

## Troubleshooting

If you see `⚠️ WARNING: Using placeholder API key!`, the API key is not set correctly.

Verify your environment variable:
```bash
echo $GEMINI_API_KEY
```

It should display your actual API key (not the placeholder).
