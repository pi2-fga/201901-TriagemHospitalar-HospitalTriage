from django.shortcuts import render
from boogie.router import Router

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
    return render(request, 'triage/scale_page.html')
