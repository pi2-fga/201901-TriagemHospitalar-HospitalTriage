import os
import requests
import json


HEADERS = {'content-type': 'application/json'}


def send_triage_to_patient_management_app(triage):
    """
    Sends a triage object in json format to be saved in
    patient management app database
    """
    post_url = os.environ.get("PATIENT_HOST", "")
    cookies = {'csrftoken': 'token'}
    headers = HEADERS
    headers['X-CSRF-TOKEN'] = 'token'
    route = os.environ.get("TRIAGE_ROUTE", "")
    params = {
        "triage": triage,
    }
    request = requests.post(post_url + route,
                            data=json.dumps(params),
                            headers=headers, cookies=cookies)
    return request


def send_bot_request(message, triage):
    """
    Sends bot app a message
    """
    post_url = os.environ.get("BOT_HOST", "")

    params = {
        "message": message,
    }

    request = requests.post(post_url, data=json.dumps(params), headers=HEADERS)
    return get_bot_category(request, triage)


def get_bot_category(response, triage):
    """
    Process bot message format, transforming it into a dict
    """
    response = response.text
    if response:
        response = json.loads(response)[0]["text"]
        partition = response.partition(' ')
        response_type = partition[0]
        if partition[0] == 'pain_scale':
            content = None
        else:
            content = partition[2]
        triage.bot_next_type = response_type
        triage.bot_next_content = content
        triage.save()
        return {
            'type': response_type,
            'content': content,
        }


def map_question_animation(question):
    d = {'Posicione seus pés na marca e espere o sinal, como mostrado abaixo, para medirmos seu peso e altura.':
         ['img/weight.gif', {'height': 1.80, 'body_mass': 80}],
         'Posicione o seu braço, como mostrado abaixo, para medirmos seus dados vitais.':
         ['img/temperature.gif', {'temperature': 38.0, 'blood_oxygen_level': 95.0}],
         'Posicione seu braço na braçadeira, como mostrado abaixo, para medirmos sua pressão.':
         ['img/pressure.gif', {'blood_pressure': "[\"120\", \"81\"]"}]
         }
    return d[question]
