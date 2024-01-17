from getcredentials import credentials


def tags(text, comment):
    import requests

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {credentials('openai_api_key')}"
    }

    response_json = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json={
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user",
                      "content": 'I will give you a text and you have to find 10 or more best tags that fit into the '
                                 'topic and'
                                 'reply with only them, separated by commas. Text: ' + text + ' ' + comment}],
        "temperature": 0
    }).json()

    return response_json["choices"][0]["message"]["content"]
