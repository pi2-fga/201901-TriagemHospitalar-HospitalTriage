from boogie.router import Router
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from triage.forms import TextForm, BooleanForm
from .utils import (send_bot_request, send_triage_to_patient_management_app,
                    save_values, call_eletrocardiogram)
from .models import Triage
from .serializers import TriageSerializer
from .utils import TRIAGE_RISK_CATEGORIES, MEASURES_DICT


urlpatterns = Router(
    models={
        'triage': Triage,
    },
    lookup_field={
        'triage': 'pk',
    },
)
triage_url = f'<model:triage>/'


@urlpatterns.route()
def welcome_page(request):
    question = _("Qual é o seu nome?")
    form = TextForm()
    form.fields['subject'].label = question
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid:
            triage = Triage.objects.create()
            data = request.POST.copy()
            answer = data.get('subject')
            return first_questions_flow(question, answer, triage)
    return render(request, 'triage/text_question.html', {'form': form})


@urlpatterns.route('animation/' + triage_url)
def gif_page(request, triage):
    question_info = MEASURES_DICT[triage.next_question]
    info = {'title': '',
            'text': question_info[0],
            'animation': question_info[1]}
    if request.method == "POST":
        save_values(triage, question_info[2])

        return make_measurements(triage, triage.next_question)
    return render(request, 'triage/animation.html', info)


@urlpatterns.route('scale/' + triage_url)
def scale_page(request, triage):
    error = None

    if request.method == "POST" and 'options' in request.POST:
        value = request.POST['options']
        next_question = send_bot_request(value, triage)
        return redirect_by_type(next_question, triage)
    elif request.method == "POST":
        error = _('Você precisa escolher uma opção')
    return render(request, 'triage/pain_scale.html', {'errors': error})


@urlpatterns.route('text/' + triage_url)
def text_question(request, triage):
    form = TextForm()
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            if triage.bot_next_type == 'textr':
                answer = triage.next_question + ' ' + data.get('subject')
            else:
                answer = data.get('subject')
            next_question = send_bot_request(answer, triage)
            return redirect_by_type(next_question, triage)
    form.fields['subject'].label = triage.next_question
    return render(request, 'triage/text_question.html', {'form': form})


@urlpatterns.route('boolean/' + triage_url)
def boolean_question(request, triage):
    form = BooleanForm()
    if request.method == "POST":
        form = BooleanForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data['boolean']
            next_question = send_bot_request(answer, triage)
            return redirect_by_type(next_question, triage)
    form.fields['boolean'].label = triage.next_question
    return render(request, 'triage/boolean_question.html', {'form': form})


@urlpatterns.route('risk/' + triage_url)
def pacient_risk(request, triage):
    serialized_obj = TriageSerializer(triage)
    response = send_triage_to_patient_management_app(serialized_obj.data)
    if response.status_code == 200:
        color = Triage.TRIAGE_RISK_CATEGORIES[triage.risk_level][1]
        return render(request, 'triage/risk_level.html',
                      {'risk_color': color})


@urlpatterns.route('text_question/' + triage_url)
def first_questions(request, triage):
    form = TextForm()
    form.fields['subject'].label = triage.next_question
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid:
            data = request.POST.copy()
            answer = data.get('subject')
            return first_questions_flow(triage.next_question, answer, triage)
    return render(request, 'triage/text_question.html', {'form': form})


@urlpatterns.route('eletrocardiogram/' + triage_url)
def eletrocardiogram_page(request, triage):
    question_info = MEASURES_DICT[triage.next_question]
    info = {'title': '',
            'text': question_info[0],
            'animation': question_info[1]}
    if request.method == "POST":
        save_values(triage, question_info[2])
        call_eletrocardiogram()
        answer = "Os dados foram salvos na aplicação da estação da triagem."
        next_question = send_bot_request(answer, triage)
        return redirect_by_type(next_question, triage)
    return render(request, 'triage/animation.html', info)


def redirect_by_type(next_question, triage):
    triage.next_question = next_question['content']
    triage.current_type = next_question['type']
    triage.save()
    print(next_question['type'])
    if next_question['type'] == 'yes_or_no':
        return redirect('/triage/boolean/' + str(triage.pk))
    elif next_question['type'] == 'text':
        return redirect('/triage/text/' + str(triage.pk))
    elif next_question['type'] == 'textr':
        return redirect('/triage/text/' + str(triage.pk))
    elif next_question['type'] == 'pain_scale':
        return redirect('/triage/scale/' + str(triage.pk))
    elif next_question['type'] == 'info':
        return redirect('/triage/animation/' + str(triage.pk))
    elif next_question['type'] == 'risk':
        choice = TRIAGE_RISK_CATEGORIES[next_question['content']]
        triage.risk_level = choice
        triage.save()
        return redirect('/triage/risk/' + str(triage.pk))
    elif next_question['type'] == 'measurements':
        return make_measurements(triage)
    elif next_question['type'] == 'data':
        answer = process_data(next_question['content'], triage)
        next_question = send_bot_request(answer, triage)
        return redirect_by_type(next_question, triage)
    elif next_question['type'] == 'signal':
        answer = "Os dados foram salvos na aplicação da estação da triagem."
        next_question = send_bot_request(answer, triage)
        return redirect_by_type(next_question, triage)
    elif next_question['type'] == 'eletrocardiogram':
        return redirect('/triage/eletrocardiogram/' + str(triage.pk))
    else:
        print('tipo não reconhecido')
        print(next_question)


@urlpatterns.route('wboolean/' + triage_url)
def wboolean_question(request, triage):
    form = BooleanForm()
    if request.method == "POST":
        form = BooleanForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data['boolean']
            if answer == 'Sim':
                triage.wheelchair = True
                triage.save()
            next_question = {'type': triage.bot_next_type,
                             'content': triage.bot_next_content}
            return redirect_by_type(next_question, triage)
    form.fields['boolean'].label = 'Você é usuário de cadeira de rodas?'

    return render(request, 'triage/boolean_question.html', {'form': form})


FLOW = ['Qual é o seu nome?',
        'O que você está sentindo?',
        'Você usa medicação contínua? Se sim, cite quais.'
        ]
FLOW_ATTRIBUTE = ['name', 'main_complaint', 'continuos_medication',
                  'wheelchair']


def first_questions_flow(previous_question, answer, triage):
        number_previous = FLOW.index(previous_question)
        setattr(triage, FLOW_ATTRIBUTE[number_previous], answer)
        triage.save()
        print(FLOW_ATTRIBUTE[number_previous])
        print(triage.main_complaint)
        print(triage.continuos_medication)
        if number_previous == 1:
            next_question = send_bot_request(answer, triage)
            if next_question['type'] == 'risk':
                choice = TRIAGE_RISK_CATEGORIES[next_question['content']]
                triage.risk_level = choice
                triage.save()
                return redirect('/triage/risk/' + str(triage.pk))
            else:
                triage.bot_next_type = next_question['type']
                triage.bot_next_content = next_question['content']
                triage.save()
        elif number_previous == 2:
            next_question = {'type': triage.bot_next_type,
                             'content': triage.bot_next_content}
            return redirect('/triage/wboolean/' + str(triage.pk))
        triage.next_question = FLOW[number_previous+1]
        triage.save()
        return redirect('/triage/text_question/' + str(triage.pk))


FLOWM = ['temperature', 'pressure', 'body_mass']


def make_measurements(triage, previous_question=None):
    """
    decides which measurements to make
    """
    wheelchair = triage.wheelchair
    if not previous_question:
        triage.next_question = FLOWM[0]
        triage.save()
        return redirect('/triage/animation/' + str(triage.pk))
    else:
        number_previous = FLOWM.index(previous_question)
        if number_previous == 2 or (number_previous == 1 and wheelchair):
            answer = triage.get_measurements()
            next_question = send_bot_request(answer, triage)
            return redirect_by_type(next_question, triage)
        else:
            triage.next_question = FLOWM[number_previous+1]
            triage.save()
            return redirect('/triage/animation/' + str(triage.pk))


def process_data(content, triage):
    previous_diagnosis = {'diabetes': 'Diabetes',
                          'infarction': 'Infarto do miocárdio',
                          'migrain': 'Enxaqueca'}

    partition = content.partition(".")
    attributes = partition[0].split()
    it = list(iter(attributes))
    names = it[::2]
    values = []
    for x in names:
        if x in previous_diagnosis.keys() and (it[it.index(x)+1] != 'None'):
            values.append(previous_diagnosis[x])
        else:
            setattr(triage, x, it[it.index(x)+1])
    if values:
        triage.set_previous_diagnosis(values)
    triage.save()
    return "Os dados foram salvos na aplicação da estação da triagem."
