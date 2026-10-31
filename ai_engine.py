from openai import OpenAI
from config import API_KEY, MODEL_NAME, SYSTEM_PROMPT


def get_ai_response(chat_history):

    if not API_KEY:
        raise ValueError("OpenAI API key is missing.")

    client = OpenAI(api_key=API_KEY)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(chat_history)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages
    )

    return response.choices[0].message.content