import os

from dotenv import load_dotenv
import google.generativeai as genai

# Load variables from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set in .env")

genai.configure(api_key=api_key)

print("Available models for this API key:\n")

for m in genai.list_models():
    # Каждый объект модели имеет поле name
    print("-", m.name)
