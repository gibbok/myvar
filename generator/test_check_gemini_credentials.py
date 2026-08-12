"""Tests for the Gemini credential preflight."""

import io
import unittest
from urllib.error import HTTPError

from check_gemini_credentials import key_fingerprint, validate_credentials


class Response:
    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def read(self):
        return b'{"name": "models/gemini-3.6-flash"}'


class GeminiCredentialTests(unittest.TestCase):
    def test_validates_key_without_putting_it_in_the_url(self):
        def opener(request, timeout):
            self.assertEqual(timeout, 30)
            self.assertNotIn("test-secret", request.full_url)
            self.assertEqual(request.get_header("X-goog-api-key"), "test-secret")
            return Response()

        self.assertEqual(
            validate_credentials("test-secret", opener),
            "models/gemini-3.6-flash",
        )

    def test_reports_invalid_key_clearly(self):
        body = io.BytesIO(
            b'{"error":{"details":[{"reason":"API_KEY_INVALID"}]}}'
        )

        def opener(_request, timeout):
            self.assertEqual(timeout, 30)
            raise HTTPError("url", 400, "Bad Request", {}, body)

        with self.assertRaisesRegex(RuntimeError, "automatically Auth keys"):
            validate_credentials("invalid", opener)

    def test_fingerprint_is_stable_and_does_not_expose_key(self):
        fingerprint = key_fingerprint("test-secret")

        self.assertEqual(fingerprint, "9caf06bb4436")
        self.assertNotIn("test-secret", fingerprint)


if __name__ == "__main__":
    unittest.main()
