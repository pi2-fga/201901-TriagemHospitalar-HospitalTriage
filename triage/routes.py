from boogie.router import Router
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from triage.forms import TextForm, BooleanForm
from .utils import (send_bot_request, send_triage_to_patient_management_app,
                    map_question_animation)
from .models import Triage
from .serializers import TriageSerializer

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
    animation = map_question_animation(triage.next_question)
    info = {'title': '',
            'text': triage.next_question,
            'url': '/triage/scale',
            'animation': animation}

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
            print(triage.current_type)
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
    # TODO: send to patient management triage object
    # assuming obj is a model instance
    serialized_obj = TriageSerializer(triage)
    # print(rest_api.serialize(triage))
    response = send_triage_to_patient_management_app(serialized_obj.data)
    if response.status_code == 200:
        print('top')
    else:
        print('ooops')
        print(response)
    return render(request, 'triage/risk_level.html',
                  {'risk_color': triage.risk_level})


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
        return redirect('/triage/risk/' + str(triage.pk))
    elif next_question['type'] == 'data':
        print('oi')
    else:
        print('tipo não reconhecido')
        print(next_question)


FLOW = ['Qual é o seu nome?',
        'O que você está sentindo?'
        ]
FLOW_ATTRIBUTE = ['name', 'main_complaint']


def first_questions_flow(previous_question, answer, triage):
        number_previous = FLOW.index(previous_question)
        setattr(triage, FLOW_ATTRIBUTE[number_previous], answer)

        if number_previous == 1:
            next_question = send_bot_request(answer, triage)
            triage.bot_next_type = next_question['type']
            triage.bot_next_content = next_question['content']
            triage.save()
            return redirect_by_type(next_question, triage)
        else:
            triage.next_question = FLOW[number_previous+1]
            triage.save()
            print(triage.next_question)
            return redirect('/triage/text_question/' + str(triage.pk))
