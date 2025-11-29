import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env")

# Configure Gemini API client
genai.configure(api_key=API_KEY)


def generate_text(prompt: str):
    """
    Wrapper around Gemini text generation.

    Args:
        prompt (str): Input prompt for the model.

    Returns:
        tuple:
            text (str): Generated text.
            usage (dict | None): Token usage information.
            response (object | None): Raw Gemini response object.
    """
    # Use an actively supported model id
    # See https://ai.google.dev/gemini-api/docs/models for the latest list.
    model = genai.GenerativeModel("gemini-2.5-flash")

    try:
        response = model.generate_content(prompt)
    except google_exceptions.NotFound as e:
        # Helpful debug message instead of a cryptic stack trace
        raise RuntimeError(
            "Gemini model 'gemini-2.5-flash' was not found for this API key "
            "or API version. Please check that:\n"
            "- Your API key is a Gemini *Developer* key from Google AI Studio.\n"
            "- The model name is available for your account/region.\n"
            "- The project has Gemini API enabled."
        ) from e
    except google_exceptions.GoogleAPICallError as e:
        # Generic API error wrapper
        raise RuntimeError(f"Gemini API call failed: {e}") from e

    text = response.text or ""

    usage = None
    if getattr(response, "usage_metadata", None):
        usage = {
            "prompt_tokens": response.usage_metadata.prompt_token_count,
            "candidates_tokens": response.usage_metadata.candidates_token_count,
            "total_tokens": response.usage_metadata.total_token_count,
        }

    return text, usage, response
