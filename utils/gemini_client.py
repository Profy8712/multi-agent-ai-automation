import os
from typing import Any, Dict, Tuple

from dotenv import load_dotenv
import google.generativeai as genai


class GeminiAPIError(Exception):
    """Raised when Google Gemini API call fails."""


# Load env variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY in .env")

# Configure Gemini
genai.configure(api_key=API_KEY)

# Correct model names for NEW SDK
MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "models/gemini-2.5-flash")


model = genai.GenerativeModel(MODEL_NAME)


def generate_text(prompt: str) -> Tuple[str, Dict[str, Any], Any]:
    try:
        response = model.generate_content(
            prompt,
            generation_config={"max_output_tokens": 1024}
        )
    except Exception as exc:
        raise GeminiAPIError(f"Gemini API request failed: {exc}")

    text = response.text or ""

    usage = {}
    try:
        usage = response.usage_metadata.to_dict()
    except:
        pass

    return text.strip(), usage, response
