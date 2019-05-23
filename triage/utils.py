import os
import requests
import json


HEADERS = {'content-type': 'application/json'}


def make_bot_request(message):
    post_url = os.environ.get("BOT_HOST", "")

    params = {
        "message": message,
    }

    request = requests.post(post_url, data=json.dumps(params), headers=HEADERS)
    return get_bot_category(request)


def get_bot_category(response):
    response = response.text
    response = json.loads(response)[0]["text"]
    partition = response.partition(' ')
    response_type = partition[0]
    if partition[0] == 'pain_scale':
        content = None
    else:
        content = partition[2]
    return {
        'type': response_type,
        'content': content,
    }
