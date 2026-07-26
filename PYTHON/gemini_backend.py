import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

chat = client.chats.create(
    model="gemini-2.5-flash"
)


def stream_response(prompt):

    stream = chat.send_message_stream(prompt)

    for chunk in stream:
        if chunk.text:
            yield chunk.text