from triage.utils import map_question_animation

QUESTIONS = [
    'Posicione seus pés na marca e espere o sinal, como mostrado abaixo, para medirmos seu peso e altura.',
    'Posicione o seu braço, como mostrado abaixo, para medirmos seus dados vitais.',
    'Posicione seu braço na braçadeira, como mostrado abaixo, para medirmos sua pressão.'
]

GIF = ['img/weight.gif', 'img/temperature.gif', 'img/pressure.gif']


def test_question_gif(client):
    for idx, question in enumerate(QUESTIONS):
        assert map_question_animation(question)[0] == GIF[idx]
