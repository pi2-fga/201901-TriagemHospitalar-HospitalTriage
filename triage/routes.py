from django.shortcuts import render
from boogie.router import Router
from triage.forms import ScaleForm

urlpatterns = Router()


@urlpatterns.route()
def welcome_page(request):
    form = ScaleForm()
    return render(request, 'triage/welcome_page.html', {'form': form})


@urlpatterns.route('scale/')
def scale_page(request):
    form = ScaleForm()
    return render(request, 'triage/form_page.html', {'form': form})
