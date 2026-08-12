"""Tests for generator configuration."""

import os
import unittest
from unittest.mock import patch

from config import get_gemini_api_key


class GeminiApiKeyTests(unittest.TestCase):
    def test_returns_plain_key(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            self.assertEqual(get_gemini_api_key(), "test-key")

    def test_normalizes_dotenv_assignment(self):
        with patch.dict(
            os.environ, {"GEMINI_API_KEY": 'GEMINI_API_KEY="test-key"'}
        ):
            self.assertEqual(get_gemini_api_key(), "test-key")

    def test_rejects_missing_key(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "GEMINI_API_KEY is missing"):
                get_gemini_api_key()


if __name__ == "__main__":
    unittest.main()
