# Gemini API Key Setup

## Setting Your API Key

The multi-agent system uses Google's Gemini API for intelligent content generation, review, and metadata extraction.

### Option 1: Environment Variable (Recommended)

Set the `GEMINI_API_KEY` environment variable:

```bash
export GEMINI_API_KEY="your-actual-gemini-api-key-here"
```

For GitHub Actions, create the repository secret `GEMINI_API_KEY`. You may paste
either the key alone or the corresponding `.env` assignment; the generator
normalizes both formats without printing the secret.

The workflow validates the key before generating content and prints a short
SHA-256 fingerprint. Compare it with the local key without revealing the key:

```bash
cd generator
uv run python -c 'from dotenv import load_dotenv; load_dotenv(); from config import get_gemini_api_key; from check_gemini_credentials import key_fingerprint; print(key_fingerprint(get_gemini_api_key()))'
```

If Google reports `API_KEY_INVALID`, create a new key in Google AI Studio and
replace the repository Actions secret. Google automatically creates new AI
Studio keys as **Auth keys**; there is no separate key-type option to select. A
code change cannot repair a key that Google has rejected.

## Getting a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
