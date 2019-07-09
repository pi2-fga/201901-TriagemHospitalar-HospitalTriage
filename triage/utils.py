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
    rpc_response = rpc.call('pressao')
    rpc.connection.close()

    try:

        rpc_response_decoded = rpc_response.decode()
        rpc_response_loads = json.loads(rpc_response_decoded)

        if isinstance(rpc_response_loads, list):

            if len(rpc_response_loads) != 2:
                raise Exception()

            for i in range(len(rpc_response_loads)):

                if isinstance(rpc_response_loads[i], float):
                    rpc_response_loads[i] = int(rpc_response_loads[i])
                elif not isinstance(rpc_response_loads[i], int):
                    raise Exception()

                if rpc_response_loads[i] < 0 or rpc_response_loads[i] > 999:
                    raise Exception()

            rpc_response = rpc_response_loads

        else:
            raise Exception()

    except:

        rpc_response = '-1000'  # Error flag

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
    rpc_response_altura = rpc.call('altura')
    rpc.connection.close()

    try:

        rpc_response_decoded_altura = rpc_response_altura.decode()
        rpc_response_loads_altura = json.loads(rpc_response_decoded_altura)

        if isinstance(rpc_response_loads_altura, int) or \
                isinstance(rpc_response_loads_altura, float):

            if isinstance(rpc_response_loads_altura, float):
                rpc_response_loads_altura = int(rpc_response_loads_altura)

            if rpc_response_loads_altura < 0 or \
                    rpc_response_loads_altura > 210:
                raise Exception()

            rpc_response_altura = rpc_response_loads_altura

        else:
            raise Exception()

    except:

        rpc_response_altura = -1000  # Error flag

    rpc = RpcClient()
    rpc_response_peso = rpc.call('peso')
    rpc.connection.close()

    try:

        rpc_response_decoded_peso = rpc_response_peso.decode()
        rpc_response_loads_peso = json.loads(rpc_response_decoded_peso)

        if isinstance(rpc_response_loads_peso, int) or \
                isinstance(rpc_response_loads_peso, float):

            if isinstance(rpc_response_loads_peso, int):
                rpc_response_loads_peso = float(rpc_response_loads_peso)

            if rpc_response_loads_peso < 0 or \
                    rpc_response_loads_peso > 200:
                raise Exception()

            rpc_response_peso = round(rpc_response_loads_peso, 1)

        else:
            raise Exception()

    except:

        rpc_response_peso = -1000.0  # Error flag

    height_mass_dict = {
        'height': rpc_response_altura,
        'body_mass': rpc_response_peso
    }
    return height_mass_dict


def call_temperature_measurement():
    """
    Calls RPC Server to measure patient body temperature
    """
    # return {'body_temperature': 36.0}

    rpc = RpcClient()
    rpc_response = rpc.call('temperatura')
    rpc.connection.close()

    try:

        rpc_response_decoded = rpc_response.decode()
        rpc_response_loads = json.loads(rpc_response_decoded)

        if isinstance(rpc_response_loads, int) or \
                isinstance(rpc_response_loads, float):

            if isinstance(rpc_response_loads, int):
                rpc_response_loads = float(rpc_response_loads)

            if rpc_response_loads < 0 or \
                    rpc_response_loads > 99.9:
                raise Exception()

            rpc_response = round(rpc_response_loads, 1)

        else:
            raise Exception()

    except:

        rpc_response = -1000.0  # Error flag

    body_temperature_dict = {
        'body_temperature': rpc_response
    }
    return body_temperature_dict


def call_oxygen_measurement():
    """
    Calls RPC Server to measure patient blood oxygen level
    """
    # return {'blood_oxygen_level': 95.0}

    rpc = RpcClient()
    rpc_response = rpc.call('oximetria')
    rpc.connection.close()

    try:

        rpc_response_decoded = rpc_response.decode()
        rpc_response_loads = json.loads(rpc_response_decoded)

        if isinstance(rpc_response_loads, int) or \
                isinstance(rpc_response_loads, float):

            if isinstance(rpc_response_loads, int):
                rpc_response_loads = float(rpc_response_loads)

            if rpc_response_loads < 0 or \
                    rpc_response_loads > 100:
                raise Exception()

            rpc_response = round(rpc_response_loads, 1)

        else:
            raise Exception()

    except:

        rpc_response = -1000.0  # Error flag

    blood_oxygen_level_dict = {
        'blood_oxygen_level': rpc_response
    }
    return blood_oxygen_level_dict


def call_eletrocardiogram():
    """
    Calls RPC Server to make eletrocardiogram
    """
    # return {'eletrocardiogram': 95.0}

    rpc = RpcClient()
    rpc_response = rpc.call('ecg')
    rpc.connection.close()

    try:

        rpc_response_decoded = rpc_response.decode()
        rpc_response_loads = json.loads(rpc_response_decoded)

        if isinstance(rpc_response_loads, list):

            if len(rpc_response_loads) != 2560:
                raise Exception()

            for i in range(len(rpc_response_loads)):

                if isinstance(rpc_response_loads[i], int):
                    rpc_response_loads[i] = float(rpc_response_loads[i])
                elif not isinstance(rpc_response_loads[i], float):
                    raise Exception()

                if rpc_response_loads[i] < 0 or rpc_response_loads[i] > 6:
                    raise Exception()

                rpc_response_loads[i] = round(rpc_response_loads[i], 6)

            rpc_response = rpc_response_loads

        else:
            raise Exception()

    except:

        rpc_response = '-1000'  # Error flag

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
