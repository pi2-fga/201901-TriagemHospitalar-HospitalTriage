from django.shortcuts import render
from boogie.router import Router
from triage.forms import TextForm, BooleanForm
from .utils import make_bot_request
urlpatterns = Router()


@urlpatterns.route()
def welcome_page(request):
    form = TextForm()
    form.fields['subject'].label = "O que você está sentindo?"
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid:
            data = request.POST.copy()
            answer = data.get('subject')
            next_page = make_bot_request(answer)
            return redirect_by_type(next_page, request)
    return render(request, 'triage/text_question.html', {'form': form})


@urlpatterns.route('animation/')
def gif_page(request):
    info = {'title': '',
            'text': 'Posicione seus pés na marca e clique em iniciar.',
            'url': '/triage/scale'}
    return render(request, 'triage/animation.html', info)


@urlpatterns.route('scale/')
def scale_page(request):
    if request.method == "POST" and 'options' in request.POST:
        # value = request.POST['options']
        # TODO: IMPLEMENT SENDING INFORMATION TO BOT
        pass
    elif request.method == "POST":
        pass
        # TODO: IMPLEMENT validation
    return render(request, 'triage/pain_scale.html')


@urlpatterns.route('text/')
def text_question(request, question):
    form = TextForm()
    form.fields['subject'].label = question
    return render(request, 'triage/text_question.html', {'form': form})


@urlpatterns.route('boolean/')
def boolean_question(request, question):
    form = BooleanForm()
    form.fields['boolean'].label = question
    return render(request, 'triage/boolean_question.html', {'form': form})


@urlpatterns.route('risk/')
def pacient_risk(request, risk_color):
    return render(request, 'triage/risk_level.html',
                  {'risk_color': risk_color})


def redirect_by_type(next_question, request):
    if next_question['type'] == 'yes_or_no':
        return boolean_question(request, next_question['content'])
    elif next_question['type'] == 'text':
        return text_question(request, next_question['content'])
    elif next_question['type'] == 'pain_scale':
        return scale_page(request)
    elif next_question['type'] == 'info':
        return gif_page(request)
    elif next_question['type'] == 'risk':
        return pacient_risk(request, next_question['content'])
    else:
        print('tipo não reconhecido')
        print(next_question)
