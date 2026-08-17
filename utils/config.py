from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# Read the Gemini API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Safety check
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing in .env file")