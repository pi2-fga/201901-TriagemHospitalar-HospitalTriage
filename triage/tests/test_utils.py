from triage.utils import MEASURES_DICT

QUESTIONS = [
    'Posicione o seu braço, como mostrado abaixo, para medirmos seus dados vitais.',
    'Posicione seu braço na braçadeira, como mostrado abaixo, para medirmos sua pressão.',
    'Posicione seus pés na marca e espere o sinal, como mostrado abaixo, para medirmos seu peso e altura.',
    'Aguarde para realização de mais exames.'
]

GIF = ['img/temperature.gif', 'img/pressure.gif', 'img/weight.gif', 'img/wait.gif']
TYPE = ['temperature', 'pressure', 'body_mass', 'eletrocardiogram']


def test_question_gif(client):
    for idx, question in enumerate(TYPE):
        assert MEASURES_DICT[question][0] == QUESTIONS[idx]
        assert MEASURES_DICT[question][1] == GIF[idx]
