from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

print("API Key:", os.getenv("GOOGLE_API_KEY")[:10])

client = genai.Client()

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say hello"
    )
    print(response.text)
except Exception as e:
    print(e)