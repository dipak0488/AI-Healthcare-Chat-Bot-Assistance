from groq import Groq
from dotenv import load_dotenv
import os
import os
from groq import Groq

client = Groq(
    api_key=os.getenv("API_KEY")   # ✅ correct (lowercase)
)

def get_bot_response(message, language="en"):

    if language == "hi":
        lang_instruction = "Reply in Hindi language."
    elif language == "mr":
        lang_instruction = "Reply in Marathi language."
    else:
        lang_instruction = "Reply in English language."

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"""
You are an AI Healthcare Assistant.

Rules:
• Detect symptoms
• Give answers in bullet points
• Maximum 5 points
• Give precautions

{lang_instruction}
"""
            },
            {
                "role": "user",
                "content": message
            }
        ],
        model="llama-3.1-8b-instant"
    )

    return chat_completion.choices[0].message.content