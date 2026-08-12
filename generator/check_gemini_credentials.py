"""Validate Gemini credentials before running the content generator."""

import hashlib
import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from dotenv import load_dotenv

from config import get_gemini_api_key

MODEL_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-3.6-flash"
)


def key_fingerprint(api_key: str) -> str:
    """Return a non-secret identifier that can be compared across environments."""
    return hashlib.sha256(api_key.encode()).hexdigest()[:12]


def validate_credentials(api_key: str, opener=urlopen) -> str:
    """Validate the key against Google's lightweight model metadata endpoint."""
    request = Request(MODEL_URL, headers={"x-goog-api-key": api_key})

    try:
        with opener(request, timeout=30) as response:
            payload = json.load(response)
    except HTTPError as error:
        try:
            payload = json.load(error)
            reason = payload["error"]["details"][0].get("reason", "UNKNOWN")
        except (KeyError, TypeError, ValueError):
            reason = "UNKNOWN"

        if reason == "API_KEY_INVALID":
            raise RuntimeError(
                "Google rejected GEMINI_API_KEY (API_KEY_INVALID). Create a new "
                "key in Google AI Studio (new keys are automatically Auth keys) "
                "and update the repository Actions secret."
            ) from error
        raise RuntimeError(
            f"Gemini credential validation failed with HTTP {error.code} ({reason})."
        ) from error

    return payload.get("name", "unknown model")


def main() -> None:
    """Load, identify, and validate the configured Gemini API key."""
    load_dotenv()
    api_key = get_gemini_api_key()
    fingerprint = key_fingerprint(api_key)
    print(f"Gemini key fingerprint: sha256:{fingerprint} (length: {len(api_key)})")
    model = validate_credentials(api_key)
    print(f"Gemini credentials accepted for {model}.")


if __name__ == "__main__":
    main()
