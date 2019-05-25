from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from boogie.router import Router
from triage.forms import TextForm, BooleanForm
from .utils import make_bot_request
from .models import Triage
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
    info = {'title': '',
            'text': 'Posicione seus pés na marca e clique em iniciar.',
            'url': '/triage/scale'}
    return render(request, 'triage/animation.html', info)


@urlpatterns.route('scale/' + triage_url)
def scale_page(request, triage):
    error = None

    if request.method == "POST" and 'options' in request.POST:
        value = request.POST['options']
        next_question = make_bot_request(value, triage)
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
            answer = data.get('subject')
            next_question = make_bot_request(answer, triage)
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
            next_question = make_bot_request(answer, triage)
            return redirect_by_type(next_question, triage)
    form.fields['boolean'].label = triage.next_question
    return render(request, 'triage/boolean_question.html', {'form': form})


@urlpatterns.route('risk/' + triage_url)
def pacient_risk(request, triage):
    # TODO: send to patient management triage object
    return render(request, 'triage/risk_level.html',
                  {'risk_color': triage.risk_level})


@urlpatterns.route('text_question/' + triage_url)
def first_questions(request, triage):
    print(triage.next_question)
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
    triage.save()
    if next_question['type'] == 'yes_or_no':
        return redirect('/triage/boolean/' + str(triage.pk))
    elif next_question['type'] == 'text':
        return redirect('/triage/text/' + str(triage.pk))
    elif next_question['type'] == 'pain_scale':
        return redirect('/triage/scale/' + str(triage.pk))
    elif next_question['type'] == 'info':
        return redirect('/triage/animation/' + str(triage.pk))
    elif next_question['type'] == 'risk':
        return redirect('/triage/risk/' + str(triage.pk))
    else:
        print('tipo não reconhecido')
        print(next_question)


FLOW = ['Qual é o seu nome?',
        'O que você está sentindo?',
        'Qual é a sua idade?',
        'Caso você use medicação contínua, cite quais são os remédios.',
        'Você possui alergia a alguma medicação?']
FLOW_ATTRIBUTE = ['name', 'main_complaint', 'age', 'continuos_medication',
                  'alergies']


def first_questions_flow(previous_question, answer, triage):
        number_previous = FLOW.index(previous_question)
        setattr(triage, FLOW_ATTRIBUTE[number_previous], answer)

        triage.save()
        if number_previous == 1:
            next_question = make_bot_request(answer, triage)
            if next_question['type'] == 'risk':
                triage.risk_level = next_question['content']
                triage.save()
                return pacient_risk(triage)
            else:
                triage.bot_next_type = next_question['type']
                triage.bot_next_content = next_question['content']
                triage.save()
        elif number_previous == 4:
            next_question = {'type': triage.bot_next_type,
                             'content': triage.bot_next_content}
            return redirect_by_type(next_question, triage)
        triage.next_question = FLOW[number_previous+1]
        triage.save()
        print(triage.next_question)
        return redirect('/triage/text_question/' + str(triage.pk))
