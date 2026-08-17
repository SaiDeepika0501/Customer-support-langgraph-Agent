import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

question = "Where is my order?"

prompt = f"""
You are a professional customer support assistant.

Rules:
- Be polite and concise.
- If order information is missing, ask for the order ID.
- Do not invent refund or shipping details.
- End with: "Is there anything else I can help you with today?"

Customer question:
{question}

Response:
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print(response.text)

# Run:

# python raw_gemini.py