# from app.config import settings
import openai
from app.prompt import *
from app.config import settings

openai.api_key = settings.openai_api_key

def request_response(user_input, transcript):
    messages = [{"role": "system", "content": question_prompt},
            {"role": "user", "content": [{"type": "text", "text": f"사용자의 질문:\n{transcript + user_input}"}]}]
    
    gpt4_response = openai.chat.completions.create(
            model='gpt-4o-2024-08-06',
            messages=messages,
            max_tokens=1024,
        )

    response = gpt4_response.choices[0].message.content
    print(response)
    return response