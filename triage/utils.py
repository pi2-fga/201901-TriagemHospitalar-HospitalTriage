import os
import requests
import json
from django.utils.translation import ugettext_lazy as _
from rpc.rpc_client import RpcClient


HEADERS = {'content-type': 'application/json'}
TRIAGE_RISK_CATEGORIES = {
    _('red'): 0,
    _('yellow'): 1,
    _('green'): 2,
    _('blue'): 3,

}


def call_blood_pressure_measurement():
    """
    Calls RPC Server to measure patient blood pressure
    """
    # return {'blood_pressure': "[\"120\", \"81\"]"}

    rpc = RpcClient()
    rpc_response = rpc.call('pressao').decode()
    rpc.connection.close()

    blood_pressure_dict = {
        'blood_pressure': rpc_response
    }
    return blood_pressure_dict


def call_height_mass_measurement():
    """
    Calls RPC Server to measure patient height and mass
    """
    # return {'height': 1.80, 'body_mass': 80}

    rpc = RpcClient()
    rpc_response_height = rpc.call('altura').decode()
    rpc_response_body_mass = rpc.call('peso').decode()
    rpc.connection.close()

    height_mass_dict = {
        'height': float(rpc_response_height),
        'body_mass': float(rpc_response_body_mass)
    }
    return height_mass_dict


def call_temperature_measurement():
    """
    Calls RPC Server to measure patient body temperature
    """
    # return {'body_temperature': 36.0}

    rpc = RpcClient()
    rpc_response = rpc.call('temperatura').decode()
    rpc.connection.close()

    body_temperature_dict = {
        'body_temperature': float(rpc_response)
    }
    return body_temperature_dict


def call_oxygen_measurement():
    """
    Calls RPC Server to measure patient blood oxygen level
    """
    # return {'blood_oxygen_level': 95.0}

    rpc = RpcClient()
    rpc_response = rpc.call('oximetria').decode()
    rpc.connection.close()

    blood_oxygen_level_dict = {
        'blood_oxygen_level': float(rpc_response)
    }
    return blood_oxygen_level_dict


def call_eletrocardiogram():
    """
    Calls RPC Server to make eletrocardiogram
    """
    # return {'eletrocardiogram': 95.0}

    rpc = RpcClient()
    rpc_response = rpc.call('ecg').decode()
    rpc.connection.close()

    eletrocardiogram_dict = {
        'eletrocardiogram': rpc_response
    }
    return eletrocardiogram_dict


MEASURES_DICT = {
     'temperature':
     ['Posicione o seu braço, como mostrado abaixo, para medirmos seus dados vitais.',
      'img/temperature.gif', call_temperature_measurement],
     'oximetry':
     ['Posicione seu dedo na presilha, como mostrado abaixo, para medirmos seus dados vitais.',
      'img/oximetry.gif', call_oxygen_measurement],
     'pressure':
     ['Posicione seu braço na braçadeira, como mostrado abaixo, para medirmos sua pressão.',
      'img/pressure.gif', call_blood_pressure_measurement],
     'body_mass':
     ['Posicione seus pés na marca e espere o sinal, como mostrado abaixo, para medirmos seu peso e altura.',
      'img/weight.gif', call_height_mass_measurement],
     'eletrocardiogram':
     ['Aguarde para realização de mais exames.', 'img/wait.gif',
      call_eletrocardiogram]
}


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
    if response == '[]\n':
        return {
            'type': 'restart',
            'content': None,
        }
    elif response:
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


def save_values(triage, values):
    values = values()
    for key in values.keys():
        setattr(triage, key, values[key])
    triage.save()
