import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPEN_AI"))

def get(text):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are required to take following script and output a string in format suggestedTitle(up to 100 symbols, must end with #story #shorts and one custom topic hashtag):description(short recap):videotags(separated with commas, tags only can't have spaces between words). do NOT add anything else to the response."},
            {
                "role": "user",
                "content": text
            }
        ]
    )

    return completion.choices[0].message.content.split(":",2)
