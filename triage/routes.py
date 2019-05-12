from django.shortcuts import render
from boogie.router import Router
from triage.forms import TextForm, BooleanForm

urlpatterns = Router()


@urlpatterns.route()
def welcome_page(request):
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
def text_question(request):
    form = TextForm()
    form.fields['subject'].label = "Pergunta top"
    return render(request, 'triage/text_question.html', {'form': form})


@urlpatterns.route('boolean/')
def boolean_question(request):
    form = BooleanForm()
    form.fields['boolean'].label = "Pergunta top"
    return render(request, 'triage/boolean_question.html', {'form': form})


@urlpatterns.route('risk/')
def pacient_risk(request):
    return render(request, 'triage/risk_level.html',
                  {'risk_color': 'red'})
